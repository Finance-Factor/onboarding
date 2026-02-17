#!/bin/bash
set -e

SSH_CFG="$HOME/.ssh/config"

sudo rsync -avz --delete \
    --exclude "secrets/staging" --exclude "secrets/prod" \
    --exclude "node_modules" --exclude ".next" \
    -e "ssh -F $SSH_CFG" \
    ff:/srv/shared_root/platform ../

sudo chown -R "$USER:$USER" ../platform