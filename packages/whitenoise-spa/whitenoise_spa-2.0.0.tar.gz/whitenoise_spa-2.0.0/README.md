# whitenoise-spa

Serve SPA (Single Page Application) in django using whitenoise

## Installation

You can install the package via pip:

```
pip install whitenoise-spa
```

## Usage

1. Edit your `settings.py` file and add `whitenoise_spa.middleware.WhiteNoiseSPAMiddleware` to the MIDDLEWARE list. The middleware should be placed directly after the Django SecurityMiddleware (if you are using it) and before all other middleware. This middleware replaces the whitenoise middleware.
   ```python
   MIDDLEWARE = [
       # ...
       "django.middleware.security.SecurityMiddleware",
       "whitenoise_spa.middleware.WhiteNoiseSPAMiddleware",
       # ...
   ]
   ```
2. Configure SPA root and urls.
   ```python
   WHITENOISE_SPA_ROOT = BASE_DIR / "dist"
   WHITENOISE_SPA_URL_PATTERN = "/|/login/|/settings/"
   ```

## License

This project is licensed under the terms of the MIT license.
