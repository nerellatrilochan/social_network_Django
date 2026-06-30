#!/bin/bash

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Check if arguments are provided
if [ -z "$1" ]; then
    log "Usage: $0 <version-type>"
    exit 1
fi

# Get the previous version
previous_version=$(poetry version | cut -d' ' -f2)
log "Previous version: $previous_version"

# Run poetry version with the specified component
log "Updating version with Poetry..."
if ! poetry version "$1"; then
    log "Failed to update version using Poetry."
    exit 1
fi

# Get the current version
current_version=$(poetry version | cut -d' ' -f2)
log "Current version: $current_version"

# Attempt to extract the file path from pyproject.toml
log "Extracting file to commit from pyproject.toml..."
file_to_commit=$(grep -Po '(?<=file\.")([^"]+)' pyproject.toml | head -1)  # Ensure only the first match is taken
if [ -z "$file_to_commit" ]; then
    log "Failed to find the file to commit in pyproject.toml."
    exit 1
fi
log "File to commit: $file_to_commit"

# Update the version in the specified __init__.py file
log "Updating version in $file_to_commit..."
if ! sed -i "s/^__version__ = .*/__version__ = '$current_version'/g" "$file_to_commit"; then
    log "Failed to update the version in $file_to_commit."
    exit 1
fi

# Add changes to staging
log "Adding changes to staging..."
if ! git add pyproject.toml "$file_to_commit"; then
    log "Failed to add changes to staging."
    exit 1
fi

# Commit the changes
log "Committing changes..."
if ! git commit -m "Poetry version: $previous_version -> $current_version"; then
    log "Failed to commit changes."
    exit 1
fi

# Tag the commit
log "Tagging the commit..."
if ! git tag "v$current_version"; then
    log "Failed to create git tag."
    exit 1
fi

log "Successfully updated and committed the version: $previous_version -> $current_version"
