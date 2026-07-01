#!/bin/bash

OUTPUT="testing/m5_label_results.txt"
echo "" >> "$OUTPUT"
echo "===============================" >> "$OUTPUT"
echo "=========== RE-RUN ===========" >> "$OUTPUT"
echo "===============================" >> "$OUTPUT"

echo "=== TEST 1: Label A (likely_ai) ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence represents a transformative paradigm shift in modern society. It is important to note that while the benefits of AI are numerous, it is equally essential to consider the ethical implications. Furthermore, stakeholders across various sectors must collaborate to ensure responsible deployment.", "creator_id": "label-test-ai"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TEST 2: Label B (uncertain) ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The relationship between monetary policy and asset price inflation has been extensively studied in the literature. Central banks face a fundamental tension between their mandate for price stability and the unintended consequences of prolonged low interest rates on equity and real estate valuations.", "creator_id": "label-test-uncertain"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TEST 3: Label C (likely_human) ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably wont go back unless someone drags me there", "creator_id": "label-test-human"}' \
  | python -m json.tool >> "$OUTPUT"

echo "Label test complete. Results saved to $OUTPUT"
