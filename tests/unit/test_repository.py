from unittest import mock

import pytest

from warlok.repository import (
    get_repository_dir,
    RepositoryNotFoundError,
    RepositoryNotFoundMessage,
)


def test_get_repository_dir_unix_error():
    with mock.patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = [False, False, False]
        with pytest.raises(RepositoryNotFoundError) as err:
            get_repository_dir("/home/warlok/repo")

        assert str(err.value) == RepositoryNotFoundMessage(
            original="/home/warlok/repo"
        )
        assert mock_exists.call_count == 3


def test_get_repository_dir_windows_error():
    with mock.patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = [False, False, False]
        with pytest.raises(RepositoryNotFoundError) as err:
            get_repository_dir("c:/home/warlok/repo")

        assert str(err.value) == RepositoryNotFoundMessage(
            original="c:/home/warlok/repo"
        )
        assert mock_exists.call_count == 3


def test_get_repository_dir_unix():
    with mock.patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = [False, True, False]
        path = get_repository_dir("/home/warlok/repo/project")

        assert path == "/home/warlok/repo"
        assert mock_exists.call_count == 2


def test_get_repository_dir_windows():
    with mock.patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = [False, True, False]
        path = get_repository_dir("c:/home/warlok/repo/project")

        assert path == "c:/home/warlok/repo"
        assert mock_exists.call_count == 2
