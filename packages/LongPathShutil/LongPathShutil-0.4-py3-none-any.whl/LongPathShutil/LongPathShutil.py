import shutil
import os
from pathlib import Path
from typing import IO, Callable, List, Optional, Tuple, Union
import winreg

def enable_long_paths_on_registry():
    """
    Enables long path support in Windows by modifying the Windows registry.
    This requires administrative privileges and does not always work.
    """
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\\CurrentControlSet\\Control\\FileSystem",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)

def disable_long_paths_on_registry():
    """
    Disables long path support in Windows by modifying the Windows registry.
    This requires administrative privileges.
    """
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\\CurrentControlSet\\Control\\FileSystem",
        0,
        winreg.KEY_WRITE,
    )
    winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)
    return True

def is_long_paths_enabled_on_registry():
    """
    Checks if long path support is enabled in Windows.

    Returns:
        bool: True if long paths are enabled, False otherwise.
    """
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\\CurrentControlSet\\Control\\FileSystem",
        0,
        winreg.KEY_READ,
    )
    value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
    winreg.CloseKey(key)
    return value == 1

def add_long_path_prefix(path: Union[str, Path]) -> str:
    """
    Adds the \\?\ prefix to a path if it isn't already present.

    Args:
        path (Union[str, Path]): The path to add the prefix to.

    Returns:
        str: The path with the \\?\ prefix added, if applicable.
    """
    prefix = "\\\\?\\"
    unc_prefix = "\\\\?\\UNC\\"
    path = Path(path)

    if os.name == "nt":
        path_str = str(path)
        
        if not path.is_absolute():
            path = path.resolve()
            path_str = str(path)

        if path_str.startswith("\\\\"):
            if not path_str.startswith(unc_prefix):
                return unc_prefix + path_str[2:]
        else:
            if not path_str.startswith(prefix):
                return prefix + path_str

    return path

def copyfileobj(fsrc: IO[bytes], fdst: IO[bytes], length: int = 16 * 1024) -> None:
    """
    Copies the contents of one file object to another.

    Args:
        fsrc (IO[bytes]): Source file object.
        fdst (IO[bytes]): Destination file object.
        length (int, optional): Number of bytes per read. Defaults to 16 * 1024.
    """
    return shutil.copyfileobj(fsrc, fdst, length)

def copyfile(
    src: Union[str, Path], dst: Union[str, Path], *, follow_symlinks: bool = True
) -> str:
    """
    Copies the contents of a file to another file.

    Args:
        src (Union[str, Path]): Source file path.
        dst (Union[str, Path]): Destination file path.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.

    Returns:
        str: The destination file path.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    return shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)

def copymode(
    src: Union[str, Path], dst: Union[str, Path], *, follow_symlinks: bool = True
) -> None:
    """
    Copies the permission bits from the source to the destination.

    Args:
        src (Union[str, Path]): Source file path.
        dst (Union[str, Path]): Destination file path.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    shutil.copymode(src, dst, follow_symlinks=follow_symlinks)

def copystat(
    src: Union[str, Path], dst: Union[str, Path], *, follow_symlinks: bool = True
) -> None:
    """
    Copies the metadata from the source to the destination.

    Args:
        src (Union[str, Path]): Source file path.
        dst (Union[str, Path]): Destination file path.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    shutil.copystat(src, dst, follow_symlinks=follow_symlinks)

def copy(
    src: Union[str, Path], dst: Union[str, Path], *, follow_symlinks: bool = True
) -> str:
    """
    Copies a file to another location, preserving metadata.

    Args:
        src (Union[str, Path]): Source file path.
        dst (Union[str, Path]): Destination file path.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.

    Returns:
        str: The destination file path.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    return shutil.copy(src, dst, follow_symlinks=follow_symlinks)

def copy2(
    src: Union[str, Path], dst: Union[str, Path], *, follow_symlinks: bool = True
) -> str:
    """
    Copies a file to another location, preserving metadata.

    Args:
        src (Union[str, Path]): Source file path.
        dst (Union[str, Path]): Destination file path.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.

    Returns:
        str: The destination file path.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

def copytree(
    src: Union[str, Path],
    dst: Union[str, Path],
    symlinks: bool = False,
    ignore: Optional[Callable[[str, List[str]], List[str]]] = None,
    copy_function: Callable[
        [Union[str, Path], Union[str, Path]], str
    ] = shutil.copy2,
    ignore_dangling_symlinks: bool = False,
    dirs_exist_ok: bool = False,
) -> str:
    """
    Recursively copy an entire directory tree rooted at src to a directory named dst.

    Args:
        src (Union[str, Path]): Source directory.
        dst (Union[str, Path]): Destination directory.
        symlinks (bool, optional): Whether to copy symlinks. Defaults to False.
        ignore (Optional[Callable[[str, List[str]], List[str]]], optional): Ignore function. Defaults to None.
        copy_function (Callable, optional): Copy function to use. Defaults to shutil.copy2.
        ignore_dangling_symlinks (bool, optional): Ignore dangling symlinks. Defaults to False.
        dirs_exist_ok (bool, optional): Whether destination directory can already exist. Defaults to False.

    Returns:
        str: Destination directory path.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    return shutil.copytree(
        src,
        dst,
        symlinks=symlinks,
        ignore=ignore,
        copy_function=copy_function,
        ignore_dangling_symlinks=ignore_dangling_symlinks,
        dirs_exist_ok=dirs_exist_ok,
    )

def move(
    src: Union[str, Path],
    dst: Union[str, Path],
    copy_function: Callable[
        [Union[str, Path], Union[str, Path]], str
    ] = shutil.copy2,
) -> str:
    """
    Moves a file or directory to another location.

    Args:
        src (Union[str, Path]): Source file or directory.
        dst (Union[str, Path]): Destination path.
        copy_function (Callable, optional): Copy function to use. Defaults to shutil.copy2.

    Returns:
        str: Destination path.
    """
    src = add_long_path_prefix(src)
    dst = add_long_path_prefix(dst)
    return shutil.move(src, dst, copy_function=copy_function)

def rmtree(
    path: Union[str, Path],
    ignore_errors: bool = False,
    onerror: Optional[Callable[[Callable, str, Tuple[int, int]], None]] = None,
    onexc: Optional[Callable[[Callable, str, BaseException], None]] = None,
    dir_fd: Optional[int] = None,
) -> None:
    """
    Removes a directory tree.

    Args:
        path (Union[str, Path]): Path to the directory tree to be removed.
        ignore_errors (bool, optional): Ignore errors during removal. Defaults to False.
        onerror (Optional[Callable], optional): Error handling callback. Defaults to None.
        onexc (Optional[Callable], optional): Exception handling callback. Defaults to None.
        dir_fd (Optional[int], optional): Directory file descriptor. Defaults to None.
    """
    path = add_long_path_prefix(path)
    shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror, onexc=onexc, dir_fd=dir_fd)

rmtree.avoids_symlink_attacks = shutil.rmtree.avoids_symlink_attacks

def disk_usage(path: Union[str, Path]) -> shutil._ntuple_diskusage:
    """
    Returns disk usage statistics about the given path.

    Args:
        path (Union[str, Path]): Path for which to check disk usage.

    Returns:
        shutil._ntuple_diskusage: Disk usage statistics.
    """
    path = add_long_path_prefix(path)
    return shutil.disk_usage(path)

def chown(
    path: Union[str, Path],
    user: Optional[Union[int, str]] = None,
    group: Optional[Union[int, str]] = None,
    dir_fd: Optional[int] = None,
    follow_symlinks: bool = True,
) -> None:
    """
    Changes the owner and group of a file.

    Args:
        path (Union[str, Path]): Path to the file.
        user (Optional[Union[int, str]], optional): New user owner. Defaults to None.
        group (Optional[Union[int, str]], optional): New group owner. Defaults to None.
        dir_fd (Optional[int], optional): A directory file descriptor. Defaults to None.
        follow_symlinks (bool, optional): Whether to follow symlinks. Defaults to True.
    """
    path = add_long_path_prefix(path)
    shutil.chown(path, user=user, group=group, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

def which(
    cmd: str, mode: int = os.F_OK | os.X_OK, path: Optional[str] = None
) -> Optional[str]:
    """
    Returns the path to an executable which would have been run if the given cmd was called.

    Args:
        cmd (str): Command to check.
        mode (int, optional): Accessibility check mode. Defaults to os.F_OK | os.X_OK.
        path (Optional[str], optional): PATH environment variable to use. Defaults to None.

    Returns:
        Optional[str]: Path to the executable, or None if not found.
    """
    return shutil.which(cmd, mode=mode, path=path)

def get_archive_formats() -> List[Tuple[str, str]]:
    """
    Returns a list of supported archive formats.

    Returns:
        List[Tuple[str, str]]: List of (format_name, description) tuples.
    """
    return shutil.get_archive_formats()

def register_archive_format(
    name: str,
    function: Callable,
    extra_args: Optional[List] = None,
    description: str = "",
) -> None:
    """
    Registers an archive format.

    Args:
        name (str): Format name.
        function (Callable): Function to create an archive.
        extra_args (Optional[List], optional): Extra arguments for the archive creation function. Defaults to None.
        description (str, optional): Format description. Defaults to ''.
    """
    shutil.register_archive_format(
        name, function, extra_args=extra_args, description=description
    )

def unregister_archive_format(name: str) -> None:
    """
    Unregisters an archive format.

    Args:
        name (str): Format name to unregister.
    """
    shutil.unregister_archive_format(name)

def make_archive(
    base_name: Union[str, Path],
    format: str,
    root_dir: Optional[Union[str, Path]] = None,
    base_dir: Optional[Union[str, Path]] = None,
    verbose: int = 0,
    dry_run: bool = False,
    owner: Optional[Union[int, str]] = None,
    group: Optional[Union[int, str]] = None,
    logger: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Creates an archive file.

    Args:
        base_name (Union[str, Path]): Archive file name without extension.
        format (str): Archive format.
        root_dir (Optional[Union[str, Path]], optional): Root directory of the archive. Defaults to None.
        base_dir (Optional[Union[str, Path]], optional): Base directory inside the archive. Defaults to None.
        verbose (int, optional): Verbosity level. Defaults to 0.
        dry_run (bool, optional): Perform a dry run. Defaults to False.
        owner (Optional[Union[int, str]], optional): Owner to set. Defaults to None.
        group (Optional[Union[int, str]], optional): Group to set. Defaults to None.
        logger (Optional[Callable[[str], None]], optional): Logger function. Defaults to None.

    Returns:
        str: Path to the created archive file.
    """
    base_name = add_long_path_prefix(base_name)
    if root_dir:
        root_dir = add_long_path_prefix(root_dir)
    if base_dir:
        base_dir = add_long_path_prefix(base_dir)
    return shutil.make_archive(
        base_name,
        format,
        root_dir=root_dir,
        base_dir=base_dir,
        verbose=verbose,
        dry_run=dry_run,
        owner=owner,
        group=group,
        logger=logger,
    )

def get_unpack_formats() -> List[Tuple[str, List[str], str]]:
    """
    Returns a list of supported unpack formats.

    Returns:
        List[Tuple[str, List[str], str]]: List of (format_name, extensions, description) tuples.
    """
    return shutil.get_unpack_formats()

def register_unpack_format(
    name: str,
    extensions: List[str],
    function: Callable,
    extra_args: Optional[List] = None,
    description: str = "",
) -> None:
    """
    Registers an unpack format.

    Args:
        name (str): Format name.
        extensions (List[str]): List of supported extensions.
        function (Callable): Function to extract the archive.
        extra_args (Optional[List], optional): Extra arguments for the extraction function. Defaults to None.
        description (str, optional): Format description. Defaults to ''.
    """
    shutil.register_unpack_format(
        name, extensions, function, extra_args=extra_args, description=description
    )

def unregister_unpack_format(name: str) -> None:
    """
    Unregisters an unpack format.

    Args:
        name (str): Format name to unregister.
    """
    shutil.unregister_unpack_format(name)

def unpack_archive(
    filename: Union[str, Path],
    extract_dir: Optional[Union[str, Path]] = None,
    format: Optional[str] = None,
    filter: Optional[str] = None,
) -> None:
    """
    Unpacks an archive.

    Args:
        filename (Union[str, Path]): Archive file path.
        extract_dir (Optional[Union[str, Path]], optional): Directory to extract to. Defaults to None.
        format (Optional[str], optional): Archive format. Defaults to None.
        filter (Optional[str], optional): Extraction filter for archive files. Defaults to None.
    """
    filename = add_long_path_prefix(filename)
    if extract_dir:
        extract_dir = add_long_path_prefix(extract_dir)
    shutil.unpack_archive(filename, extract_dir=extract_dir, format=format, filter=filter)

def ignore_patterns(*patterns: str) -> Callable[[str, List[str]], List[str]]:
    """
    Returns a callable that ignores files matching the given patterns.

    Args:
        patterns (str): Patterns to ignore.

    Returns:
        Callable[[str, List[str]], List[str]]: A callable that can be passed to ignore parameter of copytree.
    """
    return shutil.ignore_patterns(*patterns)

def get_terminal_size(fallback: Tuple[int, int] = (80, 24)) -> os.terminal_size:
    """
    Returns the terminal size in characters.

    Args:
        fallback (Tuple[int, int], optional): Fallback size if terminal size cannot be determined. Defaults to (80, 24).

    Returns:
        os.terminal_size: Named tuple with terminal width and height.
    """
    return shutil.get_terminal_size(fallback=fallback)
