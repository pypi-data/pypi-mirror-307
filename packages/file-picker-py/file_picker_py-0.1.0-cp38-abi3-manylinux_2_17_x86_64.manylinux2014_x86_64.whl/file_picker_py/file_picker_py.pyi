from typing import Optional, List

def pick_file_blocking() -> Optional[str]:
    """Pick a single file using a native file dialog.

    Returns:
        Optional[str]: Path of the selected file, or None if dialog was cancelled
    """
    ...

def pick_files_blocking() -> List[str]:
    """Pick multiple files using a native file dialog.

    Returns:
        List[str]: List of selected file paths, empty if dialog was cancelled
    """
    ...

def pick_folder_blocking() -> Optional[str]:
    """Pick a single folder using a native file dialog.

    Returns:
        Optional[str]: Path of the selected folder, or None if dialog was cancelled
    """
    ...

def pick_folders_blocking() -> List[str]:
    """Pick multiple folders using a native file dialog.

    Returns:
        List[str]: List of selected folder paths, empty if dialog was cancelled
    """
    ...

def pick_save_file_blocking() -> Optional[str]:
    """Pick a save file location using a native file dialog.

    Returns:
        Optional[str]: Path of the selected save location, or None if dialog was cancelled
    """
    ...