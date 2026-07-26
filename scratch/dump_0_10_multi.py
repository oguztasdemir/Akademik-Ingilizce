import json
import os

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

freq_0_10_multi = []
for word, val in dict_data.items():
    parts = val.split("|")
    freq = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 0
    tr = parts[0].strip()
    if 0 <= freq <= 10:
        meanings = [m.strip() for m in tr.split(",")]
        if len(meanings) > 1:
            freq_0_10_multi.append((word, meanings, freq))

with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\multi_0_10_translations.txt", "w", encoding="utf-8") as f:
    for word, trs, freq in sorted(freq_0_10_multi, key=lambda x: x[0]):
        f.write(f"{word:25} | {trs} | freq: {freq}\n")

print(f"Dumped {len(freq_0_10_multi)} words to multi_0_10_translations.txt")
