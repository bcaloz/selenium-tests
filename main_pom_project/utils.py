import os


def get_test_file_path(filename: str, test_file: str) -> tuple[str, str]:
    """
    Return full file path and filename for a file in the test_data directory.
    """
    base_dir = os.path.dirname(os.path.abspath(test_file))
    file_path = os.path.abspath(os.path.join(base_dir, "..", "test_data", filename))
    return file_path, os.path.basename(file_path)
