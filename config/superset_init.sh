#!/bin/bash

# Conditional bootstrap admin: only run on a fresh install (no existing
# user row). Once Superset has at least one user, deploys stop adding
# dummy admins and stop spamming "Error! User already exists ..." into
# the log. Manage further accounts through Settings → List Users in
# the UI; ADMIN_USERNAME/PASSWORD env vars are now a fresh-install
# convenience, not an active credential.
USER_COUNT=$(superset fab list-users 2>/dev/null | grep -cE "^[[:space:]]*\|[[:space:]]*[0-9]")
USER_COUNT=${USER_COUNT:-0}
if [ "$USER_COUNT" -eq 0 ] 2>/dev/null && [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
    echo "No existing users found — bootstrapping initial admin '$ADMIN_USERNAME'"
    superset fab create-admin \
        --username "$ADMIN_USERNAME" \
        --firstname Superset \
        --lastname Admin \
        --email "$ADMIN_EMAIL" \
        --password "$ADMIN_PASSWORD"
else
    echo "Skipping fab create-admin (existing users: $USER_COUNT)"
fi

# Upgrading Superset metastore
superset db upgrade

# setup roles and permissions
superset superset init

# Starting server (exec so gunicorn becomes PID 1 — Railway sees it
# stay alive and routes traffic to it; without exec the wrapper shell
# exits as soon as run-server.sh forks gunicorn into the background,
# Railway calls that "container exited" and tears the service down.)
exec /usr/bin/run-server.sh
