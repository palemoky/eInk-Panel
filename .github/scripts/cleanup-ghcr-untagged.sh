#!/bin/bash
# Cleanup untagged GHCR images (SHA256 digests)

set -e

PACKAGE_NAME="${1:-eink-dashboard}"
OWNER="${2:-palemoky}"

echo "🧹 Cleaning up untagged GHCR images (SHA256 digests)..."
echo "Package: ${OWNER}/${PACKAGE_NAME}"

# Determine the correct endpoint (Org or User)
echo "🔍 Determining endpoint type..."
if gh api "/orgs/${OWNER}" >/dev/null 2>&1; then
  echo "✅ Detected Organization account"
  BASE_ENDPOINT="/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions"
else
  echo "✅ Detected User account"
  BASE_ENDPOINT="/users/${OWNER}/packages/container/${PACKAGE_NAME}/versions"
fi

# Get untagged images using the determined endpoint
echo "🔍 Fetching untagged images from ${BASE_ENDPOINT}..."
UNTAGGED_IDS=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "${BASE_ENDPOINT}?per_page=100" \
  --jq '.[] | select(.metadata.container.tags | length == 0) | .id' \
  2>/dev/null || echo "")

if [ -n "$UNTAGGED_IDS" ]; then
  COUNT=$(echo "$UNTAGGED_IDS" | wc -l | tr -d ' ')
  echo "📦 Found $COUNT untagged images to delete"
  
  DELETED=0
  FAILED=0
  
  echo "$UNTAGGED_IDS" | while read version_id; do
    # Skip if version_id is empty or looks like JSON
    if [ -z "$version_id" ] || [[ "$version_id" == *"{"* ]]; then
      continue
    fi
    
    # Delete using the determined endpoint
    if gh api \
      --method DELETE \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      "${BASE_ENDPOINT}/${version_id}" \
      >/dev/null 2>&1; then
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
