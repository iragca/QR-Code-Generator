"""
This module provides utility functions for file and folder operations.

Functions:
    zip_batch(folder_names):
        Compresses multiple folders into a single ZIP file.
"""

import time
import zipfile
import os
from tqdm import tqdm

def zip_batch(folder_names):
    """Compresses multiple folders into a single ZIP file.

    Args:
        zip_name (str): The name of the output ZIP file.
        folder_names (list of str): A list of folder paths to be compressed.

    Returns:
        None

    Example:
        zip_files_and_folders('archive.zip', ['folder1', 'folder2', ... foldern])
    """

    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with zipfile.ZipFile(f"batch-{timestamp}", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder in tqdm(folder_names, desc="Zipping folders"):
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file),
                                os.path.join(folder, '..')))
    except Exception as e:
        print(f"{type(e).__name__}: Error in zipping files. {e}")
