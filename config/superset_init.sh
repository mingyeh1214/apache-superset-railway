#!/bin/bash

# Conditional bootstrap admin: only run on a fresh install (no existing
# admin row in ab_user). Once the first admin exists, manage further
# accounts through the Superset UI (Settings → List Users) instead of
# re-running fab create-admin on every deploy — that command never
# updates an existing user's password and just litters the deploy log
# with "Error! User already exists ..." each restart.
USER_COUNT=$(superset fab list-users 2>/dev/null | grep -cE "^[[:space:]]*\|[[:space:]]*[0-9]" || echo 0)
if [ "${USER_COUNT:-0}" -eq 0 ] && [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
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

# Starting server
/bin/sh -c /usr/bin/run-server.sh
