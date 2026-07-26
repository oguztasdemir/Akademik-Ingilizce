import json
import os

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

# Find words with frequency count 0-10 that have multiple meanings
freq_0_10_multi = []
for word, val in dict_data.items():
    parts = val.split("|")
    freq = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 0
    tr = parts[0].strip()
    if 0 <= freq <= 10:
        meanings = [m.strip() for m in tr.split(",")]
        if len(meanings) > 1:
            freq_0_10_multi.append((word, meanings, freq))

print(f"Words with frequency 0-10 and multiple translations: {len(freq_0_10_multi)}")
for w, trs, freq in freq_0_10_multi[:40]:
    print(f"{w:20} -> {trs} | freq: {freq}")
