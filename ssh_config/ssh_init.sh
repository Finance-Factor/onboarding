# ----- SSH Agent persistent & multi-keys with auto-expiring keys -----

# List of keys to load (modify as needed)
SSH_KEYS=(
  "$HOME/.ssh/ssh_hostinger"
  "$HOME/.ssh/ssh_wsl_github"
)

# Expiration time for each key (in seconds)
SSH_KEY_LIFETIME=10800 # 3 hours

# File storing agent environment variables
SSH_ENV="$HOME/.ssh/agent_env"

# Start a new ssh-agent and load keys
start_agent() {
    echo "[SSH] Starting new ssh-agent..."
    /usr/bin/ssh-agent -s > "$SSH_ENV"
    chmod 600 "$SSH_ENV"
    source "$SSH_ENV" >/dev/null

    LOADED_KEYS=()

    for key in "${SSH_KEYS[@]}"; do
        if [ -f "$key" ]; then
            if ssh-add -t "$SSH_KEY_LIFETIME" "$key" </dev/null >/dev/null 2>&1; then
                LOADED_KEYS+=("$(basename "$key")")
            fi
        fi
    done

    if [ ${#LOADED_KEYS[@]} -gt 0 ]; then
        echo "[SSH] Keys added with expiration (${SSH_KEY_LIFETIME}s): ${LOADED_KEYS[*]}"
    else
        echo "[SSH] No keys loaded."
    fi
}

# If an existing agent environment file is present
if [ -f "$SSH_ENV" ]; then
    source "$SSH_ENV" >/dev/null

    # Check if the agent is still running
    if ! kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
        echo "[SSH] Stale agent detected, starting a new one..."
        start_agent
    fi
else
    # No environment file → first-time startup
    start_agent
fi