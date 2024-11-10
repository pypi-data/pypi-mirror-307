from __future__ import annotations
import time
from typing import Callable

from pprint import pformat
from pydantic import BaseModel, Field, ConfigDict

from . import api


class APIBaseModel(BaseModel):
    model_config = ConfigDict()

    def __str__(self) -> str:
        return pformat(self.model_dump(exclude_none=True))

    def __repr__(self) -> str:
        return str(self)


class Error(APIBaseModel):
    error: str


class Balance(APIBaseModel):
    balance: int


class Stat(APIBaseModel):
    date: str
    request_type: str
    charged: int


class Thumbnail(APIBaseModel):
    url: str
    width: int | None = Field(default=None)
    height: int | None = Field(default=None)


class Channel(APIBaseModel):
    id: str
    title: str
    description: str
    url: str
    banner_url: str
    comment_count: int
    subscriber_count: int
    video_count: int
    view_count: int
    thumbnails: dict[str, Thumbnail] | None = Field(default=None)


class VideoFormat(APIBaseModel):
    format: str
    cached: bool
    file_size: int | None = Field(default=None)

    def __str__(self) -> str:
        return pformat(self.model_dump(exclude_none=False))


class VideoFormats(dict[str, VideoFormat]):
    def filter(self, cached: bool):
        return {u: v for u, v in self.items() if v.cached == cached}


class DownloadResultModel(APIBaseModel):
    status: str
    file_id: str | None = Field(default=None)


class DownloadResult:
    """
    Represents the result of a video download process and provides methods
    to track the download's readiness status.
    """

    def __init__(
        self,
        result_model: DownloadResultModel,
        api: api.Api,
        video_id: str,
        video_format: str,
    ):
        """
        Initializes the DownloadResult instance.

        Args:
            r (models.DownloadResult): The raw download result from the API.
            api (Api): The Api instance used for making requests.
            video_id (str): The ID of the video being downloaded.
            video_format (str): The format of the video being downloaded.
        """
        self.result_model = result_model
        self._api: api.Api = api
        self._video_id: str = video_id
        self._format: str = video_format

    def wait_until_ready(
        self,
        delay: float = 5.0,
        callback: Callable[[DownloadResultModel], bool] | None = None,
    ) -> DownloadResultModel:
        """
        Waits until the download result is either ready or failed.

        Args:
            delay (float): Interval between polling requests in seconds. Default is 5.0.
            callback (Callable[[models.DownloadResult], bool], optional):
                      A callback function called on each iteration.
                      If it returns True, the waiting is interrupted.

        Returns:
            models.DownloadResult: The final download result when ready or failed.
        """
        if not delay or delay <= 0:
            delay = 1.0

        while True:
            r = self._api.download(self._video_id, self._format)
            if callback and callback(r):
                return r
            if r.status in ("ready", "failed"):
                return r
            time.sleep(delay)

    def __getattr__(self, name):
        # Delegate attribute access to video_model
        return getattr(self.result_model, name)


class VideoModel(APIBaseModel):
    id: str
    title: str
    description: str
    duration: str
    url: str
    published_at: str
    category_id: str | None = Field(default=None)
    channel_id: str
    channel_title: str
    channel_url: str
    comment_count: int
    like_count: int
    view_count: int
    thumbnails: dict[str, Thumbnail] | None = Field(default=None)


class Video:
    def __init__(self, api: api.Api, video_model: VideoModel) -> None:
        self._api = api
        self.video_model = video_model

    def formats(self) -> VideoFormats:
        """
        Retrieves the available formats for this video.

        Returns:
            models.VideoFormats: An object containing information about available video formats.
        """
        return self._api.video_formats(self.video_model.id)

    def download(self, video_format: str) -> DownloadResult:
        """
        Initiates a download for this video in a specified format.

        Args:
            video_format (str): The desired format for the download (e.g. 360p, 720p).

        Returns:
            DownloadResult: An object representing the download process.
        """
        return self._api.download(self.video_model.id, video_format)

    def __str__(self) -> str:
        return pformat(self.video_model)

    def __getattr__(self, name):
        # Delegate attribute access to video_model
        return getattr(self.video_model, name)

    def __repr__(self) -> str:
        return pformat(self.video_model)
