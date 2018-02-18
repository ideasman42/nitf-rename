
************************************
Nifty Indispensable Text File Rename
************************************

NITF-rename is a convenient, command-line renaming utility
which uses a text-file to manipulate file names and optionally path hierarchy.

- Support for moving files between directories.
- Support for using version control when renaming (git, svn, hg).
- Directory creation (simply write in a new path hierarchy)
- No configuration.


Motivation
==========

While there are many graphical file renaming utilities,
I found them clumsy and wanted to use something more flexible that didn't depend on a GUI,
or involve scripting.

Usage
=====

The workflow is as follows:

- Run the command, passing in one or more directories that contain files you wish to rename.
- The editor you select will be opened with each filename on it's own line.
- Edit the filenames as you like **keeping them in order, without adding/removing lines**.
- Save the file and exit.
- The renaming operation will be performed, printing out a summary once complete.

.. note::

   There is no issues with recursively selecting a large number of files
   only to edit a handful. Unmodified text is simply ignored.

.. warning::

   Since renaming multiple files may fail at any point (permission denied or file-system error),
   you may want to back up the files before batch renaming.

   Unless you're using version control (the ``--vcs`` option), where the changes can be reverted.


Example Wrapper
---------------

Example of a wrapper that renames all files in the directories passed::

   #!/bin/sh
   exec nitf-rename \
       --editor "gvim --nofork {file}" \
       "$@"


Example Usage
-------------

Rename all files in the current directory::

   nitf-rename --editor="gvim --nofork {file}" .


Rename all C/C++ source files recursively within a git repository::

   nitf-rename \
       --editor="gvim --nofork {file}" \
       --include-files=".+\.(c|h|hh|cxx|cpp|cc|hxx|hpp)$" --recursive --vcs=git .

Help Text
=========

.. BEGIN HELP TEXT

Output of ``nitf-rename --help``

usage::

       nitf-rename [-h] --editor EDITOR_COMMAND [--quiet] [--overwrite]
                   [--recursive] [--flatten] [--prune-empty]
                   [--vcs <none,auto,git,hg,svn>]
                   [--include-files INCLUDE_FILES]
                   [--exclude-files EXCLUDE_FILES]
                   search_paths [search_paths ...]

NITF - Nifty Indispensable Text File Rename.

positional arguments:
  search_paths          Paths to scan for files to rename.

optional arguments:
  -h, --help            show this help message and exit
  --editor EDITOR_COMMAND
                        Command used to edit file and arguments
                        which will be passed to the editor:
                        ``{file}`` will be replaced
                        with the file-name.
                        eg: ``--editor="gvim {file} --nofork"``

                        Take care to run the editor in a foreground process to block until the process exits.

display arguments:
  These options control output.

  --quiet               Only print errors.

renaming behavior arguments:
  These options control how renaming is performed.

  --overwrite           Allow files to overwrite when new name already exists.
  --recursive           Include files recursively.
  --flatten             Remove path prefix from filenames.
                        Use with "--recursive" to strip the directories from the files.
  --prune-empty         Remove empty directories.
  --vcs <none,auto,git,hg,svn>
                        Move using version control.

filepath matching arguments:
  These options control which files are selected to be renamed.

  --include-files INCLUDE_FILES
                        Case insensitive regular expression matched against each file,
                        only include files that pass.
  --exclude-files EXCLUDE_FILES
                        Case insensitive regular expression matched against each file,
                        only search files that fail. Defaults to "\." (skip hidden files).

Typically this should be executed by a wrapper or shell alias.

.. END HELP TEXT


TODO
====

- Handle renaming that swaps exiting names
  *(currently reports error on overwriting).*
- A mode where paths are manipulated as a tree instead of a list of names
  *(to allow for more convenient changes to the directory structure).*
