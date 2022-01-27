import logging
from typing import Generator, Iterable

import spotipy
from spotipy.cache_handler import CacheFileHandler

from credentials import CLIENT_ID, REDIRECT_URI, SCOPE
import utils


class SpotifyAdapter(spotipy.Spotify):
    """A wrapper for the Spotify API."""

    def __init__(self, client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE):
        """
        Initialize the SpotifyAdapter.

        :param: client_id: The client ID.
        :param: redirect_uri: The redirect URI.
        :param: scope: The permissions to be requested.
        """
        auth_manager = spotipy.SpotifyPKCE(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_handler=CacheFileHandler(cache_path=utils.get_cache_path()),
        )
        super().__init__(auth_manager=auth_manager)

    def playlist_uri(self, id: str) -> str:
        """
        Get the Spotify playlist ID from a Spotify ID, URI, or URL.
        """
        return super()._get_uri(type="playlist", id=id)

    def playlist_add_items(self, playlist_id: str, items: Iterable[str]) -> None:
        """
        Add items to a Spotify playlist.

        :param: playlist_id: The Spotify playlist ID.
        :param: items: The items to add.
        """
        for batch in utils.chunks(items, size=100):
            super().playlist_add_items(playlist_id, items=batch)
            logging.debug(f"Added batch of {len(batch)} items to {playlist_id}")

    def public_playlist_items(self, playlist_id: str, *args, **kwargs) -> list[str]:
        """
        Get the public (non local) tracks and episodes of a playlist.

        :param playlist_id: The ID, URI, or URL of the playlist.
        :return: The public items of the playlist.
        """
        items = [
            item["track"]["uri"]
            for item in self.playlist_items(playlist_id, *args, **kwargs)
            if not item["track"]["is_local"]
        ]

        logging.info(f"Found {len(items)} items in {playlist_id}")
        return items

    def playlist_items(
        self, playlist_id: str, *args, **kwargs
    ) -> Generator[dict, None, None]:
        """
        Get the tracks and episodes of a playlist.

        :param playlist_id: The ID, URI, or URL of the playlist.
        :return: The items of the playlist.
        """
        results = super().playlist_items(playlist_id, *args, **kwargs)
        while isinstance(results, dict):
            yield from results["items"]
            results = self.next(results)
