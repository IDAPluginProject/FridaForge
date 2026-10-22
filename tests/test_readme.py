import re
from pathlib import Path

README = (Path(__file__).resolve().parent.parent / "README.md").read_text(encoding="utf-8")
RAW_ASSETS = "https://raw.githubusercontent.com/noobexon1/FridaForge/main/assets/"


def _image_sources() -> list[str]:
    markdown = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", README)
    html = re.findall(r'<img[^>]*src="([^"]+)"', README)
    return markdown + html


def test_local_images_use_absolute_raw_urls():
    local = [s for s in _image_sources() if "img.shields.io" not in s]
    assert local
    assert [s for s in local if not s.startswith(RAW_ASSETS)] == []


def test_binary_ninja_section_mentions_extension_manager():
    assert "Extension Manager" in README
