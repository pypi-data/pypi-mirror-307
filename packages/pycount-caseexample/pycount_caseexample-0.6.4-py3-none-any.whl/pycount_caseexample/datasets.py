from importlib import resources
import warnings

def get_flatland():
    """Get path to example "Flatland" [1]_ text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E. A. Abbott, "Flatland", Seeley & Co., 1884.
    """
    warnings.warn("This function will be deprecated in v1.0.0", FutureWarning)
    with resources.path("pycount_caseexample.data", "flatland.txt") as f:
        data_file_path = f
    return data_file_path

def get_zen():
    """Get path to example "Flatland" [1]_ text file.

    Returns
    -------
    pathlib.PosixPath
        Path to file.

    References
    ----------
    .. [1] E. A. Abbott, "Flatland", Seeley & Co., 1884.
    """
    with resources.path("pycount_caseexample.data", "zen.txt") as f:
        data_file_path = f
    return data_file_path