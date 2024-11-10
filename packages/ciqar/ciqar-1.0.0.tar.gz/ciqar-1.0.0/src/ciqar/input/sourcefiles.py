from __future__ import annotations

from itertools import chain, tee
from pathlib import Path

from ciqar.input import SourceFile


class SourceFileCollector:
    """
    Collects all source files that have been analyzed and must therefore be respected for the
    report.

    The collection is done on demand when the data is accessed for the first time.
    """

    SOURCE_FILE_SUFFIX = "py"
    """
    Suffix of source files to search for.
    """

    def __init__(self, search_paths: list[Path], exclude_paths: list[Path]):
        """
        Create a new SourceFileCollector instance with the list of paths search for source files
        in. The search paths must share a common ancestor. On Linux/Unix this is usually
        fulfilled by "/", so the exception may mainly occur on Windows.

        :param seach_paths: List of (absolute) paths to recursively search for source files in.
        :path exclude_paths: List of (absolute) paths to exclude from the source file search.
        :raises ValueError: The given search paths do not share a common path, or no path given
                            at all.
        """
        if not search_paths:
            raise ValueError("Please provide at least one search path.")
        self._search_paths = search_paths
        self._exclude_paths = exclude_paths
        self._cached_source_files: dict[Path, SourceFile] = {}
        self._ignored_files: list[Path] = (
            []
        )  # List source files that have been ignored (-e CLI flag)
        self._base_path = self.__get_longest_common_base_path(search_paths)

    @staticmethod
    def __get_longest_common_base_path(search_paths: list[Path]) -> Path:
        """
        Finds the largsets common ancestor for the provided search paths.
        Example: The following paths share the common ancestor /tmp/src (and *not* /tmp!)
            /tmp/src/dir1/
            /tmp/src/dir2/
            /tmp/src/dir3/dir4

        :return: Longest common base path.
        :raises ValueError: There is no common base path
        """
        # Take the first path and check if it is a parent of all other ones.
        # If it is not, take the first item's parent and check again, until it's a parent of
        # all other items.
        pivot_path = search_paths[0]
        give_up = False
        while not give_up:
            if all(
                (pivot_path == other_path) or (pivot_path in other_path.parents)
                for other_path in search_paths[1:]
            ):
                return pivot_path
            give_up = bool(pivot_path.parent == pivot_path)
            pivot_path = pivot_path.parent
        raise ValueError("Unable to find a common parent of all provided search paths.")

    def __collect_source_files(self) -> None:
        """
        Collects all source files from all requested search paths.
        """
        if self._cached_source_files:
            return

        for search_path in self._search_paths:
            file_iter1, file_iter2 = tee(
                search_path.rglob("*.{}".format(self.SOURCE_FILE_SUFFIX)), 2
            )
            self._cached_source_files.update(
                {
                    p: SourceFile(p, self._base_path)
                    for p in file_iter1
                    if not self.__is_excluded(p)
                }
            )
            self._ignored_files.extend(filter(self.__is_excluded, file_iter2))

    def __is_excluded(self, source_file: Path) -> bool:
        """
        Checks whether the requested file is excluded.
        A file is excluded if it or one of its (direct or indirect) parents is contained in the
        `self._exclude_paths` list.
        """
        return any(
            filter(
                lambda f: f in self._exclude_paths, chain([source_file], source_file.parents)
            )
        )

    def get_excluded_source_files(self) -> list[Path]:
        """
        Get a list of all source file paths that have been excluded due to the "-e" CLI flag but
        would have been part of the source file list otherwise.
        """
        self.__collect_source_files()
        return self._ignored_files

    def get_all_source_files(self) -> list[SourceFile]:
        """
        Returns a list of all found source files.

        :returns: List of source file representations.
        """
        self.__collect_source_files()
        return list(self._cached_source_files.values())

    def get_source_file(self, source_file_path: Path) -> SourceFile:
        """
        Returns the SourceFile object for the requested file, if it exists in the source tree.

        :param source_file_path: Absolute path of the source file to lookup.
        :returns: Corresponding SourceFile object.
        :raises: FileNotFoundError if file does not exist.
        """
        self.__collect_source_files()
        try:
            return self._cached_source_files[source_file_path]
        except KeyError:
            raise FileNotFoundError(
                "File not found in source tree: {}".format(source_file_path)
            )
