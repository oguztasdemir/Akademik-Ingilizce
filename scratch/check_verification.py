import json

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for w in ["star", "iron", "learn", "recycle", "enact", "postpone"]:
    if w in data:
        print(f"{w} -> {data[w]}")
    else:
        print(f"{w} not found in dictionary.json")
