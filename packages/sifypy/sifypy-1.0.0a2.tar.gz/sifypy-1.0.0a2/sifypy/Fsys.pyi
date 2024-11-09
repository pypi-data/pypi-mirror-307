from ._typing.typing import String

def getfilesize(base_dir: String = ".", filename: String = "") -> int | None:
    """Get the size of a file in bytes."""
    ...
    
def getdir(base_dir: String = ".", filter_extension=None, filter_name=None) -> list:
    """List files in a directory with optional filters for extensions or names."""
    ...

