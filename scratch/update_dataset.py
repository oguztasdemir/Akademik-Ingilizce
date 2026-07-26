import os
import json

base_dir = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen"

# Load the simplified translations map
with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\simplified_multi_translations.json", "r", encoding="utf-8") as f:
    simplified_map = json.load(f)

# Stats counters
files_updated = 0
words_updated = 0

# 1. Update dictionary.json
dict_path = os.path.join(base_dir, "dictionary.json")
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated = False
    for word, val in data.items():
        w_lower = word.strip().lower()
        if w_lower in simplified_map:
            parts = val.split("|")
            freq_part = parts[1].strip() if len(parts) > 1 else ""
            
            new_tr = ", ".join(simplified_map[w_lower])
            new_val = f"{new_tr} | {freq_part}" if freq_part else new_tr
            
            if val != new_val:
                data[word] = new_val
                updated = True
                words_updated += 1
                
    if updated:
        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Updated dictionary.json")
        files_updated += 1

# Helper to traverse directories and update files
def update_dir(subdir, word_keys, tr_keys, delimiter="\n"):
    global files_updated, words_updated
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
                    
                    file_modified = False
                    
                    # Determine structure
                    if isinstance(content, list):
                        items = content
                    elif isinstance(content, dict) and "words" in content:
                        items = content["words"]
                    else:
                        continue
                        
                    for item in items:
                        word_val = None
                        word_key_found = None
                        for wk in word_keys:
                            if wk in item and isinstance(item[wk], str):
                                word_val = item[wk].strip().lower()
                                word_key_found = wk
                                break
                        if not word_val or word_val not in simplified_map:
                            continue
                            
                        # Word matches a simplified translation word!
                        simplified_trs = simplified_map[word_val]
                        new_tr_str = delimiter.join(simplified_trs)
                        
                        for tk in tr_keys:
                            if tk in item:
                                if item[tk] != new_tr_str:
                                    item[tk] = new_tr_str
                                    file_modified = True
                                    words_updated += 1
                                    
                    if file_modified:
                        with open(filepath, "w", encoding="utf-8") as f:
                            json.dump(content, f, ensure_ascii=False, indent=2)
                        files_updated += 1
                except Exception as e:
                    print(f"Error updating {filepath}: {e}")

# 2. Update kelime_kampi
update_dir("kelime_kampi", ["word"], ["tr"])

# 3. Update gelismis_kelime_kampi
update_dir("gelismis_kelime_kampi", ["word"], ["tr", "turkish"])

# 4. Update yds_kitap
update_dir("yds_kitap", ["word"], ["turkish"])

# 5. Update minioyunlar
update_dir("minioyunlar", ["english"], ["turkish"])

print(f"\nUpdate complete!")
print(f"Total files written/updated: {files_updated}")
print(f"Total word translation records updated: {words_updated}")
