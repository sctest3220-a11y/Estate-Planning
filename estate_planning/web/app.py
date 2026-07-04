"""Flask app: login-gated, terms-acknowledged questionnaire that produces
Thai-law advice and draft documents in English, Thai, or dual language.

Privacy: estate-planning inputs are processed in memory per request and are
never written to disk or stored server-side. Only account credentials and a
terms-acknowledgment timestamp are persisted (see store.py).
"""

import io
import os
import zipfile
from functools import wraps

import markdown as md

from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ..advice import assess
from ..documents import (
    DOCUMENT_SPECS,
    LANGUAGE_LABELS,
    LANGUAGE_MODES,
    LIVING_WILL_OPTIONS,
    MODE_DUAL,
    document_title,
    generate,
)
from ..asset_workbook import parse_workbook, template_xlsx
from ..assets_csv import parse_csv
from ..bequests import summarize
from ..models import ASSET_CATEGORIES, STATUS_CHOICES, RELATIONSHIP_CHOICES
from ..sample import sample_plan
from ..tax import tax_plan
from ..tips import planning_tips
from . import google_auth
from .forms import build_plan, parse_language, parse_selected_docs
from .i18n import DEFAULT_UI_LANG, UI_LANGS, t as translate
from .store import UserStore

store = UserStore()


def _doc_catalog(mode=MODE_DUAL):
    """[(key, english_title, localized_title), ...] for building selection UIs."""
    return [
        (key, spec[0], document_title(key, mode)) for key, spec in DOCUMENT_SPECS.items()
    ]


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("ESTATE_SECRET_KEY", "dev-only-change-me")
    google_auth.init_app(app)

    @app.template_filter("attr_json")
    def attr_json(value):
        """JSON-encode a value, escaped for safe use inside an HTML attribute."""
        import json

        from markupsafe import escape

        return escape(json.dumps(value, ensure_ascii=False))

    @app.template_filter("urlize_links")
    def urlize_links(text):
        """Escape text, then turn https URLs into clickable links."""
        import re
        from markupsafe import escape

        parts = re.split(r"(https?://[^\s]+)", text)
        out = []
        for part in parts:
            if part.startswith("http"):
                url = str(escape(part))
                out.append(f'<a href="{url}" target="_blank" rel="noopener">{url}</a>')
            else:
                out.append(str(escape(part)))
        return "".join(out)

    # Make catalog + language options + UI translations available to every template.
    @app.context_processor
    def inject_globals():
        ui_lang = session.get("ui_lang", DEFAULT_UI_LANG)
        label_key = "label_th" if ui_lang == "th" else "label_en"
        living_will_catalog = [
            (key, opt[label_key]) for key, opt in LIVING_WILL_OPTIONS.items()
        ]
        return {
            "doc_catalog": _doc_catalog(),
            "language_modes": LANGUAGE_MODES,
            "language_labels": LANGUAGE_LABELS,
            "asset_categories": ASSET_CATEGORIES,
            "living_will_catalog": living_will_catalog,
            "google_enabled": google_auth.is_configured(),
            "ui_lang": ui_lang,
            "ui_langs": UI_LANGS,
            "t": lambda key: translate(key, ui_lang),
        }

    @app.route("/set-language/<lang>")
    def set_language(lang):
        if lang in UI_LANGS:
            session["ui_lang"] = lang
        return redirect(request.referrer or url_for("index"))

    def _t(key):
        return translate(key, session.get("ui_lang", DEFAULT_UI_LANG))

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("user"):
                return redirect(url_for("login", next=request.path))
            return view(*args, **kwargs)

        return wrapped

    def terms_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("acknowledged"):
                return redirect(url_for("terms"))
            return view(*args, **kwargs)

        return wrapped

    @app.route("/")
    def index():
        if not session.get("user"):
            return redirect(url_for("login"))
        if not session.get("acknowledged"):
            return redirect(url_for("terms"))
        return redirect(url_for("questionnaire"))

    # ---- Authentication ----------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            ok, error = store.create_user(
                request.form.get("username", ""), request.form.get("password", "")
            )
            if ok:
                flash(_t("flash_account_created"), "success")
                return redirect(url_for("login"))
            flash(error, "error")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            if store.verify(username, password):
                _start_session(username.strip().lower())
                return redirect(request.args.get("next") or url_for("index"))
            flash(_t("flash_invalid_login"), "error")
        return render_template("login.html")

    @app.route("/login/google")
    def login_google():
        if not google_auth.is_configured():
            flash(_t("flash_google_not_configured"), "error")
            return redirect(url_for("login"))
        redirect_uri = url_for("google_callback", _external=True)
        return google_auth.authorize_redirect(redirect_uri)

    @app.route("/auth/google/callback")
    def google_callback():
        if not google_auth.is_configured():
            return redirect(url_for("login"))
        try:
            email = google_auth.fetch_email()
        except Exception:
            flash(_t("flash_google_failed"), "error")
            return redirect(url_for("login"))
        if not email:
            flash(_t("flash_google_email"), "error")
            return redirect(url_for("login"))
        username = store.create_or_get_google_user(email)
        _start_session(username)
        return redirect(url_for("index"))

    def _start_session(username):
        session.clear()
        session["user"] = username
        session["acknowledged"] = store.has_acknowledged(username)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/terms", methods=["GET", "POST"])
    @login_required
    def terms():
        if request.method == "POST":
            if request.form.get("acknowledge") == "on":
                store.record_acknowledgment(session["user"])
                session["acknowledged"] = True
                return redirect(url_for("questionnaire"))
            flash(_t("terms_must_ack"), "error")
        return render_template("terms.html")

    # ---- Asset sheet template (offline) ------------------------------------

    @app.route("/asset-template.xlsx")
    @login_required
    @terms_required
    def asset_template():
        return Response(
            template_xlsx(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=asset_sheet_template.xlsx"
            },
        )

    # ---- Preview (no data entry required) ----------------------------------

    @app.route("/preview")
    @login_required
    @terms_required
    def preview():
        mode = parse_language(request.args)
        selected = [k for k in request.args.getlist("documents") if k in DOCUMENT_SPECS]
        selected = selected or list(DOCUMENT_SPECS.keys())
        documents = generate(sample_plan(), selected, mode)
        return render_template(
            "preview.html",
            documents=documents,
            selected=selected,
            mode=mode,
        )

    # ---- Questionnaire, results, download ----------------------------------

    @app.route("/questionnaire", methods=["GET", "POST"])
    @login_required
    @terms_required
    def questionnaire():
        if request.method == "POST":
            plan, errors = build_plan(request.form)
            if errors:
                for e in errors:
                    flash(e, "error")
                return render_template(
                    "questionnaire.html",
                    statuses=STATUS_CHOICES,
                    relationships=RELATIONSHIP_CHOICES,
                    form=request.form,
                )
            # Merge an uploaded asset sheet, if provided (non-fatal on error).
            # Accepts the multi-tab .xlsx template or a plain .csv.
            upload = request.files.get("asset_csv")
            if upload and upload.filename:
                try:
                    raw = upload.read()
                    if upload.filename.lower().endswith(".xlsx"):
                        plan.assets.extend(parse_workbook(raw))
                    else:
                        plan.assets.extend(parse_csv(raw.decode("utf-8-sig")))
                except Exception:
                    flash(_t("flash_csv_failed"), "error")
            mode = parse_language(request.form)
            selected = parse_selected_docs(request.form)
            advice = assess(plan)
            documents = generate(plan, selected, mode)
            return render_template(
                "results.html",
                advice=advice,
                documents=documents,
                tax=tax_plan(plan),
                tips=planning_tips(plan),
                bequests=summarize(plan),
                assets=plan.assets,
                form=request.form,
            )
        return render_template(
            "questionnaire.html",
            statuses=STATUS_CHOICES,
            relationships=RELATIONSHIP_CHOICES,
            form={},
        )

    @app.route("/print", methods=["POST"])
    @login_required
    @terms_required
    def print_documents():
        # Regenerate from re-posted form data (no server-side storage), render
        # the Markdown as HTML, and return a clean print-ready page.
        plan, errors = build_plan(request.form)
        if errors:
            for e in errors:
                flash(e, "error")
            return redirect(url_for("questionnaire"))
        mode = parse_language(request.form)
        selected = parse_selected_docs(request.form)
        documents = generate(plan, selected, mode)
        rendered = {
            key: (title, md.markdown(content, extensions=["tables"]))
            for key, (title, content) in documents.items()
        }
        return render_template("print.html", documents=rendered)

    @app.route("/download", methods=["POST"])
    @login_required
    @terms_required
    def download():
        # Regenerate documents from the re-posted form data; nothing is read
        # from server-side storage, so no PII persists between requests.
        plan, errors = build_plan(request.form)
        if errors:
            for e in errors:
                flash(e, "error")
            return redirect(url_for("questionnaire"))

        mode = parse_language(request.form)
        selected = parse_selected_docs(request.form)
        documents = generate(plan, selected, mode)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for key, (_title, content) in documents.items():
                zf.writestr(f"{key}_{mode}.md", content)
        buf.seek(0)
        return Response(
            buf.getvalue(),
            mimetype="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=estate_planning_drafts.zip"
            },
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
