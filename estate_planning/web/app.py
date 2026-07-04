"""Flask app: login-gated, terms-acknowledged questionnaire that produces
Thai-law advice and draft documents.

Privacy: estate-planning inputs are processed in memory per request and are
never written to disk or stored server-side. Only account credentials and a
terms-acknowledgment timestamp are persisted (see store.py).
"""

import io
import os
import zipfile
from functools import wraps

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
from ..documents import DOCUMENT_RENDERERS
from ..models import STATUS_CHOICES, RELATIONSHIP_CHOICES
from .forms import build_plan
from .store import UserStore

store = UserStore()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("ESTATE_SECRET_KEY", "dev-only-change-me")

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

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            ok, error = store.create_user(username, password)
            if ok:
                flash("Account created. Please log in.", "success")
                return redirect(url_for("login"))
            flash(error, "error")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            if store.verify(username, password):
                session.clear()
                session["user"] = username.strip().lower()
                session["acknowledged"] = store.has_acknowledged(session["user"])
                nxt = request.args.get("next") or url_for("index")
                return redirect(nxt)
            flash("Invalid username or password.", "error")
        return render_template("login.html")

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
            flash("You must acknowledge the terms to continue.", "error")
        return render_template("terms.html")

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
            advice = assess(plan)
            documents = {
                key: (title, render(plan))
                for key, (title, render) in DOCUMENT_RENDERERS.items()
            }
            return render_template(
                "results.html",
                advice=advice,
                documents=documents,
                form=request.form,
            )
        return render_template(
            "questionnaire.html",
            statuses=STATUS_CHOICES,
            relationships=RELATIONSHIP_CHOICES,
            form={},
        )

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

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for key, (title, render) in DOCUMENT_RENDERERS.items():
                zf.writestr(f"{key}.md", render(plan))
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
