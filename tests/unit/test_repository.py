import pytest

from warlok.repository import (
    RepositoryNotFoundError,
    RepositoryNotFoundMessage,
    get_repository_dir,
)


def test_get_repository_dir_unix_error(os_path_exists_mock):

    os_path_exists_mock.side_effect = [False, False, False]
    with pytest.raises(RepositoryNotFoundError) as err:
        get_repository_dir('/home/warlok/repo')

    assert str(err.value) == RepositoryNotFoundMessage(
        original='/home/warlok/repo',
    )
    assert os_path_exists_mock.call_count == 3


def test_get_repository_dir_windows_error(os_path_exists_mock):
    os_path_exists_mock.side_effect = [False, False, False]
    with pytest.raises(RepositoryNotFoundError) as err:
        get_repository_dir('c:/home/warlok/repo')

    assert str(err.value) == RepositoryNotFoundMessage(
        original='c:/home/warlok/repo',
    )
    assert os_path_exists_mock.call_count == 3


def test_get_repository_dir_unix(os_path_exists_mock):
    os_path_exists_mock.side_effect = [False, True, False]
    path = get_repository_dir('/home/warlok/repo/project')

    assert path == '/home/warlok/repo'
    assert os_path_exists_mock.call_count == 2


def test_get_repository_dir_windows(os_path_exists_mock):
    os_path_exists_mock.side_effect = [False, True, False]
    path = get_repository_dir('c:/home/warlok/repo/project')

    assert path == 'c:/home/warlok/repo'
    assert os_path_exists_mock.call_count == 2
