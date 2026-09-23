from pathlib import Path

def get_asset(file_name: str) -> str:
    """Returns the absolute path to a resource file inside the assests folder."""
    assets_folder = Path(__file__).parent.resolve() / "assests"
    return str(assets_folder / file_name)