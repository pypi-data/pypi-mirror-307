from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from enum import Enum
from io import BytesIO
from pathlib import Path
from time import sleep
from typing import Optional, Union
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException

DOWNLOAD_ATTEMPTS = 10
DOWNLOAD_INTERRUPTION = 1


class ImagePigError(Exception):
    pass


class APIResponse:
    def __init__(self, content: dict) -> None:
        self.content = content

    @property
    def data(self) -> bytes:
        if data := self.content.get("image_data"):
            return b64decode(data)

        if self.url:
            for _ in range(DOWNLOAD_ATTEMPTS):
                response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})

                if response.ok:
                    return response.content

                if response.status_code == 404:
                    sleep(DOWNLOAD_INTERRUPTION)
                else:
                    break

            response.raise_for_status()

        return None

    @property
    def image(self) -> object:
        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError('Pillow package is not installed. Please install it using "pip install pillow".') from e

        return Image.open(BytesIO(self.data))

    @property
    def url(self) -> str:
        return self.content.get("image_url")

    @property
    def seed(self) -> Optional[int]:
        return self.content.get("seed")

    @property
    def mime_type(self) -> Optional[str]:
        return self.content.get("mime_type")

    @property
    def duration(self) -> Optional[timedelta]:
        if (started_at := self.content.get("started_at")) and (completed_at := self.content.get("completed_at")):
            return datetime.fromisoformat(completed_at) - datetime.fromisoformat(started_at)

        return None

    def save(self, path: str) -> None:
        with Path(path).open("wb") as f:
            f.write(self.data)


class ImagePig:
    """
    Image Pig API
    https://imagepig.com/docs/
    """

    class Proportion(Enum):
        LANDSCAPE = "landscape"
        PORTRAIT = "portrait"
        SQUARE = "square"
        WIDE = "wide"

    def __init__(self, api_key: str, raise_exceptions: bool = True, api_url: str = "https://api.imagepig.com") -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.raise_exceptions = raise_exceptions

    def _call_api(self, endpoint: str, payload: dict) -> APIResponse:
        response = requests.post(
            f"{self.api_url}/{endpoint}",
            headers={"Api-Key": self.api_key},
            json=payload,
        )

        try:
            content = response.json() or {}
        except RequestException:
            content = {}

        if response.ok or not self.raise_exceptions:
            return APIResponse(content)

        message = content.get("error", "")

        if (
            not message
            and (detail := content.get("detail"))
            and isinstance(detail, list)
            and isinstance(detail[0], dict)
        ):
            message = detail[0].get("msg", "")

        raise ImagePigError(f"The API responded with HTTP {response.status_code}: {message}")

    def default(self, prompt: str, negative_prompt: str = "", **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "negative_prompt": prompt})
        return self._call_api("", kwargs)

    def xl(self, prompt: str, negative_prompt: str = "", **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "negative_prompt": prompt})
        return self._call_api("xl", kwargs)

    def flux(self, prompt: str, proportion: Proportion = Proportion.LANDSCAPE, **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "proportion": proportion.value})
        return self._call_api("flux", kwargs)

    def _prepare_image(self, image: Union[str, bytes], param_name: str, params: dict):
        if isinstance(image, str):
            parsed_url = urlparse(image)

            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                raise ImagePigError(f"Invalid URL: {image}. We support only the HTTP(S) protocol.")

            params[f"{param_name}_url"] = image
        elif isinstance(image, bytes):
            params[f"{param_name}_data"] = b64encode(image)
        else:
            raise TypeError(f"Please provide str or bytes object as {param_name}.")

        return params

    def faceswap(self, source_image: Union[str, bytes], target_image: Union[str, bytes], **kwargs) -> APIResponse:
        kwargs = self._prepare_image(source_image, "source_image", kwargs)
        kwargs = self._prepare_image(target_image, "target_image", kwargs)
        return self._call_api("faceswap", kwargs)

    def upscale(self, image: Union[str, bytes], upscaling_factor: int = 2, **kwargs) -> APIResponse:
        if upscaling_factor not in (2, 4, 8):
            raise ImagePigError("Upscaling factor needs to be 2, 4 or 8.")

        kwargs["upscaling_factor"] = upscaling_factor
        kwargs = self._prepare_image(image, "image", kwargs)
        return self._call_api("upscale", kwargs)

    def cutout(self, image: Union[str, bytes], **kwargs) -> APIResponse:
        kwargs = self._prepare_image(image, "image", kwargs)
        return self._call_api("cutout", kwargs)

    def replace(
        self, image: Union[str, bytes], select_prompt: str, positive_prompt: str, negative_prompt: str = "", **kwargs
    ):
        kwargs.update(
            {
                "select_prompt": select_prompt,
                "positive_prompt": positive_prompt,
                "negative_prompt": negative_prompt,
            }
        )
        kwargs = self._prepare_image(image, "image", kwargs)
        return self._call_api("replace", kwargs)

    def outpaint(
        self,
        image: Union[str, bytes],
        positive_prompt: str,
        negative_prompt: str = "",
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        left: int = 0,
        **kwargs,
    ):
        kwargs.update(
            {
                "positive_prompt": positive_prompt,
                "negative_prompt": negative_prompt,
                "top": top,
                "right": right,
                "bottom": bottom,
                "left": left,
            }
        )
        kwargs = self._prepare_image(image, "image", kwargs)
        return self._call_api("outpaint", kwargs)
