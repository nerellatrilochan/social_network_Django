#!/bin/sh

# Remove the local tag 'patch_deploy'
git tag -d patch_deploy

# Fetch all tags from remote
git push --delete origin patch_deploy
echo "Removed remote tag 'patch_deploy'"

# Add new tag 'patch_deploy'
git tag patch_deploy
echo "Added new tag 'patch_deploy'"

# Push 'patch_deploy' tag to remote
git push origin patch_deploy
echo "Pushed 'patch_deploy' tag to remote"

# Print commit hash and commit message of 'patch_deploy' tag
echo "Commit hash: $(git rev-parse patch_deploy)"
echo "Commit message: $(git show -s --format=%B $(git rev-parse patch_deploy))"
