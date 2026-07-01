#!/bin/bash

OUTPUT="testing/test_results.txt"
echo "" >> "$OUTPUT"
echo "===============================" >> "$OUTPUT"
echo "=== RE-RUN: Updated TTR Weights ===" >> "$OUTPUT"
echo "===============================" >> "$OUTPUT"

echo "=== TEST 1: Clearly AI-generated ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence represents a transformative paradigm shift in modern society. It is important to note that while the benefits of AI are numerous, it is equally essential to consider the ethical implications. Furthermore, stakeholders across various sectors must collaborate to ensure responsible deployment.", "creator_id": "test-m4-1"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TEST 2: Clearly human-written ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "ok so i finally tried that new ramen place downtown and honestly? underwhelming. the broth was fine but they put WAY too much sodium in it and i was thirsty for like three hours after. my friend got the spicy version and said it was better. probably wont go back unless someone drags me there", "creator_id": "test-m4-2"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TEST 3: Borderline formal human ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The relationship between monetary policy and asset price inflation has been extensively studied in the literature. Central banks face a fundamental tension between their mandate for price stability and the unintended consequences of prolonged low interest rates on equity and real estate valuations.", "creator_id": "test-m4-3"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== TEST 4: Lightly edited AI output ===" >> "$OUTPUT"
curl -s -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I have been thinking a lot about remote work lately. There are genuine tradeoffs — flexibility and no commute on one side, isolation and blurred work-life boundaries on the other. Studies show productivity varies widely by individual and role type.", "creator_id": "test-m4-4"}' \
  | python -m json.tool >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "=== AUDIT LOG ===" >> "$OUTPUT"
curl -s http://localhost:5000/log | python -m json.tool >> "$OUTPUT"

echo "Done! Results saved to $OUTPUT"