""" Merge spotify playlists. """

import argparse
import logging

from playlist import Playlist


def spunify(destination_playlist: str, source_playlists: set[str]):
    """
    Merge the source playlists into the destination playlist.

    :param destination_playlist: The url of the playlist where the
        tracks will be merged.
    :param source_playlists: The urls of the playlists to be merged
        into the destination.
    """
    logging.info(f"Merging {source_playlists} into {destination_playlist}.")

    destination: Playlist = Playlist(destination_playlist)
    for source in source_playlists:
        destination += Playlist(source)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge spotify playlists",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.INFO,
        help="Increase verbosity",
    )
    group.add_argument(
        "-vv",
        "--very-verbose",
        action="store_const",
        const=logging.DEBUG,
        help="Increase verbosity further",
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="The ID, URI, or URL of the playlist where the tracks will be merged",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-s",
        "--sources",
        help="The URLs, URIs, or IDs of the playlists to be merged into the destination",
        nargs="+",
        required=True,
        type=str,
    )

    return parser.parse_args()


def main():
    """Main function."""

    args = parse_args()

    logging.basicConfig(
        level=args.verbose or args.very_verbose or logging.WARNING,
        format=f"%(asctime)s [%(module)s]: %(message)s",
        datefmt="%I:%M:%S %p",
    )

    spunify(args.destination, set(args.sources))


if __name__ == "__main__":
    main()
