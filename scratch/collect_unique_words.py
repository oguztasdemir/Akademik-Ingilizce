import os
import json

base_dir = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen"

all_words = set()

# 1. dictionary.json
dict_path = os.path.join(base_dir, "dictionary.json")
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for w in data.keys():
            all_words.add(w.strip().lower())

# Helper to traverse and collect words
def collect_from_dir(subdir, word_keys, tr_keys):
    dir_path = os.path.join(base_dir, subdir)
    if not os.path.exists(dir_path):
        return
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".json") and file != "00_genel.json":
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = json.load(f)
                        # Could be list or dict
                        items = []
                        if isinstance(content, list):
                            items = content
                        elif isinstance(content, dict):
                            # Check if has 'words' key
                            items = content.get("words", [])
                        
                        for item in items:
                            for k in word_keys:
                                if k in item and isinstance(item[k], str):
                                    all_words.add(item[k].strip().lower())
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

collect_from_dir("kelime_kampi", ["word"], ["tr"])
collect_from_dir("gelismis_kelime_kampi", ["word"], ["tr", "turkish"])
collect_from_dir("yds_kitap", ["word"], ["turkish"])
collect_from_dir("minioyunlar", ["english"], ["turkish"])

print(f"Total unique words across all targeted datasets: {len(all_words)}")
# Let's save the list
with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\all_unique_words.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(all_words)), f, ensure_ascii=False, indent=2)
