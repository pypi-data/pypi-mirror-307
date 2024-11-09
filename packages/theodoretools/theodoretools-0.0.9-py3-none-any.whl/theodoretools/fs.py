import os


def list_subdirectories(path: str, reverse: bool = True):
    try:
        subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        subdirs.sort(reverse=reverse)
        return subdirs
    except FileNotFoundError:
        return []


def get_directory_size(directory: str, exclude_extensions=[]):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            if any(f.endswith(ext) for ext in exclude_extensions):
                continue
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    total_size_mb = total_size / (1024 * 1024)

    total_size_mb = round(total_size_mb, 2)

    return total_size_mb
