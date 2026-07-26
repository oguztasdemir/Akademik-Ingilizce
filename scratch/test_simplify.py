import json

dict_path = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\Dataset\yokdil\fen\dictionary.json"

with open(dict_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

def simplify_tr(tr_str):
    if not tr_str:
        return []
    
    # Split by common delimiters
    delimiters = [',', '\n', ';', '/']
    temp_str = tr_str
    for d in delimiters:
        temp_str = temp_str.replace(d, '|||')
    meanings = [m.strip() for m in temp_str.split('|||') if m.strip()]
    
    # Remove duplicates
    cleaned = []
    seen = set()
    for m in meanings:
        m_lower = m.lower()
        if m_lower in seen:
            continue
        seen.add(m_lower)
        cleaned.append(m)
        
    # Remove redundant verb stems (e.g. "oku" when "okumak" is present)
    final_meanings = []
    infinitives = {m.lower() for m in cleaned if m.lower().endswith('mak') or m.lower().endswith('mek')}
    for m in cleaned:
        m_lower = m.lower()
        is_redundant_stem = False
        for inf in infinitives:
            stem = inf[:-3]
            if m_lower == stem:
                is_redundant_stem = True
                break
        if not is_redundant_stem:
            final_meanings.append(m)
            
    # Limit to max 2 meanings
    final_meanings = final_meanings[:2]
    return final_meanings

preview_changes = []
for word, val in dict_data.items():
    parts = val.split("|")
    tr_part = parts[0].strip()
    freq_part = parts[1].strip() if len(parts) > 1 else ""
    
    simplified = simplify_tr(tr_part)
    simplified_str = ", ".join(simplified)
    
    if tr_part != simplified_str:
        preview_changes.append((word, tr_part, simplified_str))

print(f"Total changes: {len(preview_changes)}")
with open(r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları\scratch\simplified_preview.txt", "w", encoding="utf-8") as f:
    for word, original, simplified in preview_changes:
        f.write(f"{word:25} | Original: {original:50} | Simplified: {simplified}\n")
