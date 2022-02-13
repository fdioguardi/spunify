""" Constants for the credentials for the Authorization flow. """

CLIENT_ID: str = "7679e0ed5e7248a28981b3a2eb3803cb"
REDIRECT_URI: str = "http://127.0.0.1:9090"
SCOPE: list[str] | str = [
    "playlist-modify-private",
    "playlist-read-collaborative",
    "playlist-read-private",
]
