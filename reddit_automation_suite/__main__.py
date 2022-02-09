import logging
from .loader import RedditAssitant


logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)

if __name__ == "__main__":
    # Intialize
    assistant = RedditAssitant()
    assistant.stream_subreddit()
