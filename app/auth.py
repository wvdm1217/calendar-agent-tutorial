from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore

from app.config import get_settings

settings = get_settings()


def authenticate():
    """Handles user authentication for the Google Calendar API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if settings.token_file.exists():
        creds = Credentials.from_authorized_user_file(
            settings.token_file, settings.scopes
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.credentials_file, settings.scopes
            )
            try:
                creds = flow.run_local_server(
                    port=settings.auth_port, open_browser=False
                )
            except Exception as e:
                print(f"\nAuthentication error: {e}")
                print("\nPlease ensure:")
                print(f"1. Port {settings.auth_port} is accessible")
                print("2. You've opened the URL in your browser")
                print("3. The redirect URI is configured in Google Cloud Console")
                raise
        # Save the credentials for the next run
        with open(settings.token_file, "w") as token:
            token.write(creds.to_json())
    return creds


def refresh_token():
    """Refreshes the authentication token."""
    creds = None
    if settings.token_file.exists():
        creds = Credentials.from_authorized_user_file(
            settings.token_file, settings.scopes
        )
    if creds and creds.refresh_token:
        creds.refresh(Request())
        with open(settings.token_file, "w") as token:
            token.write(creds.to_json())
        return True
    return False
