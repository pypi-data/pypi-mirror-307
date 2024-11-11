import re
from pathlib import Path
from typing import Callable


class FolderBasedAttrsError(Exception):
    """Custom exception for folder-related errors"""
    pass


def load_class_attrs_from_folder[T](folder: str | Path, target: T, banterml_parser: Callable[[str], list[dict[str, str]]]) -> None:
    match folder:
        case None:
            raise FolderBasedAttrsError("Folder name must be a non-empty string")
        case str():
            folder = Path(folder)

    if not folder.exists():
        raise FolderBasedAttrsError(f"Folder not found: {folder}")
    loaded_files = False

    # Load all .txt and .xml files
    for file_path in folder.iterdir():
        if not file_path.is_file() or file_path.name.startswith('.'):
            continue

        if file_path.suffix not in ['.txt', '.banterml']:
            continue

        attr_name = file_path.stem  # filename without extension

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not _is_valid_content(content, file_path):
                raise FolderBasedAttrsError(
                    f"Invalid or empty content in file: {file_path}"
                )

            if file_path.suffix == '.banterml':
                content = banterml_parser(content)

            setattr(target, attr_name, content)
            loaded_files = True

        except (IOError, UnicodeDecodeError) as e:
            raise FolderBasedAttrsError(
                f"Error reading file {file_path}: {str(e)}"
            ) from e

    if not loaded_files:
        raise FolderBasedAttrsError(
            f"No valid files found in {folder}"
        )


def _is_valid_content(content: str, file_path: Path) -> bool:
    """Basic content validation"""
    if not content.strip():
        return False

    if file_path.suffix == '.xml':
        # Check for basic XML-like structure
        return bool(re.search(r'<\w+>.*?</\w+>', content, re.DOTALL))

    return True
