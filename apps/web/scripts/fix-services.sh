#!/bin/bash

# Batch fix all service files to use centralized api instance
# This script replaces "import axios from 'axios'" with "import { api } from '@/utils/api'"
# and removes BASE_URL constants, replacing axios.* calls with api.* calls

SERVICE_FILES=(
  "analytics-api.ts"
  "document-api.ts"
  "hall-ticket-api.ts"
  "hostel-api.ts"
  "internal-exam-api.ts"
  "library-api.ts"
  "payment-api.ts"
  "placement-api.ts"
  "transport-api.ts"
  "university-exam-api.ts"
)

for file in "${SERVICE_FILES[@]}"; do
  filepath="src/services/$file"
  
  if [ -f "$filepath" ]; then
    echo "Processing $file..."
    
    # Replace import statement
    sed -i '' "s/import axios from 'axios';/import { api } from '@\/utils\/api';/g" "$filepath"
    
    # Remove BASE_URL line
    sed -i '' "/^const BASE_URL = /d" "$filepath"
    sed -i '' "/^const BASE_URL=/d" "$filepath"
    
    # Replace axios.get with api.get
    sed -i '' "s/axios\.get(\`\${BASE_URL}/api.get(\`/g" "$filepath"
    sed -i '' "s/axios\.post(\`\${BASE_URL}/api.post(\`/g" "$filepath"
    sed -i '' "s/axios\.put(\`\${BASE_URL}/api.put(\`/g" "$filepath"
    sed -i '' "s/axios\.delete(\`\${BASE_URL}/api.delete(\`/g" "$filepath"
    sed -i '' "s/axios\.patch(\`\${BASE_URL}/api.patch(\`/g" "$filepath"
    
    echo "✅ Fixed $file"
  else
    echo "⚠️  File not found: $filepath"
  fi
done

echo ""
echo "🎉 Batch fix complete!"
echo "Files processed: ${#SERVICE_FILES[@]}"
