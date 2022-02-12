"""
A collection of functions that call Instagram Basic Display API endpoints.
Functions:
    get_auth_url(app_id, redirect_url, state) -> string
    get_short_token(app_id, app_secret, redirect_url, auth_code) -> string
    get_long_token(app_id, app_secret, redirect_url, auth_code) -> string
    refresh_long_token(token) -> string

    get_media(token, media_id, fields) -> object
    get_album_images(token, media_id, fields) -> object

    get_user(token, api_version, fields) -> object
    get_user_media(token, api_version, fields) -> object
"""
import requests

# Instagram
API_VERSION = "v12.0"
GRAPH_URL = "https://graph.instagram.com"
OAUTH_URL = "https://api.instagram.com/oauth"
MEDIA_FIELDS = (
    "id,media_type,media_url,permalink,thumbnail_url,caption,timestamp,username"
)
ALBUM_IMAGE_FIELDS = "id,media_type,media_url,thumbnail_url"
USER_FIELDS = "id,username,account_type,media_count,media"

# --------------------
#  Authorizationc
# --------------------
def get_auth_url(app_id, redirect_url, state=False):
    """Get an app's authorization url."""
    state_url = ""
    if state:
        state_url = f"&state={state}"
    return (
        f"{OAUTH_URL}/authorize"
        f"?client_id={app_id}"
        f"&redirect_uri={redirect_url}"
        "&response_type=code"
        "&scope=user_profile,user_media"
        f"{state_url}"
    )


def get_short_token(app_id, app_secret, redirect_url, auth_code):
    """Get a short-lived access token."""
    url = f"{OAUTH_URL}/access_token"
    payload = {
        "client_id": app_id,
        "client_secret": app_secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_url,
        "code": auth_code,
    }
    resp = requests.post(url, data=payload).json()
    return resp["access_token"]


def get_long_token(app_id, app_secret, redirect_url, auth_code):
    """Get a long-lived access token."""
    url = f"{GRAPH_URL}/access_token"
    query = {
        "client_secret": app_secret,
        "grant_type": "ig_exchange_token",
        "access_token": get_short_token(app_id, app_secret, redirect_url, auth_code),
    }
    resp = requests.get(url, params=query).json()
    return resp["access_token"]


def refresh_long_token(long_token):
    """Refresh a long-lived access token."""
    url = f"{GRAPH_URL}/refresh_access_token"
    query = {"grant_type": "ig_refresh_token", "access_token": long_token}
    resp = requests.get(url, params=query).json()
    return resp["access_token"]


# --------------------
#  Media
# --------------------
def get_media(token, media_id, fields=MEDIA_FIELDS):
    """Get media's attributes."""
    url = f"{GRAPH_URL}/{media_id}"
    query = {
        "fields": "".join(fields),
        "access_token": token,
    }
    req = requests.get(url, params=query).json()
    if req["media_type"] == "CAROUSEL_ALBUM":
        del req["media_url"]
        album_images = get_album_images(token, req["id"])["data"]
        req["album_images"] = album_images
    return req


def get_album_images(token, media_id, fields=ALBUM_IMAGE_FIELDS):
    """Get all images for an album."""
    url = f"{GRAPH_URL}/{media_id}/children"
    query = {
        "fields": "".join(fields),
        "access_token": token,
    }
    req = requests.get(url, params=query).json()
    return req


# --------------------
#  User
# --------------------
def get_user(token, api_version=API_VERSION, fields=USER_FIELDS):
    """Get user's information"""
    url = f"{GRAPH_URL}/{api_version}/me"
    query = {
        "fields": "".join(fields),
        "access_token": token,
    }
    req = requests.get(url, params=query).json()
    return req


def get_user_media(token, api_version=API_VERSION, fields=MEDIA_FIELDS):
    """Get user's media."""
    url = f"{GRAPH_URL}/{api_version}/me/media"
    query = {
        "fields": "".join(fields),
        "access_token": token,
    }
    req = requests.get(url, params=query).json()
    for idx, media in enumerate(req["data"]):
        if media["media_type"] == "CAROUSEL_ALBUM":
            req["data"][idx] = get_media(token, media["id"])
    return req
