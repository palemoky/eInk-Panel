#!/bin/bash
# Cleanup old GHCR pre-release images (keep latest 2)

set -e

PACKAGE_NAME="${1:-eink-dashboard}"
OWNER="${2:-palemoky}"

echo "🧹 Cleaning up old GHCR pre-release images..."
echo "Package: ${OWNER}/${PACKAGE_NAME}"

# Try org endpoint first, fall back to user endpoint
# Get all versions with pre-release tags, sorted by created_at (newest first)
VERSIONS=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions?per_page=100" \
  --jq '[.[] | select(.metadata.container.tags | length > 0) | select(.metadata.container.tags[] | test("alpha|beta|rc"))] | sort_by(.created_at) | reverse | .[2:] | .[] | {id: .id, tags: .metadata.container.tags, created_at: .created_at}' \
  2>/dev/null || \
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/users/${OWNER}/packages/container/${PACKAGE_NAME}/versions?per_page=100" \
  --jq '[.[] | select(.metadata.container.tags | length > 0) | select(.metadata.container.tags[] | test("alpha|beta|rc"))] | sort_by(.created_at) | reverse | .[2:] | .[] | {id: .id, tags: .metadata.container.tags, created_at: .created_at}')

# Get version IDs to delete (skip the latest 2)
VERSION_IDS=$(echo "$VERSIONS" | jq -r '.id')

if [ -n "$VERSION_IDS" ]; then
  COUNT=$(echo "$VERSION_IDS" | wc -l | tr -d ' ')
  echo "📦 Found $COUNT old pre-release versions to delete (keeping latest 2)"
  
  DELETED=0
  FAILED=0
  
  echo "$VERSION_IDS" | while read version_id; do
    # Try org endpoint first, fall back to user endpoint
    if gh api \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions/${version_id}" \
      2>/dev/null; then
      echo "✓ Deleted version ID: $version_id"
      DELETED=$((DELETED + 1))
    elif gh api \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/users/${OWNER}/packages/container/${PACKAGE_NAME}/versions/${version_id}"; then
      echo "✓ Deleted version ID: $version_id"
      DELETED=$((DELETED + 1))
    else
      echo "✗ Failed to delete version ID: $version_id"
      FAILED=$((FAILED + 1))
    fi
  done
  
  echo ""
  echo "📊 Summary: Deleted $DELETED versions, $FAILED failed"
else
  echo "✨ No old pre-release versions to delete (keeping latest 2)"
fi
