#!/bin/bash
# Quick script to delete all academic batches
# Usage: ./delete_batches_simple.sh YOUR_AUTH_TOKEN

API_URL="http://localhost:8000/api/v1/batches"

if [ -z "$1" ]; then
    echo "Usage: ./delete_batches_simple.sh YOUR_AUTH_TOKEN"
    echo ""
    echo "To get your token:"
    echo "1. Log in to http://localhost:3000"
    echo "2. Open DevTools (F12) → Application → Local Storage"
    echo "3. Copy the 'token' value"
    exit 1
fi

TOKEN="$1"

echo "📋 Fetching batches..."
BATCHES=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/")

# Show batches (simple version without jq)
echo "$BATCHES"
echo ""

# Extract IDs manually if jq is not available
if command -v jq &> /dev/null; then
    BATCH_IDS=$(echo "$BATCHES" | jq -r '.[].id')
else
    # Fallback: extract IDs using grep/sed
    BATCH_IDS=$(echo "$BATCHES" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
fi

if [ -z "$BATCH_IDS" ]; then
    echo "✅ No batches found!"
    exit 0
fi

echo "⚠️  Found batches with IDs: $BATCH_IDS"
echo ""
read -p "Delete all batches? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
for ID in $BATCH_IDS; do
    echo -n "Deleting batch $ID... "
    STATUS=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE -H "Authorization: Bearer $TOKEN" "$API_URL/$ID")
    if [ "$STATUS" = "200" ]; then
        echo "✅"
    else
        echo "❌ (HTTP $STATUS)"
    fi
done

echo ""
echo "✅ Done!"
