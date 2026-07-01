#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./test_m5_appeals.sh <content_id>"
  echo "Hint: Run ./test_m5_labels.sh first, grab a content_id from the output, and pass it here."
  exit 1
fi

CONTENT_ID="$1"
OUTPUT="testing/m5_appeal_results.txt"
> "$OUTPUT"

echo "=== SUBMITTING APPEAL FOR CONTENT: $CONTENT_ID ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/appeal \
  -H "Content-Type: application/json" \
  -d "{\"content_id\": \"$CONTENT_ID\", \"creator_reasoning\": \"I wrote this myself from personal experience. I am a non-native English speaker and my writing style may appear more formal than typical.\"}" \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== AUDIT LOG VERIFICATION ===" >> "$OUTPUT"
curl -s http://localhost:5000/log | python -m json.tool >> "$OUTPUT"

echo "Appeal test complete. Results saved to $OUTPUT"
