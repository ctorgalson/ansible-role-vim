# Ansible Role Vim

An Ansible role to install Vim and plugins on Linux and macOS.

This role uses Vim 8's native package manager (see `:help packages`), so roles will be
installed by default to the following locations:

- `~/.vim/pack/ansible-managed/start`
- `~/.vim/pack/ansible-managed/opt`

## Requirements

The role has no special requirements, but Vim package management only
works with Vim > 8.0, so it's necessary to ensure that a sufficiently
recent version of Vim is either present, or will be installed by setting
the `vim_installed_packages` variable appropriately.

## Role Variables

The following variables are used in the role. See also Example Playbook
(below) and `molecule/default/playbook.yml` for specific examples.

| Variable name | Default value | Description |
|---------------|---------------|-------------|
| `vim_installed_packages`      | `["vim"]`         | A list of packages to install (passed to Ansible's Package module). |
| `vim_removed_packages`        | `[]`              | A list of packages to remove (e.g. on Ubuntu, it might be preferable to remove `vim-tiny`). |
| `vim_owner`                   | `""`              | The system user to install Vim and/or associated plugins for. |
| `vim_group`                   | `""`              | The group of the user specificed in `vim_owner`. |
| `vim_pack_subdirectory`       | `ansible-managed` | The name of the directory to place plugins installed by this role into the default creates e.g. `~/.vim/pack/ansible-managed/start` and `~/.vim/pack/ansible-managed/opt`. |
| `vim_start_installed_plugins` | `[]`              | The list of plugins to install to `~/.vim/pack/ansible-managed/start`--see `:help packages` for details on what this means. Should contain a `repo` property and (optionally) a `version` property as used by Ansible's Git module. |
| `vim_opt_installed_plugins`   | `[]`              | The list of plugins to install to `~/.vim/pack/ansible-managed/opt`--see `:help packages` for details on what this means. Should contain a `repo` property and (optionally) a `version` property as used by Ansible's Git module. |
| `vim_start_removed_plugins`   | `[]`              | A list of directory names to remove from `~/.vim/pack/ansible-managed/start`. |
| `vim_opt_removed_plugins`     | `[]`              | A list of directory names to remove from `~/.vim/pack/ansible-managed/opt`. |
| `vim_dotfiles`                | `[]`              | A list of local vim-related dotfiles to install to `~/`. |

## Example Playbook

    ---
    # Note: all of these plugins--even the ones being removed in the
    # example--are awesome plugins that I use every day.
    #
    - hosts: all
      vars:
        vim_removed_packages:
          - "vim-tiny"
        vim_owner: "lorem"
        vim_group: "lorem"
        vim_start_installed_plugins:
          - repo: "https://github.com/altercation/vim-colors-solarized.git"
          - repo: "https://github.com/itchyny/lightline.vim.git"
          - repo: "https://github.com/scrooloose/nerdcommenter.git"
        vim_opt_installed_plugins:
          - repo: "https://github.com/vim-vdebug/vdebug.git"
          - repo: "https://github.com/godlygeek/tabular.git"
        vim_start_removed_plugins:
          - "nerdcommenter"
        vim_opt_removed_plugins:
          - "tabular"
        vim_dotfiles:
          - "{{ playbook_dir }}/files/dotfiles/.vimrc"
      roles:
        - role: ansible-role-vim

## License

GPLv3

## Author Information

Christopher Torgalson
