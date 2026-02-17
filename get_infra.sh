#!/bin/bash

# This script will fail if any command fails, so that we don't end up with a half-updated platform directory.
set -e

# Check if rsync is installed, otherwise install it
if ! command -v rsync &> /dev/null; then
  echo "rsync could not be found, installing it..."
  sudo apt-get update
  sudo apt-get install -y rsync
  echo "rsync installed successfully."
fi

# Prompt the user for the SSH alias of their main VPS session
read -p "Enter your main VPS session SSH alias: " ssh_alias
ssh_alias=$(echo "$ssh_alias" | xargs)
SSH_ALIAS="$ssh_alias"

# Prompt the user for the destination folder name
# read -p "Enter the destination folder name in your home (Just hit ENTER for default name: platform): " folder_name
# folder_name=${folder_name:-platform}
# FOLDER_NAME="$folder_name"

# mkdir -p ~/"$FOLDER_NAME"

# Check if the SSH alias is defined in the SSH config file
SSH_CONFIG_FILE="$HOME/.ssh/config"

sudo rsync -avz --delete \
    --exclude "secrets/staging" --exclude "secrets/prod" \
    --exclude "node_modules" --exclude ".next" --exclude ".venv" --exclude "__pycache__" --exclude "services/appsmith" \
    -e "ssh -F $SSH_CONFIG_FILE" \
    "$SSH_ALIAS":/srv/shared_root/platform ~/

sudo chown -R "$USER:$USER" ~/platform