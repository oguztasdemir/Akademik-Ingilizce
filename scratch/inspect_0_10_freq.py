import json
import os

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

# Find words with frequency count 0-10
freq_0_10_words = []
for word, val in dict_data.items():
    parts = val.split("|")
    freq = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 0
    tr = parts[0].strip()
    if 0 <= freq <= 10:
        freq_0_10_words.append((word, tr, freq))

print(f"Total words with frequency 0-10 in dictionary.json: {len(freq_0_10_words)}")
for w, tr, freq in freq_0_10_words[:30]:
    print(f"{w} -> {tr} | freq: {freq}")
