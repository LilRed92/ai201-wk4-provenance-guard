#!/bin/bash

OUTPUT="testing/m5_ratelimit_results.txt"
> "$OUTPUT"

echo "=== RATE LIMIT TEST (12 rapid requests) ===" >> "$OUTPUT"

for i in $(seq 1 12); do
  echo -n "Request $i: HTTP Status " >> "$OUTPUT"
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:5000/submit \
    -H "Content-Type: application/json" \
    -d '{"text": "This is a rate limit test.", "creator_id": "ratelimit-test"}' >> "$OUTPUT"
done

echo "Rate limit test complete. Results saved to $OUTPUT"
