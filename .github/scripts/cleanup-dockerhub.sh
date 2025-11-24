#!/bin/bash
# Cleanup old Docker Hub pre-release tags (keep latest 2)

set -e

DOCKERHUB_USERNAME="${1}"
DOCKERHUB_TOKEN="${2}"
REPO_NAME="${3}"

echo "🧹 Cleaning up old Docker Hub pre-release tags..."
echo "Repository: ${REPO_NAME}"

# Get Docker Hub token
HUB_TOKEN=$(curl -s -H "Content-Type: application/json" -X POST \
  -d "{\"username\": \"${DOCKERHUB_USERNAME}\", \"password\": \"${DOCKERHUB_TOKEN}\"}" \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

if [ -z "$HUB_TOKEN" ] || [ "$HUB_TOKEN" = "null" ]; then
  echo "❌ Failed to get Docker Hub token"
  exit 1
fi

# Get all pre-release tags
TAGS=$(curl -s -H "Authorization: JWT ${HUB_TOKEN}" \
  "https://hub.docker.com/v2/repositories/${REPO_NAME}/tags/?page_size=100" \
  | jq -r '.results[] | select(.name | test("alpha|beta|rc")) | .name' \
  | sort -V)

# Keep latest 2, delete others
OLD_TAGS=$(echo "$TAGS" | head -n -2)

if [ -n "$OLD_TAGS" ]; then
  COUNT=$(echo "$OLD_TAGS" | wc -l | tr -d ' ')
  echo "📦 Found $COUNT old tags to delete (keeping latest 2)"
  
  DELETED=0
  FAILED=0
  
  echo "$OLD_TAGS" | while read tag; do
    if curl -X DELETE \
      -H "Authorization: JWT ${HUB_TOKEN}" \
      "https://hub.docker.com/v2/repositories/${REPO_NAME}/tags/${tag}/" \
      -s -o /dev/null -w "%{http_code}" | grep -q "^20"; then
      echo "✓ Deleted tag: $tag"
      DELETED=$((DELETED + 1))
    else
      echo "✗ Failed to delete tag: $tag"
      FAILED=$((FAILED + 1))
    fi
  done
  
  echo ""
  echo "📊 Summary: Deleted $DELETED tags, $FAILED failed"
else
  echo "✨ No old Docker Hub tags to clean (keeping latest 2)"
fi
