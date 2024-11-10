import re
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from whitenoise.middleware import WhiteNoiseMiddleware  # type:ignore


class WhiteNoiseSPAMiddleware(WhiteNoiseMiddleware):
    def __init__(self, *args: Any, **kwargs: Any):
        self.pattern: str | None = getattr(
            settings, "WHITENOISE_SPA_URL_PATTERN", None
        )
        super().__init__(*args, **kwargs)  # type:ignore
        root = getattr(settings, "WHITENOISE_SPA_ROOT", None)
        if root is not None:
            self.add_files(root)  # type:ignore

    def __call__(self, request: HttpRequest):  # type:ignore
        if self.pattern is not None and re.fullmatch(
            self.pattern, request.path_info
        ):
            request.path_info = "/index.html"
        return super().__call__(request)  # type:ignore
