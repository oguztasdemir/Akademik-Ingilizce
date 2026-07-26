import json

with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\multi_translations.json", "r", encoding="utf-8") as f:
    multi_tr = json.load(f)

# Predefined synonym / redundant drops
# (drop_word, when_present_word) -> drops drop_word if when_present_word is in the list
synonym_pairs = [
    ("bilim adamı", "bilim insanı"),
    ("yeryüzü", "dünya"),
    ("alem", "dünya"),
    ("sebep olmak", "neden olmak"),
    ("yol açmak", "neden olmak"),
    ("şart", "koşul"),
    ("vatan", "ülke"),
    ("memleket", "ülke"),
    ("fert", "birey"),
    ("şahıs", "birey"),
    ("hadise", "olay"),
    ("enstrüman", "alet"),
    ("enstrüman", "cihaz"),
    ("enstrüman", "araç"),
    ("gemi", "damar"),
    ("gemi", "kap"),
    ("roman", "yeni"),
    ("roman", "özgün"),
    ("idam etmek", "yürütmek"),
    ("idam etmek", "uygulamak"),
    ("istihbarat", "zeka"),
    ("istihbarat", "akıl"),
    ("geçit", "paragraf"),
    ("geçit", "metin"),
    ("takas etmek", "değiştirmek"),
    ("takas etmek", "değişmek"),
    ("anlaşılmak", "okumak"),
    ("tüketmek", "kullanmak"),
    ("tüketmek", "yararlanmak"),
    ("yaraşmak", "olmak"),
    ("yaraşmak", "hale gelmek"),
    ("başrol oynamak", "yıldız"),
    ("ütü", "demir"),
    ("bellemek", "öğrenmek"),
    ("geri dönüşüm sağlamak", "geri dönüştürmek"),
    ("canlandırmak", "yasalaştırmak"),
    ("tehir etmek", "ertelemek"),
    ("transportasyon", "taşıma"),
    ("ileti", "mesaj"),
    ("yorumlama", "yorum"),
    ("alan", "bölge"),
    ("ikaz etmek", "uyarmak"),
]

def clean_translation_list(word, meanings):
    # Direct manual overrides for specific words
    direct_overrides = {
        "learn": ["öğrenmek"],
        "enact": ["yasalaştırmak"],
        "warn": ["uyarmak"]
    }
    word_lower = word.lower().strip()
    if word_lower in direct_overrides:
        return direct_overrides[word_lower]

    # 1. Normalize list: strip and lowercase for comparisons
    meanings = [m.strip() for m in meanings if m.strip()]
    
    # 2. Comparative drop (e.g. drop "daha yüksek" if "yüksek" is present)
    cleaned = []
    for m in meanings:
        if m.startswith("daha "):
            base = m[5:].strip()
            if base in meanings:
                continue
        cleaned.append(m)
    
    # 3. Preposition duplicate drop (e.g. drop "göre" if "-e göre" is present)
    temp = []
    for m in cleaned:
        if not m.startswith("-"):
            dash_form_e = f"-e {m}"
            dash_form_a = f"-a {m}"
            if dash_form_e in cleaned or dash_form_a in cleaned:
                continue
        temp.append(m)
    cleaned = temp

    # 4. Synonym drops
    for drop, keep in synonym_pairs:
        if keep in cleaned and drop in cleaned:
            cleaned.remove(drop)
            
    # 5. Verb stem and tense drops (e.g. drop "oku" or "oldu" when "okumak" or "olmak" are present)
    infinitives = {m for m in cleaned if m.endswith('mak') or m.endswith('mek')}
    temp = []
    for m in cleaned:
        is_redundant = False
        for inf in infinitives:
            stem = inf[:-3]
            # check stem (e.g., "oku" from "okumak")
            if m == stem:
                is_redundant = True
                break
            # check past tense (e.g. "oldu" from "olmak", "gelişti" from "gelişmek")
            past_tenses = [stem + suffix for suffix in ["du", "dü", "dı", "di", "tu", "tü", "tı", "ti"]]
            if m in past_tenses:
                is_redundant = True
                break
            # check continuous (e.g. "büyüyor" from "büyümek")
            if m == stem + "yor" or m == stem[:-1] + "iyor" or m == stem[:-1] + "üyor":
                is_redundant = True
                break
        if not is_redundant:
            temp.append(m)
    cleaned = temp
    
    # 6. Limit to max 2 meanings
    cleaned = cleaned[:2]
    
    return cleaned

simplified_multi = {}
for w, trs in multi_tr.items():
    simplified_multi[w] = clean_translation_list(w, trs)

with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\simplified_multi_translations.json", "w", encoding="utf-8") as f:
    json.dump(simplified_multi, f, ensure_ascii=False, indent=2)

# Print a preview of what changed
print("Preview of simplified multi-translations:")
count = 0
for w in sorted(multi_tr.keys()):
    original = multi_tr[w]
    simplified = simplified_multi[w]
    if original != simplified:
        print(f"{w:25} | Original: {original} -> Simplified: {simplified}")
        count += 1
print(f"Total words modified in multi-translations: {count}")
