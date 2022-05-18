from pathlib import Path

_STATIC_DIR = Path(__file__).parent / 'static'
THUMBNAIL_DIRECTORY = _STATIC_DIR / 'thumbnails'


THUMBNAIL_SLUGS = {f.stem: f.relative_to(_STATIC_DIR) for f in THUMBNAIL_DIRECTORY.glob('*.*')}
DEFAULT_THUMBNAIL_SLUG = '_default'
