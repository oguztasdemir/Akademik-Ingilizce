import json
import os

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

print(f"Total words in dictionary.json: {len(dict_data)}")

# Let's inspect some words with 3 or more meanings (split by comma)
long_translations = []
for word, val in dict_data.items():
    # val format: "translation | count"
    parts = val.split("|")
    tr_part = parts[0].strip()
    meanings = [m.strip() for m in tr_part.split(",")]
    if len(meanings) >= 3:
        long_translations.append((word, meanings))

print(f"Words with 3 or more meanings: {len(long_translations)}")
for w, m in long_translations[:30]:
    print(f"{w} -> {m}")
