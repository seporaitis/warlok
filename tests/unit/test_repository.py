import pytest

from warlok.repository import (
    RepositoryNotFoundError,
    RepositoryNotFoundMessage,
    get_repository_dir,
    get_repository_full_name,
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


def test_get_repository_full_name_success():
    actual = get_repository_full_name('git@github.com:seporaitis/warlok.git')

    assert actual == 'seporaitis/warlok'


def test_get_repository_full_name_indexerror():
    with pytest.raises(AttributeError):
        get_repository_full_name('https://github.com/seporaitis/warlok')
