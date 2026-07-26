import os
import json

base_dir = r"c:\Users\User\Desktop\Akamik İngilizce Uygulamaları\Dataset\yokdil\fen"
# Note the directory path has a typo in original run or it is correct?
# Ah, the root path is: r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen"
base_dir = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen"

word_translations = {}

def add_translation(word, tr_str):
    if not word or not tr_str:
        return
    word = word.strip().lower()
    
    # Split by common delimiters
    delimiters = [',', '\n', ';', '/']
    temp_str = tr_str
    for d in delimiters:
        temp_str = temp_str.replace(d, '|||')
    meanings = [m.strip() for m in temp_str.split('|||') if m.strip()]
    
    if word not in word_translations:
        word_translations[word] = []
    
    for m in meanings:
        m_lower = m.lower()
        # Find if this meaning (case-insensitive check) is already added
        exists = False
        for existing in word_translations[word]:
            if existing.lower() == m_lower:
                exists = True
                break
        if not exists:
            word_translations[word].append(m)

# 1. dictionary.json (highest priority for ordering)
dict_path = os.path.join(base_dir, "dictionary.json")
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for w, val in data.items():
            parts = val.split("|")
            tr_part = parts[0].strip()
            add_translation(w, tr_part)

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
                        items = []
                        if isinstance(content, list):
                            items = content
                        elif isinstance(content, dict):
                            items = content.get("words", [])
                        
                        for item in items:
                            word = None
                            for wk in word_keys:
                                if wk in item:
                                    word = item[wk]
                                    break
                            if not word:
                                continue
                            
                            for tk in tr_keys:
                                if tk in item and isinstance(item[tk], str):
                                    add_translation(word, item[tk])
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

collect_from_dir("kelime_kampi", ["word"], ["tr"])
collect_from_dir("gelismis_kelime_kampi", ["word"], ["tr", "turkish"])
collect_from_dir("yds_kitap", ["word"], ["turkish"])
collect_from_dir("minioyunlar", ["english"], ["turkish"])

# Filter out words with multiple translations
multi_tr_words = {w: trs for w, trs in word_translations.items() if len(trs) > 1}
print(f"Total unique words: {len(word_translations)}")
print(f"Words with multiple translations: {len(multi_tr_words)}")

with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\multi_translations.json", "w", encoding="utf-8") as f:
    json.dump(multi_tr_words, f, ensure_ascii=False, indent=2)
