import os
import functools
import flask
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

def load_credentials():
    auth_string = os.getenv('PROVISIONER_AUTH', '')
    if not auth_string:
        return {}
    credentials = {}
    for pair in auth_string.split(','):
        pair = pair.strip()
        if ':' in pair:
            username, password = pair.split(':', 1)
            credentials[username.strip()] = password.strip()
    return credentials


def verify_credentials(username, password):
    if not username or not password:
        return False
    credentials = load_credentials()
    if username not in credentials:
        return False

    stored_hash = credentials[username]
    return hashlib.sha256(password.encode()).hexdigest() == stored_hash


def require_basic_auth(f):
    # Decorator to require HTTP Basic Authentication for Flask routes.
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if credentials are configured
        credentials = load_credentials()
        if not credentials:
            logger.error("No credentials configured! Set PROVISIONER_AUTH environment variable.")
            return flask.Response(
                json.dumps({
                    "error": "Authentication not configured",
                    "message": "Server authentication is not properly configured."
                }),
                status=500,
                content_type="application/json"
            )
        # Get Basic Auth credentials from request
        auth = flask.request.authorization
        if not auth or not verify_credentials(auth.username, auth.password):
            logger.warning(
                f"Failed authentication attempt from {flask.request.remote_addr} "
                f"for {flask.request.method} {flask.request.path}"
            )
            return flask.Response(
                json.dumps({
                    "error": "Unauthorized",
                    "message": "Valid credentials required."
                }),
                status=401,
                content_type="application/json",
                headers={'WWW-Authenticate': 'Basic realm="DCI Provisioner"'}
            )
        # Log successful authentication
        logger.info(
            f"Authenticated request from {auth.username} "
            f"({flask.request.remote_addr}) to {flask.request.method} {flask.request.path}"
        )
        # Store username in request context
        flask.g.username = auth.username

        return f(*args, **kwargs)
    return decorated_function
