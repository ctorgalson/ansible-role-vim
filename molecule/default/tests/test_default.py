import os

import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package", [
    "vim.tiny",
])
def test_removed_vim_packages(host, package):
    f = host.file("/usr/bin/{}".format(package))

    assert not f.exists


@pytest.mark.parametrize("package", [
    "vim",
])
def test_installed_vim_packages(host, package):
    f = host.file("/usr/bin/{}".format(package))

    assert f.exists


@pytest.mark.parametrize("owner,group", [
    ("molecule", "molecule"),
])
@pytest.mark.parametrize("directory", [
    ".vim/pack/ansible-managed",
    ".vim/pack/ansible-managed/start",
    ".vim/pack/ansible-managed/opt",
])
def test_vim_package_directories(host, owner, group, directory):
    f = host.file("/home/{}/{}".format(owner, directory))

    assert f.exists
    assert f.is_directory
    assert f.user == owner
    assert f.group == group


@pytest.mark.parametrize("owner,group", [
    ("molecule", "molecule"),
])
@pytest.mark.parametrize("directory", [
    "opt/vdebug",
    "start/lightline.vim",
    "start/vim-colors-solarized",
])
def test_vim_installed_plugins(host, owner, group, directory):
    p = "/home/{}/.vim/pack/ansible-managed/{}".format(owner, directory)
    f = host.file(p)

    assert f.exists
    assert f.is_directory
    assert f.user == owner
    assert f.group == group


@pytest.mark.parametrize("owner,group", [
    ("molecule", "molecule"),
])
@pytest.mark.parametrize("directory", [
    "opt/tabular",
    "start/nerdcommenter",
])
def test_vim_removed_plugins(host, owner, group, directory):
    p = "/home/{}/.vim/pack/ansible-managed/{}".format(owner, directory)
    f = host.file(p)

    assert not f.exists


@pytest.mark.parametrize("owner,group", [
    ("molecule", "molecule"),
])
@pytest.mark.parametrize("file", [
    ".vimrc",
])
def test_vim_dotfiles(host, owner, group, file):
    f = host.file("/home/{}/{}".format(owner, file))

    assert f.exists
    assert f.is_file
    assert f.user == owner
    assert f.group == group


@pytest.mark.parametrize("owner,group", [
    ("molecule", "molecule"),
])
@pytest.mark.parametrize("type,dir,helptags", [
  ("start", "lightline.vim", "lightline.txt"),
  ("start", "vim-colors-solarized", "solarized.txt"),
  ("opt", "vdebug", "Vdebug.txt"),
])
def test_vim_helptags(host, type, dir, helptags, owner, group):
    """
    The best way to test this would be to actually run :h pluginname in Vim
    using the method from this brilliant answer at vi.stackexchange.com.
    https://vi.stackexchange.com/q/8835/#8836.

    That way we could run e.g.:

    vim -c 'set t_ti= t_te= nomore' -c 'h lightline' -c 'qa!'

    This would return stdout out that we can use to analyze. But for whatever
    reason sudo -u molecule /bin/bash -c ' ... ' (Testinfra's only sudo method)
    doesn't actually work for this.

    As a result, we're just going to make sure a file named tags exists in the
    various plugins' doc directories, and that the file includes the plugin's
    name.
    """

    c = '/home/molecule/.vim/pack/ansible-managed/{}/{}/doc/tags'.format(
        type, dir)

    f = host.file(c)

    assert f.exists
    assert f.is_file
    assert f.user == owner
    assert f.group == group
    assert helptags in f.content_string
