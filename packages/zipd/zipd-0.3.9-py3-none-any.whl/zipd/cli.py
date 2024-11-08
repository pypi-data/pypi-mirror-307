"""Command-line interface for zipd."""

from __future__ import absolute_import, print_function

import argparse
import os
import os.path
import subprocess
import sys

import gitignore_parser

from zipd import argparsing, get_version, runcommand

DESCRIPTION_TEMPLATE = """
Recursively zip up a directory/folder into a zipfile.

The resulting zipfile will be named FOLDER.zip and placed in the current
directory.  This uses the 'zip' command to perform much of its work.
"""

EPILOG_TEMPLATE = """
To pass additional arguments to 'zip', add '--' and the arguments to the end
of the command line.  For example, to exclude entries for directories/folders
from the zip archive:

    {prog} my-folder -- -D
"""

STATUS_HELP = 42

FILTER_INCLUDE_ALL = "all"
FILTER_INCLUDE_SOME = "some"
FILTER_INCLUDE_GITIGNORE = "gitignore"
FILTER_INCLUDE_GIT = "git"
FILTER_INCLUDE_DEFAULT = FILTER_INCLUDE_SOME
FILTER_INCLUDES_USING_GITIGNORE = {FILTER_INCLUDE_GIT, FILTER_INCLUDE_GITIGNORE}

CREATE_METHOD_BACKUP = "backup"
CREATE_METHOD_KEEP = "keep"
CREATE_METHOD_OVERWRITE = "overwrite"
CREATE_METHOD_DEFAULT = CREATE_METHOD_BACKUP

ZIP_COMMAND = "zip"
ZIP_SUFFIX = ".zip"

BACKUP_SUFFIX = ".old" if sys.platform.startswith("win") else "~"

FILTER_PATHS_SOME = {".cvs", ".svn", ".git"}
FILTER_PATHS_GITIGNORE = {".git"}

GITIGNORE_BASENAME = ".gitignore"


def _is_root_dir(path):
    return os.path.realpath(path) in {os.path.sep, "/"}


def _handle_root_dir(path, force):
    if force:
        zipfile_path = "".join(["ROOT_DIRECTORY", ZIP_SUFFIX])
    else:
        raise RuntimeError(
            (
                "To zip up {path} and all its subdirectories, "
                "use the '--force' option"
            ).format(path=path)
        )
    return zipfile_path


def _infer_zipfile_path(path, force):
    if _is_root_dir(path):
        zipfile_path = _handle_root_dir(path, force)
    else:
        zipfile_path = os.path.basename(path) + ZIP_SUFFIX
    zipfile_path = os.path.join(os.path.curdir, zipfile_path)
    return zipfile_path


def _infer_backup_path(path):
    return "".join([path, BACKUP_SUFFIX])


def _add_arguments(argparser):
    group_filtering = argparser.add_argument_group(title="filtering arguments")
    mutex_group_include = group_filtering.add_mutually_exclusive_group()
    mutex_group_include.add_argument(
        "-a",
        "--all",
        dest="include",
        action="store_const",
        const=FILTER_INCLUDE_ALL,
        default=FILTER_INCLUDE_DEFAULT,
        help=(
            "Include all files/folders in the resulting zipfile "
            "(default: exclude some folders used by revision control systems "
            "such as Git, Subversion, or CVS)."
        ),
    )
    mutex_group_include.add_argument(
        "-g",
        "--gitignore",
        dest="include",
        action="store_const",
        const=FILTER_INCLUDE_GITIGNORE,
        help=(
            "If a '{gitignore}' file exists in FOLDER, use it to determine "
            "what to include in or exclude from the resulting zipfile "
            "(if a '.git' folder exists, it will be excluded)."
        ).format(gitignore=GITIGNORE_BASENAME),
    )
    mutex_group_include.add_argument(
        "-G",
        "--git",
        dest="include",
        action="store_const",
        const=FILTER_INCLUDE_GIT,
        help=(
            "Like '--gitignore', but if a '.git' folder exists in FOLDER, "
            "include it in the resulting zipfile as well."
        ),
    )
    group_zipfile = argparser.add_argument_group(title="zipfile arguments")
    group_zipfile.add_argument(
        "-o",
        "--output",
        dest="output",
        metavar="ZIPFILE",
        action="store",
        default=None,
        help=(
            "Store the resulting zip archive in ZIPFILE (default: {default})."
        ).format(default=_infer_zipfile_path("FOLDER", force=False)),
    )
    group_zipfile.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        default=False,
        help="if FOLDER is '/', go ahead and zip it up anyway.",
    )
    mutex_group_create_method = group_zipfile.add_mutually_exclusive_group()
    mutex_group_create_method.add_argument(
        "-k",
        "--keep",
        dest="create_method",
        action="store_const",
        const=CREATE_METHOD_KEEP,
        default=CREATE_METHOD_DEFAULT,
        help=(
            "Keep and reuse a preexisting zipfile "
            "(default: backup a preexisting zipfile "
            "and create a fresh one)."
        ),
    )
    mutex_group_create_method.add_argument(
        "--overwrite",
        dest="create_method",
        action="store_const",
        const=CREATE_METHOD_OVERWRITE,
        help=(
            "Remove and overwrite a preexisting zipfile "
            "(default: backup a preexisting zipfile "
            "and create a fresh one)."
        ),
    )
    argparsing.add_dry_run_argument(argparser)
    argparser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s v{version}".format(version=get_version()),
    )
    argparser.add_argument(
        "folder", metavar="FOLDER", nargs="?", default=None, help="folder to zip up"
    )
    argparser.add_argument(
        "more_options",
        metavar="...",
        nargs=argparse.REMAINDER,
        help="arguments to pass to 'zip', if any",
    )
    return argparser


def _normalize_path(path):
    path = os.path.normcase(os.path.normpath(path))
    return path


def _dir_exists(path, should_raise=False):
    if not os.path.exists(path):
        if should_raise:
            raise FileNotFoundError("path not found: {path}".format(path=path))
        return False
    if not os.path.isdir(path):
        if should_raise:
            raise NotADirectoryError("not a directory: {path}".format(path=path))
        return False
    return True


def _file_exists(path, should_raise=False):
    if not os.path.exists(path):
        if should_raise:
            raise FileNotFoundError("path not found: {path}".format(path=path))
        return False
    if not os.path.isfile(path):
        if should_raise:
            message = "not a regular file: {path}".format(path=path)
            if os.path.isdir(path):
                raise IsADirectoryError(message)
            raise IOError(message)
        return False
    return True


def _remove_file(path, dry_run, show_trace=True):
    if dry_run:
        runcommand.print_message("Would do:", dry_run=dry_run)
    if dry_run or show_trace:
        runcommand.print_trace(["rm", "-f", path], dry_run=dry_run)
    if not dry_run:
        os.remove(path)


def _rename(oldpath, newpath, dry_run, show_trace=True):
    if dry_run:
        runcommand.print_message("Would do:", dry_run=dry_run)
    if dry_run or show_trace:
        runcommand.print_trace(["mv", "-f", oldpath, newpath], dry_run=dry_run)
    if not dry_run:
        os.rename(oldpath, newpath)


def _backup_existing(path, dry_run):
    if _file_exists(path):
        backup_path = _infer_backup_path(path)
        if _file_exists(backup_path):
            _remove_file(backup_path, dry_run=dry_run)
        _rename(path, backup_path, dry_run=dry_run)


def _remove_existing(path, dry_run):
    if _file_exists(path):
        _remove_file(path, dry_run=dry_run)


def _filter_paths(root, paths, include, check_ignore=None):
    include = FILTER_INCLUDE_SOME if include is None else include
    items_to_delete = []

    if include == FILTER_INCLUDE_ALL:
        pass
    elif include == FILTER_INCLUDE_SOME:
        for i, path in enumerate(paths):
            if path in FILTER_PATHS_SOME:
                items_to_delete.append(i)
    elif include in FILTER_INCLUDES_USING_GITIGNORE:
        for i, path in enumerate(paths):
            abspath = os.path.abspath(os.path.join(root, path))
            if check_ignore is not None and check_ignore(abspath):
                items_to_delete.append(i)
            elif include == FILTER_INCLUDE_GITIGNORE and path in FILTER_PATHS_GITIGNORE:
                items_to_delete.append(i)

    for i in reversed(items_to_delete):
        del paths[i]

    return paths


def _find_paths(path, include, sort=True):
    paths = [path]
    check_ignore = None
    if include in FILTER_INCLUDES_USING_GITIGNORE:
        gitignore_path = os.path.join(os.path.abspath(path), GITIGNORE_BASENAME)
        if _file_exists(gitignore_path):
            check_ignore = gitignore_parser.parse_gitignore(gitignore_path)
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        paths.extend(
            [
                os.path.join(root, x)
                for x in _filter_paths(
                    root, dirs, include=include, check_ignore=check_ignore
                )
            ]
        )
        paths.extend(
            [
                os.path.join(root, x)
                for x in _filter_paths(
                    root, files, include=include, check_ignore=check_ignore
                )
            ]
        )
    if sort:
        paths.sort()
    return paths


def _grok_extra_args(extra_args):
    return extra_args[1:] if (extra_args and extra_args[0] == "--") else extra_args


def _run_with_piped_input(input_data, command, dry_run, show_trace):
    if dry_run:
        runcommand.print_message("Would run:", dry_run=dry_run)
    if dry_run or show_trace:
        runcommand.print_trace(command, dry_run=dry_run)
    if dry_run:
        return 0
    process = subprocess.Popen(command, universal_newlines=True, stdin=subprocess.PIPE)  # noqa: S603
    process.communicate(input=input_data)
    status = process.wait()
    return status


def _do_zip(
    folder_path,
    zipfile_path,
    include=None,
    force=False,
    create_method=None,
    dry_run=False,
    more_options=None,
):
    folder_path = _normalize_path(folder_path)
    _dir_exists(folder_path, should_raise=True)
    if zipfile_path is None:
        zipfile_path = _infer_zipfile_path(folder_path, force=force)
    more_options = _grok_extra_args(more_options)

    if create_method == CREATE_METHOD_BACKUP:
        _backup_existing(zipfile_path, dry_run=dry_run)
    elif create_method == CREATE_METHOD_OVERWRITE:
        _remove_existing(zipfile_path, dry_run=dry_run)

    if include == FILTER_INCLUDE_ALL:
        zip_command = [
            ZIP_COMMAND,
            "-r",
            zipfile_path,
            folder_path,
        ]
        zip_command.extend(more_options)
        status = runcommand.run_command(
            zip_command, check=False, dry_run=dry_run, show_trace=True
        )
    else:
        zip_command = [
            ZIP_COMMAND,
            zipfile_path,
        ]
        zip_command.extend(more_options)
        zip_command.append("-@")

        paths = _find_paths(folder_path, include)

        status = _run_with_piped_input(
            "\n".join(paths), zip_command, dry_run, show_trace=True
        )

    return status


def main(*argv):
    """
    Do the CLI things.

    :Args:
        argv
            Zero or more arguments, beginning with the program name (like
            `sys.argv`:py:attr:)

    :Returns:
        An integer to indicate status:

        - 0: success
        - Nonzero: failure
    """
    (prog, argv) = argparsing.grok_argv(argv)
    prog_name = os.path.basename(prog)
    format_args = {"prog": prog, "prog_name": prog_name}
    argparser = argparsing.setup_argparse(
        prog=prog,
        description=DESCRIPTION_TEMPLATE.format(**format_args),
        epilog=EPILOG_TEMPLATE.format(**format_args),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_arguments(argparser)
    args = argparser.parse_args(argv)

    if args.folder is None or args.folder == "--":
        argparser.print_help()
        return STATUS_HELP

    status = _do_zip(
        args.folder,
        args.output,
        include=args.include,
        force=args.force,
        create_method=args.create_method,
        dry_run=args.dry_run,
        more_options=args.more_options,
    )
    return status
