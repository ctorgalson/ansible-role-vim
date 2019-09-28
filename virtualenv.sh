#!/bin/bash

set -e

venv_path=".venv"
venv_activate="$venv_path/bin/activate"
venv_deactivate="deactivate"

# Create a brand-new virtualenv directory.
rm -rf "$venv_path" && virtualenv "$venv_path"

# Activate virtualenv within this process.
#
# Shellcheck wants to be able to source this file itself, but can't do so when
# the path is created at runtime. Oh well.
#
# shellcheck disable=SC1090
source "$venv_activate"

# Install packages as needed.
pip install "testinfra" "docker" "molecule"

# Deactviate virtualenv within this process.
"$venv_deactivate"

# Tell the user what to do.
echo ""
echo "Virtualenv prepared and packages installed. Use '. $venv_activate' to get started and '$venv_deactivate' when finished."
echo ""
