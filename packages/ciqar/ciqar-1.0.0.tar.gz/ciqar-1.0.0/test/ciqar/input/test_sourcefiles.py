"""
Unit tests for the ciqar.input.sourcefiles module.
"""

from __future__ import annotations

from contextlib import AbstractContextManager, nullcontext
from pathlib import Path
from unittest.mock import MagicMock, Mock

from pyfakefs.fake_filesystem import FakeFilesystem
import pytest

from ciqar.input import SourceFile
from ciqar.input.sourcefiles import SourceFileCollector


class TestSourceFile:
    """
    Unit tests for the SourceFile class.
    """

    @pytest.mark.parametrize(
        "file_exists, init_context",
        [
            (True, nullcontext()),
            (False, pytest.raises(FileNotFoundError)),
        ],
    )
    def test_init(
        self, file_exists: bool, init_context: AbstractContextManager[None], fs: FakeFilesystem
    ) -> None:
        """
        Ensures the initialisation behaviour of SourceFile objects.
        """
        absolute_file_path = Path("/tmp/file.txt")

        if file_exists:
            fs.create_file(absolute_file_path)

        with init_context:
            source_file = SourceFile(absolute_file_path, Path("/tmp"))
            assert source_file.absolute_path == absolute_file_path
            assert source_file.project_relative_path == Path("file.txt")

    @pytest.mark.parametrize(
        "file_content, expected_line_count",
        [
            ([], 0),  # Empty file
            (["\n"], 0),  # Empty line
            (["single line"], 1),
            (["first line", "", "third line"], 2),
        ],
    )
    def test_line_count(
        self, file_content: list[str], expected_line_count: int, fs: FakeFilesystem
    ) -> None:
        absolute_file_path = Path("/tmp/sourcefile.py")
        fs.create_file(file_path=absolute_file_path, contents="\n".join(file_content))

        source_file = SourceFile(absolute_file_path, Path("/tmp"))
        assert source_file.line_count == expected_line_count

    @pytest.mark.parametrize(
        "file_content, expected_file_content",
        [
            ([], []),  # Empty file
            (["Hello", "World"], ["Hello", "World"]),
            (["   indented string   \r"], ["   indented string"]),  # Strip trailing whitespaces
        ],
    )
    def test_content(
        self, file_content: list[str], expected_file_content: list[str], fs: FakeFilesystem
    ) -> None:
        file_path = Path("/tmp/sourcefile.py")
        fs.create_file(file_path=file_path, contents="\n".join(file_content))

        source_file = SourceFile(file_path, Path("/tmp"))
        file_content = []
        for line in source_file.content:
            file_content.append(line)

        assert expected_file_content == file_content


class TestSourceFileCollector:
    """
    Unit tests for the SourceFileCollector class.
    """

    @pytest.mark.parametrize(
        "search_paths, init_context, expected_base_path",
        [
            (["/project/src"], nullcontext(), "/project/src"),
            (["/project/src/lib1", "/project/src/lib2"], nullcontext(), "/project/src"),
            (
                ["/project/src/ext/lib/", "/project/src/app/src", "/project/src/app/test"],
                nullcontext(),
                "/project/src",
            ),
            (["/project", "/project/src"], nullcontext(), "/project"),
            (["/project/src", "/project"], nullcontext(), "/project"),
            (["/project1", "/project2"], nullcontext(), "/"),
            ([], pytest.raises(ValueError), ""),
        ],
    )
    def test_find_common_base_path(
        self,
        search_paths: list[str],
        init_context: AbstractContextManager[None],
        expected_base_path: str,
    ) -> None:
        """
        Tests the search for finding the largest common ancestor (base path) from the provided
        list of paths. (Done during object initialization.)
        """
        with init_context:
            collector = SourceFileCollector(
                search_paths=[Path(p) for p in search_paths], exclude_paths=[]
            )
            assert collector._base_path == Path(expected_base_path)

    @pytest.mark.parametrize(
        "existing_files, search_paths, exclude_paths, found_files, excluded_files",
        [
            (  # Single source dir
                ["/project/main.py", "/project/lib.py", "/project/README.md"],
                ["/project"],
                [],
                ["/project/main.py", "/project/lib.py"],
                [],
            ),
            (  # Multiple source directories
                ["/project/src/main.py", "/project/test/test_main.py", "/project/README.md"],
                ["/project/src", "/project/test"],
                [],
                ["/project/src/main.py", "/project/test/test_main.py"],
                [],
            ),
            (  # No files to find
                ["/project/src/main.py", "/project/test/test_main.py", "/project/README.md"],
                ["/home/user"],
                [],
                [],
                [],
            ),
            (  # Exclude single file
                ["/project/main.py", "/project/test_main.py", "/project/tasks.py"],
                ["/project/"],
                ["/project/tasks.py"],
                ["/project/main.py", "/project/test_main.py"],
                ["/project/tasks.py"],
            ),
            (  # Exclude single directory
                ["/project/src/main.py", "/project/src/test_main.py", "/project/tasks.py"],
                ["/project"],
                ["/project/src"],
                ["/project/tasks.py"],
                ["/project/src/main.py", "/project/src/test_main.py"],
            ),
            (  # Exclude multiple paths (file & dir)
                [
                    "/project/src/main.py",
                    "/project/src/test_main.py",
                    "/project/tasks.py",
                    "/project/main.py",
                ],
                ["/project"],
                ["/project/src", "/project/tasks.py"],
                ["/project/main.py"],
                ["/project/src/main.py", "/project/src/test_main.py", "/project/tasks.py"],
            ),
            (  # Exclude path does not exist
                ["/project/main.py", "/project/test_main.py"],
                ["/project"],
                ["/home/user"],
                ["/project/main.py", "/project/test_main.py"],
                [],
            ),
        ],
    )
    def test_collect_source_files(
        self,
        existing_files: list[str],
        search_paths: list[str],
        exclude_paths: list[str],
        found_files: list[str],
        excluded_files: list[str],
        fs: FakeFilesystem,
    ) -> None:
        for file in existing_files:
            fs.create_file(file_path=file, create_missing_dirs=True)

        collector = SourceFileCollector(
            search_paths=[Path(p) for p in search_paths],
            exclude_paths=[Path(p) for p in exclude_paths],
        )
        found_source_files = collector.get_all_source_files()
        excluded_source_files = collector.get_excluded_source_files()

        assert sorted(
            [str(file_info.absolute_path) for file_info in found_source_files]
        ) == sorted(found_files)
        assert sorted([str(file_path) for file_path in excluded_source_files]) == sorted(
            excluded_files
        )

    def test_collect_source_files_once(self) -> None:
        """
        Ensures that the file system is only traversed once, i.e. a second call must use the
        internal cache.
        """
        source_file_path = MagicMock(spec=Path)  # MagicMock to be able to iterate .parents
        source_file_path.exists.return_value = True
        mocked_path = Mock(spec=Path)
        mocked_path.rglob.return_value = [source_file_path]
        collector = SourceFileCollector(search_paths=[mocked_path], exclude_paths=[])

        source_file = collector.get_source_file(source_file_path)
        assert source_file.absolute_path == source_file_path
        assert mocked_path.rglob.call_count == 1

        # Second call must not call `rglob()` again, but still provide a result!
        source_file = collector.get_source_file(source_file_path)
        assert source_file.absolute_path == source_file_path
        assert mocked_path.rglob.call_count == 1

    @pytest.mark.parametrize(
        "request_filepath, raise_context",
        [
            ("/tmp/source.py", nullcontext()),  # Normal case of existing file
            ("/tmp/missingfile.py", pytest.raises(FileNotFoundError)),  # File does not exist
            (
                "/src/main.py",
                pytest.raises(FileNotFoundError),
            ),  # File exists, but is not in the search path
        ],
    )
    def test_get_source_file(
        self,
        request_filepath: str,
        raise_context: AbstractContextManager[None],
        fs: FakeFilesystem,
    ) -> None:
        """
        Tests correct behaviour of the `get_source_file()` method.
        For this test, the only existings source files are '/tmp/source.py' and '/src/main.py',
        the collector search path is '/tmp'.
        """
        fs.create_file("/tmp/source.py")
        collector = SourceFileCollector(search_paths=[Path("/tmp")], exclude_paths=[])

        with raise_context:
            source_file = collector.get_source_file(Path(request_filepath))
            assert str(source_file.absolute_path) == request_filepath
