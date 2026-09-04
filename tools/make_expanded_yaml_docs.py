#!/usr/bin/env python3
"""
tools/make_expanded_yaml_docs.py
신규 7대 팩의 1-1_story_structure.md, 2_conti.md, 3_scene.yaml 자동 문서 생성기
"""

import os
import sys
import yaml
sys.path.append("/home/krjoylee/code/game/tools")
from make_expanded_data import (
    build_charlie_pack, build_matilda_pack, build_animal_farm_pack,
    build_1984_pack, build_under_wheel_pack, build_dante_comedy_pack,
    build_zarathustra_pack
)

packs_factories = [
    ("charlie_chocolate", build_charlie_pack),
    ("matilda", build_matilda_pack),
    ("animal_farm", build_animal_farm_pack),
    ("nineteen_eighty_four", build_1984_pack),
    ("under_wheel", build_under_wheel_pack),
    ("dante_comedy", build_dante_comedy_pack),
    ("zarathustra", build_zarathustra_pack),
]

for dirname, factory in packs_factories:
    pdata = factory()
    base_dir = f"/home/krjoylee/code/game/packs/{dirname}"
    os.makedirs(base_dir, exist_ok=True)
    
    # 1. 1-1_story_structure.md
    mermaid_lines = ["graph TD"]
    for i in range(len(pdata["scenes"])):
        sc = pdata["scenes"][i]
        curr_id = f"S{sc['act']}"
        title_esc = sc['title'].replace(':', ' ').replace('"', "'")
        mermaid_lines.append(f'    {curr_id}["제{sc["act"]}막: {title_esc}"]')
        if i + 1 < len(pdata["scenes"]):
            next_id = f"S{pdata['scenes'][i+1]['act']}"
            if sc.get("is_transition"):
                mermaid_lines.append(f'    {curr_id} -->|"Enter: 진행"| {next_id}')
            else:
                mermaid_lines.append(f'    {curr_id} -->|"선택지 분기"| {next_id}')
        else:
            mermaid_lines.append(f'    {curr_id} -->|"최종 정산"| END["3대 엔딩 달성"]')

    mermaid_str = "\n".join(mermaid_lines)

    struct_md = f"""# 《{pdata['title']}》 — 이야기 구조 및 철학 설계서 (1-1단계)

> **원작**: {pdata['tier_desc']}  
> **난이도 등급**: `{pdata['tier']}` ({pdata['tier_name']})  
> **총 막/씬 수**: {len(pdata['scenes'])}개 막 완결  
> **고유 메트릭**: **`{pdata['metric_name']}`** {pdata['metric_icon']} (0 ~ 10, 기본값: 3)

---

## 1. 팩 핵심 서사 철학 및 메타데이터

* **제목**: {pdata['title']}
* **분류**: {pdata['tier_name']}
* **핵심 철학**: {pdata['tier_desc']}
* **메트릭 규칙**: 양심과 성찰에 부합하는 선택 시 +1~+3, 나태·굴복·독재·외면 시 -1~-3

---

## 2. 머메이드 서사 구조도 (Scene Graph & Flow)

```mermaid
{mermaid_str}
```

---

## 3. 엔딩 3대 성향 분석 (Ending Profiles)

| 엔딩 명칭 | 최소 메트릭 | 설명 |
|---|:---:|---|
| **{pdata['endings'][0]['title']}** | {pdata['endings'][0]['min']} | {pdata['endings'][0]['desc']} |
| **{pdata['endings'][1]['title']}** | {pdata['endings'][1]['min']} | {pdata['endings'][1]['desc']} |
| **{pdata['endings'][2]['title']}** | {pdata['endings'][2]['min']} | {pdata['endings'][2]['desc']} |
"""
    with open(f"{base_dir}/1-1_story_structure.md", "w", encoding="utf-8") as f:
        f.write(struct_md)

    # 2. 2_conti.md
    conti_lines = [f"# 《{pdata['title']}》 — 콘티 및 시나리오 규격서 (2단계)\n",
                   f"> **난이도**: {pdata['tier_name']} | **총 막 수**: {len(pdata['scenes'])}개 막 | **메트릭**: {pdata['metric_name']} {pdata['metric_icon']}\n",
                   "---\n"]
    for sc in pdata["scenes"]:
        conti_lines.append(f"### 제{sc['act']}막: {sc['title']}\n")
        conti_lines.append(f"* **화자**: {sc['speaker']}\n")
        conti_lines.append(f"* **대화 스크립트 (현대어 티키타카)**:\n```text\n{sc['text']}\n```\n")
        conti_lines.append(f"* **💡 [0]번 지혜의 사색 힌트 노트**: *\"{sc['hint']}\"*\n")
        if sc.get("is_transition"):
            conti_lines.append(f"* **전환 진행 버튼**: `[Enter] {sc['button_text']}`\n\n")
        else:
            conti_lines.append("* **선택지 및 메트릭 변동**:\n")
            for c in sc["choices"]:
                conti_lines.append(f"  - \"{c['text']}\" ({c['delta']}) ➔ {c['feedback']}\n")
            conti_lines.append("\n")

    with open(f"{base_dir}/2_conti.md", "w", encoding="utf-8") as f:
        f.write("".join(conti_lines))

    # 3. 3_scene.yaml
    clean_scenes = []
    for sc in pdata["scenes"]:
        csc = {
            "act": sc["act"],
            "title": sc["title"],
            "speaker": sc["speaker"],
            "dialogue": sc["text"],
            "hint": sc["hint"],
            "is_transition": sc["is_transition"]
        }
        if sc.get("is_transition"):
            csc["button_text"] = sc["button_text"]
        else:
            csc["choices"] = sc["choices"]
        clean_scenes.append(csc)

    yaml_data = {
        "pack": {
            "id": pdata["id"],
            "title": pdata["title"],
            "difficulty": {
                "tier": pdata["tier"],
                "name": pdata["tier_name"],
                "description": pdata["tier_desc"]
            },
            "world": {
                "metric": {
                    "name": pdata["metric_name"],
                    "icon": pdata["metric_icon"],
                    "initial": pdata.get("metric_initial", 3),
                    "max": pdata.get("metric_max", 10)
                }
            },
            "endings": pdata["endings"]
        },
        "scenes": clean_scenes
    }

    with open(f"{base_dir}/3_scene.yaml", "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

print("Generated 1-1_story_structure.md, 2_conti.md, and 3_scene.yaml for all 7 expanded packs!")
