# InstaBasic

[![PyPI](https://img.shields.io/pypi/v/instabasic)](https://pypi.org/project/instabasic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/instabasic)](https://github.com/ChaseRun/instabasic)
[![PyPI - License](https://img.shields.io/pypi/l/instabasic)](https://github.com/ChaseRun/instabasic/blob/master/LICENSE)

InstaBasic is an API wrapper for [Instagram's Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api/). I was in the process of writing python code using the Basic Display API, and I created this package for others to use. My goal for this is to support every official Basic Display API [endpoint](https://developers.facebook.com/docs/instagram-basic-display-api/reference).

_This package does not support the [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)_

## Installation

`pip install instabasic`

## Overview

The Instagram Basic Display API is an HTTP-based API for apps to get an Instagram user’s profile, images, videos, and albums. To use InstaBasic you will need to do the following:

 - Create a Facebook Developer Account
 - Create a public website
 - Provide Instagram users with an Auth link for access to their data.

Instagram's documentation includes a thorough [overview](https://developers.facebook.com/docs/instagram-basic-display-api/overview) of the API's capabilities. If you are unfamiliar with the Basic Display API, I recommend first reviewing their [Get Started Guide](https://developers.facebook.com/docs/instagram-basic-display-api/getting-started) before looking at InstaBasic's documentation.

## Usage

```
from instabasic.api import API

app_id = 'YOUR APP ID'
app_secret = 'YOUR APP SECRET'
redirect_url = 'YOUR REDIRECT URL'

insta = API(appID, appSecret, redirectUrl)

# Authorization URL for your users to sign in
auth_url = insta.get_auth_url()
print(auth_url)

# Get the short lived access token (valid for 1 hour)
short_token = insta.get_short_token(auth_code)

# Exchange this token for a long lived token (valid for 60 days)
long_token = insta.get_long_token(auth_code)

# Refresh the long lived token
long_token = insta.refresh_long_token(long_token)

# Get information about the user
user = insta.get_user(long_token)

# Get information about the user's media
user_media = insta.get_user_media(long_token)
```

## Documentation

 - [InstaBasic](https://github.com/ChaseRun/instabasic)
 - [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api/)

## Support

[Contributing Documentation](https://github.com/ChaseRun/instabasic) | Please feel free to contribute and suggest additional features.

## Disclamer

InstaBasic is in no way affliated, endorsed, or certified by Instagram. This is an independent and unofficial package. Strictly not for spam. Use at your own risk.
