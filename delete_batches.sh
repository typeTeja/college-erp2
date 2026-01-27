#!/bin/bash
# Simple script to delete all academic batches using curl
# This assumes you're logged in and have a valid session

API_URL="http://localhost:8000/api/v1/batches"

echo "=================================================="
echo "🗑️  Delete All Academic Batches"
echo "=================================================="
echo ""

# Note: You need to get your auth token first
echo "⚠️  IMPORTANT: You need to provide your authentication token"
echo ""
echo "To get your token:"
echo "1. Log in to http://localhost:3000"
echo "2. Open browser DevTools (F12)"
echo "3. Go to Application > Local Storage"
echo "4. Copy the 'token' value"
echo ""
read -p "Enter your auth token: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

echo ""
echo "📋 Fetching all batches..."
echo ""

# List all batches
BATCHES=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/")

# Check if we got a valid response
if [ $? -ne 0 ]; then
    echo "❌ Error connecting to API"
    exit 1
fi

# Extract batch IDs (requires jq)
if ! command -v jq &> /dev/null; then
    echo "❌ Error: 'jq' is not installed. Please install it first:"
    echo "   brew install jq"
    exit 1
fi

BATCH_IDS=$(echo "$BATCHES" | jq -r '.[].id')

if [ -z "$BATCH_IDS" ]; then
    echo "✅ No batches found to delete!"
    exit 0
fi

# Count batches
BATCH_COUNT=$(echo "$BATCH_IDS" | wc -l | tr -d ' ')

echo "Found $BATCH_COUNT batch(es):"
echo "$BATCHES" | jq -r '.[] | "  - ID: \(.id) | \(.batch_code) | \(.batch_name)"'
echo ""

# Confirm deletion
echo "⚠️  WARNING: This will delete ALL $BATCH_COUNT batch(es)!"
echo "This action cannot be undone."
echo ""
read -p "Type 'yes' to confirm: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Deletion cancelled."
    exit 0
fi

echo ""
echo "🗑️  Deleting batches..."
echo ""

# Delete each batch
SUCCESS=0
for ID in $BATCH_IDS; do
    echo -n "Deleting batch ID $ID... "
    RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null -X DELETE -H "Authorization: Bearer $TOKEN" "$API_URL/$ID")
    
    if [ "$RESPONSE" = "200" ]; then
        echo "✅ Success"
        ((SUCCESS++))
    else
        echo "❌ Failed (HTTP $RESPONSE)"
    fi
done

echo ""
echo "=================================================="
echo "✅ Deleted $SUCCESS/$BATCH_COUNT batches successfully!"
echo "=================================================="
