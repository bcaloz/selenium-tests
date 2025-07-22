import os


def get_test_file_path(target_filename: str, calling_file_path: str) -> tuple[str, str]:
    """
    Return full file path and filename for a file in the test_data directory.

    Parameters:
    - target_filename: name of the file to resolve (e.g., 'sample_upload.txt')
    - calling_file_path: typically __file__, used to resolve relative location

    Returns:
    - Tuple of (full_path, filename_only)
    """
    base_dir = os.path.dirname(os.path.abspath(calling_file_path))
    full_path = os.path.abspath(
        os.path.join(base_dir, "..", "test_data", target_filename)
    )
    return full_path, os.path.basename(full_path)
