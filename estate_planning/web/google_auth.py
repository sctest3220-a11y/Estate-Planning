"""Google (Gmail) OAuth login, gated on environment configuration.

Requires two environment variables, obtained from Google Cloud Console
(APIs & Services -> Credentials -> OAuth 2.0 Client ID, type "Web application"):

    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET

Add the callback URL to the client's "Authorized redirect URIs", e.g.
    http://127.0.0.1:5001/auth/google/callback   (local dev)
    https://your-domain/auth/google/callback      (production)

If the variables are absent, is_configured() returns False and the app simply
hides the "Sign in with Google" option and keeps working with local accounts.
"""

import os

from authlib.integrations.flask_client import OAuth

_CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth = OAuth()


def is_configured():
    return bool(
        os.environ.get("GOOGLE_CLIENT_ID") and os.environ.get("GOOGLE_CLIENT_SECRET")
    )


def init_app(app):
    """Register the Google OAuth client if credentials are present."""
    if not is_configured():
        return
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        server_metadata_url=_CONF_URL,
        client_kwargs={"scope": "openid email profile"},
    )


def authorize_redirect(redirect_uri):
    return oauth.google.authorize_redirect(redirect_uri)


def fetch_email():
    """Complete the OAuth exchange and return the user's verified email, or None."""
    token = oauth.google.authorize_access_token()
    userinfo = token.get("userinfo") or {}
    if not userinfo.get("email_verified"):
        return None
    return userinfo.get("email")
