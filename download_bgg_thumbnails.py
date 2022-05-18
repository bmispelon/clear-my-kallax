"""
A script to download thumbnails from BGG
"""
import argparse
import logging
import mimetypes
import os
import re
import sys
from io import BytesIO
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

import django
import requests
from defusedxml import ElementTree
from PIL import Image

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


THING_API_ENDPOINT = 'https://boardgamegeek.com/xmlapi2/thing'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', help="The size of the thumbnail (pixels)", type=int,
                        default='200')
    parser.add_argument('--sleep', help="The delay between each download request (in seconds)",
                        type=float, default='10')
    parser.add_argument('--no-progress', help="Disable the progress bar", action="store_true")
    parser.add_argument('--directory', help="The path to the output directory", type=Path,
                        default='thumbnails')
    parser.add_argument('--skip-existing', help="Skip existing thumbnails", action='store_true')

    return parser


class BoardGameGeekAPIItem:
    def __init__(self, node):
        self.node = node

    @property
    def bgg_id(self):
        return self.node.attrib['id']

    @property
    def image_url(self):
        return self.node.find('image').text.strip()

    @classmethod
    def from_response(cls, response):
        """
        Return a list of items from the given XML response
        """
        tree = ElementTree.fromstring(response.content)
        return [cls(node) for node in tree.findall('item')]


def get_fullsize_image_urls_for_games(ids):
    """
    Retrieve the image URLs for the games with the given ids.
    """
    params = {'type': 'boardgame,boardgameexpansion', 'id': ','.join(ids)}
    response = requests.get(THING_API_ENDPOINT, params=params)
    response.raise_for_status()
    items = BoardGameGeekAPIItem.from_response(response)
    return {item.bgg_id: item.image_url for item in items}


def get_bgg_id(game):
    path_regex = re.compile('^/boardgame(expansion)?/(?P<id>[^/]+)/')
    for link in game.links:
        _, netloc, path, _, _, _ = urlparse(link)
        if netloc != 'boardgamegeek.com':
            continue
        if (match := path_regex.search(path)) is None:
            logging.debug(f"URL path {path!r} for game {game.title} is not parseable")
            continue
        return match['id']

    return None


def download_fullsize_game_image(game, image_url, timeout=10):
    logging.debug(f"Downloading image for game {game.title} at URL {image_url!r}")
    response = requests.get(image_url, timeout=timeout)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)), response.headers['Content-Type']


def get_games(options):
    from games.models import \
        Game  # to make sure Django is ready before models are imported
    return Game.objects.all()  # TODO: take options.skip_existing into account


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clearmykallax.settings')
    django.setup()
    logging.basicConfig(level=logging.DEBUG)

    options = get_parser().parse_args()

    if not options.no_progress and tqdm is None:
        print("The tqdm library is not installed. "
              "Either install it with `pip install tqdm` or pass --no-progress to this script.")
        sys.exit(1)

    games_with_id = {}
    for game in get_games(options):
        if (bgg_id := get_bgg_id(game)) is None:
            continue
        if bgg_id in games_with_id:
            duplicate = games_with_id[bgg_id]
            logging.debug(f"Duplicate BGG id detected for games {game.title} and {duplicate.title}")

        games_with_id[bgg_id] = game

    image_urls = get_fullsize_image_urls_for_games(games_with_id.keys())

    if options.no_progress:
        data = games_with_id.items()
    else:
        data = tqdm(games_with_id.items())

    if options.skip_existing:
        existing_slugs = {f.stem for f in options.directory.iterdir() if f.is_file()}
    else:
        existing_slugs = set()

    for bgg_id, game in data:
        if game.slug in existing_slugs:
            logging.debug(f"Skipping existing slug {game.slug}")
            continue

        image_url = image_urls[bgg_id]
        image, contenttype = download_fullsize_game_image(game, image_url)
        image.thumbnail((options.size, options.size))
        extension = mimetypes.guess_extension(contenttype) or '.bin'
        filename = options.directory / f"{game.slug}{extension}"
        image.save(filename)
        logging.info(f"Saved thumbnail at {filename}")
        sleep(options.sleep)
