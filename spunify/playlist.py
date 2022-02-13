from __future__ import annotations
import logging
import logging.config

from adapter import SpotifyAdapter

spotify: SpotifyAdapter = SpotifyAdapter()


class Playlist:
    """
    Class to represent a playlist.

    Attributes:
        uri (str): The URI of the playlist.
        tracks (set): Set of tracks in the playlist.
    """

    def __init__(self, id: str):
        """
        Initialize a playlist.

        :param id: The ID, URI, or URL of the playlist.
        """
        self.uri = spotify.playlist_uri(id)

        logging.debug(f"Creating playlist: {self}")

    def __repr__(self):
        """Return a readable representation of the playlist."""
        return f"{self.__class__.__qualname__}({self.uri=})"

    @property
    def items(self) -> set:
        """Get the public items in the playlist."""

        if not hasattr(self, "_items"):
            logging.debug(f"Getting items for playlist: {self}")
            self._items = set(spotify.public_playlist_items(playlist_id=self.uri))

        return self._items

    def __iadd__(self, other: Playlist) -> Playlist:
        """
        Add the tracks/episodes of `other` into `self`.

        :param other: The playlist to be added.
        :return: This playlist with the added items.
        """
        if not isinstance(other, Playlist):
            raise TypeError(
                "unsupported operand type(s) for +=: "
                f"'{self.__class__.__qualname__}' and "
                f"'{other.__class__.__qualname__}'"
            )

        items: list[str] = list(other.items - self.items)
        logging.info(f"Adding {len(items)} items from {other} to {self}")

        spotify.playlist_add_items(playlist_id=self.uri, items=items)
        return self
