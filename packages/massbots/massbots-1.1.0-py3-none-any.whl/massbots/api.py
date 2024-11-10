"""Realisation of Api class"""

from __future__ import annotations

import requests

from . import models
from .error import ApiError


class Api:
    """
    The `Api` class provides methods to interact with the massbots.xyz API,
    allowing you to retrieve information about videos,channels, perform searches,
    and manage downloads.
    """

    base_url: str = "https://api.massbots.xyz"
    request_timeout = 300

    def __init__(self, token: str, bot_id: str | None = None):
        """
        Initializes the Api instance with the provided token and optional bot_id.

        Args:
            token (str): The API token for authentication.
            bot_id (str | None): An optional bot ID for bot-specific API calls.
        """
        self._token = token
        self._bot_id = bot_id

    def balance(self) -> int:
        """
        Retrieves the balance of the authenticated account.

        Returns:
            int: The balance of the account.
        """
        data: dict = self._query_api(f"{self.base_url}/me/balance")
        return models.Balance.model_validate(data).balance
    
    def stats(self) -> list[models.Stat]:
        """
        Fetches the stats of the user
        """
        data: dict = self._query_api(f"{self.base_url}/me/stats")
        return [models.Stat.model_validate(stat) for stat in data]

    def video_formats(self, video_id: str) -> models.VideoFormats:
        """
        Fetches available video formats for a given video ID.

        Args:
            video_id (str): The ID of the video.

        Returns:
            models.VideoFormats: An object containing information about available video formats.
        """
        data: dict = self._query_api(f"{self.base_url}/video/{video_id}/formats")
        formats: models.VideoFormats = models.VideoFormats()
        for fmt_name, fmt_info in data.items():
            formats[fmt_name] = models.VideoFormat.model_validate(fmt_info)
        return formats

    def channel(self, channel_id: str) -> models.Channel:
        """
        Retrieves information about a specific channel.

        Args:
            channel_id (str): The ID of the channel.

        Returns:
            models.CustomChannel: An object containing the channel information.
        """
        data: dict = self._query_api(f"{self.base_url}/channel/{channel_id}")
        return models.Channel.model_validate(data)

    def search(self, query: str, kind: str = "video") -> list[models.Video] | list[models.Channel]:
        """
        Searches for videos or channel based on a query string and kind of results.

        Args:
            query (str): The search query.
            kind (str): The type of results to retrieve ("video" or "channel").

        Returns:
            list: a list of videos or channels
        """
        match kind:
            case "video":
                data = self._query_api(f"{self.base_url}/search?q={query}&kind={kind}")
                videos = [models.VideoModel.model_validate(video_data) for video_data in data]
                return [models.Video(self, video) for video in videos]
            case "channel":
                data = self._query_api(f"{self.base_url}/search?q={query}&kind={kind}")
                return [models.Channel.model_validate(channel_data) for channel_data in data]
            case _:
                raise ValueError(f"Invalid kind for search: {kind}")

    def video(self, video_id: str) -> models.Video:
        """
        Retrieves details about a specific video.

        Args:
            video_id (str): The ID of the video.

        Returns:
            Video: A Video object containing the video's details.
        """
        data = self._query_api(f"{self.base_url}/video/{video_id}")
        video_model = models.VideoModel.model_validate(data)
        return models.Video(self, video_model)

    def download(self, video_id: str, video_format: str) -> models.DownloadResult:
        """
        Initiates a download for a video in a specified format.

        Args:
            video_id (str): The ID of the video.
            video_format (str): The desired format for the download (e.g. 360p, 720p).

        Returns:
            DownloadResult: A DownloadResult object to track the download progress.
        """
        data = self._query_api(
            f"{self.base_url}/video/{video_id}/download/{video_format}"
        )
        r = models.DownloadResultModel.model_validate(data)
        return models.DownloadResult(r, self, video_id, video_format)

    def _query_api(self, url: str) -> dict:
        """
        Internal method to send a GET request to the specified API URL.

        Args:
            url (str): The API endpoint URL.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ApiError: If the API response status code is not 200.
        """
        headers = {"X-Token": f"{self._token}"}
        if self._bot_id is not None:
            headers["X-Bot-Id"] = self._bot_id

        response = self._get_request(url, headers=headers)
        if response.status_code != requests.codes.ok:
            raise ApiError(status=response.status_code, data=response.json())

        return response.json()

    @classmethod
    def _get_request(cls, *args, **kwargs):
        """
        A static method to perform a GET request using the requests library.

        Returns:
            requests.Response: The response object.
        """
        return requests.get(*args, **kwargs, timeout=cls.request_timeout)
