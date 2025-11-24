#!/bin/bash
# Cleanup untagged GHCR images (SHA256 digests)

set -e

PACKAGE_NAME="${1:-eink-panel}"
OWNER="${2:-palemoky}"

echo "🧹 Cleaning up untagged GHCR images (SHA256 digests)..."
echo "Package: ${OWNER}/${PACKAGE_NAME}"

# Get all untagged versions (try org first, fall back to user)
UNTAGGED_IDS=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions?per_page=100" \
  --jq '.[] | select(.metadata.container.tags | length == 0) | .id' \
  2>/dev/null || \
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/users/${OWNER}/packages/container/${PACKAGE_NAME}/versions?per_page=100" \
  --jq '.[] | select(.metadata.container.tags | length == 0) | .id')

if [ -n "$UNTAGGED_IDS" ]; then
  COUNT=$(echo "$UNTAGGED_IDS" | wc -l | tr -d ' ')
  echo "📦 Found $COUNT untagged images to delete"
  
  DELETED=0
  FAILED=0
  
  echo "$UNTAGGED_IDS" | while read version_id; do
    if gh api \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions/${version_id}" \
      2>/dev/null; then
      echo "✓ Deleted untagged SHA256: $version_id"
      DELETED=$((DELETED + 1))
    elif gh api \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "/users/${OWNER}/packages/container/${PACKAGE_NAME}/versions/${version_id}"; then
      echo "✓ Deleted untagged SHA256: $version_id"
      DELETED=$((DELETED + 1))
    else
      echo "✗ Failed to delete untagged SHA256: $version_id"
      FAILED=$((FAILED + 1))
    fi
  done
  
  echo ""
  echo "📊 Summary: Deleted $DELETED untagged images, $FAILED failed"
  
  # Write to GitHub step summary
  if [ -n "$GITHUB_STEP_SUMMARY" ]; then
    echo "### 🧹 Untagged Images Cleanup" >> "$GITHUB_STEP_SUMMARY"
    echo "- **Deleted**: $DELETED untagged SHA256 images" >> "$GITHUB_STEP_SUMMARY"
    echo "- **Failed**: $FAILED" >> "$GITHUB_STEP_SUMMARY"
  fi
else
  echo "✨ No untagged images to delete"
  
  if [ -n "$GITHUB_STEP_SUMMARY" ]; then
    echo "### 🧹 Untagged Images Cleanup" >> "$GITHUB_STEP_SUMMARY"
    echo "✨ No untagged images found" >> "$GITHUB_STEP_SUMMARY"
  fi
fi
