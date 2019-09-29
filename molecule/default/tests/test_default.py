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
    ("lorem", "lorem"),
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
    ("lorem", "lorem"),
])
@pytest.mark.parametrize("directory", [
    "opt/vdebug",
    "start/lightline.vim",
    "start/vim-colors-solarized",
])
def test_vim_installed_packages(host, owner, group, directory):
    p = "/home/{}/.vim/pack/ansible-managed/{}".format(owner, directory)
    f = host.file(p)

    assert f.exists
    assert f.is_directory
    assert f.user == owner
    assert f.group == group


@pytest.mark.parametrize("owner,group", [
    ("lorem", "lorem"),
])
@pytest.mark.parametrize("directory", [
    "opt/tabular",
    "start/nerdcommenter",
])
def test_vim_removed_packages(host, owner, group, directory):
    p = "/home/{}/.vim/pack/ansible-managed/{}".format(owner, directory)
    f = host.file(p)

    assert not f.exists
