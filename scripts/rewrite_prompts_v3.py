#!/usr/bin/env python3
"""
v3.6.27 - Final: Clean all prompts in visual_bible.json
- Remove all Chinese characters from prompt_en and video_prompts
- Ensure ALL prompts contain "1998 Chinese TV drama aesthetic" and "cinematic film grain"
- Ensure prompt_en format: [actor-locked description]. High-quality screenshot from the 1998 CCTV TV series "Water Margin", natural lighting, cinematic film grain.
"""
import json, os, re

VB = os.path.expanduser("~/.agentic-os/character_designs/visual_bible.json")
with open(VB) as f:
    d = json.load(f)

changes = 0

def is_chinese(ch):
    return '\u4e00' <= ch <= '\u9fff'

def has_chinese(s):
    return any(is_chinese(ch) for ch in s)

def strip_chinese(s):
    return ''.join(ch for ch in s if not is_chinese(ch) and ch not in '，。！？；：、""''（）【】《》').strip()

def ensure_98_suffix(s, add_cinematic=True):
    """Ensure prompt has required quality suffixes."""
    suffix = "cinematic film grain, 1998 Chinese TV drama aesthetic."
    if add_cinematic:
        suffix = "cinematic film grain, 1998 Chinese TV drama aesthetic."
    else:
        suffix = "1998 Chinese TV drama aesthetic."
    
    # Remove existing suffix variations first
    s = re.sub(r'(cinematic film grain,?\s*)?1998\s*(Chinese\s*)?(TV\s*)?drama\s*(aesthetic|style).?', '', s, flags=re.IGNORECASE)
    s = re.sub(r'(cinematic\s+)?film\s+grain,?\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'cinematic\s+lighting,?\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'High-quality screenshot from the 1998 CCTV TV series "Water Margin",?\s*', '', s, flags=re.IGNORECASE)
    
    s = s.strip().rstrip('.') + '. ' + suffix
    return s.strip()

for cid, char in list(d['characters'].items()):
    name = char.get('name', cid)
    changed = False
    
    # 1. Fix prompt_en
    pe = char.get('prompt_en', '')
    if pe:
        new_pe = strip_chinese(pe)
        if new_pe != pe:
            char['prompt_en'] = new_pe
            changed = True
        # Ensure 1998 suffix
        if '1998' not in char['prompt_en']:
            char['prompt_en'] = ensure_98_suffix(char['prompt_en'])
            # Also add the "High-quality screenshot from" prefix if missing
            if not char['prompt_en'].startswith('High-quality'):
                # Move the prefix to front
                suffix_text = "High-quality screenshot from the 1998 CCTV TV series \"Water Margin\", natural lighting, cinematic film grain."
                # Get just the character description part
                desc_part = re.sub(r'(cinematic film grain,?\s*)?1998\s*(Chinese\s*)?(TV\s*)?drama\s*(aesthetic|style).?', '', char['prompt_en'], flags=re.IGNORECASE).strip().rstrip('.')
                char['prompt_en'] = desc_part + '. ' + suffix_text
            changed = True
        if has_chinese(char['prompt_en']):
            char['prompt_en'] = strip_chinese(char['prompt_en'])
            changed = True
    
    # 2. Fix video_prompts
    vp = char.get('video_prompts', {})
    for scheme_key, scheme in vp.items():
        for text_field in ['prompt', '简练版']:
            txt = scheme.get(text_field, '')
            if not txt:
                continue
            new_txt = strip_chinese(txt)
            if new_txt != txt:
                scheme[text_field] = new_txt
                changed = True
            # Ensure 1998 suffix in prompt (not necessary for short fields)
            if text_field == 'prompt' and '1998' not in scheme['prompt']:
                scheme['prompt'] = ensure_98_suffix(scheme['prompt'])
                changed = True
            if has_chinese(scheme.get(text_field, '')):
                scheme[text_field] = strip_chinese(scheme[text_field])
                changed = True
    
    if changed:
        changes += 1

with open(VB, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print(f"done. modified {changes} chars")

# Verify
with open(VB) as f:
    d = json.load(f)

problems = 0
for cid, char in d['characters'].items():
    pe = char.get('prompt_en', '')
    if has_chinese(pe):
        print(f"  CHINESE in prompt_en: {cid} ({char.get('name','')})")
        problems += 1
    if '1998' not in pe and pe:
        print(f"  NO 1998 in prompt_en: {cid} ({char.get('name','')})")
        problems += 1
    if not pe:
        print(f"  EMPTY prompt_en: {cid} ({char.get('name','')})")
        problems += 1
    
    vp = char.get('video_prompts', {})
    for sk, sv in vp.items():
        txt = sv.get('prompt', '')
        if has_chinese(txt):
            print(f"  CHINESE in {cid} {sk}: {txt[:30]}")
            problems += 1
        if '1998' not in txt:
            print(f"  NO 1998 in {cid} {sk}")
            problems += 1

print(f"Total problems: {problems}")
if problems == 0:
    print("ALL CLEAN!")
