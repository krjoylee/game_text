// engine/src/loader.rs
// 팩 및 씬 로딩 모듈 (Zero Dependency)

use crate::model::*;
use crate::yaml_parser::{parse_yaml, YamlValue};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Debug, Clone)]
pub struct LoadedPack {
    pub meta: PackMeta,
    pub scenes: HashMap<String, Scene>,
    pub initial_scene_id: String,
}

pub fn load_pack_from_path(pack_path: &Path) -> Result<LoadedPack, String> {
    if !pack_path.exists() {
        return Err(format!("경로가 존재하지 않습니다: {:?}", pack_path));
    }

    let target_file = if pack_path.is_file() {
        pack_path.to_path_buf()
    } else {
        let candidates = [
            pack_path.join("4_game_scene.yaml"),
            pack_path.join("3_scene.yaml"),
            pack_path.join("pack.yaml"),
        ];

        let mut found = None;
        for c in &candidates {
            if c.exists() {
                found = Some(c.clone());
                break;
            }
        }

        found.ok_or_else(|| {
            format!(
                "팩 설정 파일을 찾을 수 없습니다: {:?} (4_game_scene.yaml, 3_scene.yaml, pack.yaml)",
                pack_path
            )
        })?
    };

    let content = fs::read_to_string(&target_file)
        .map_err(|e| format!("파일 읽기 실패 ({:?}): {}", target_file, e))?;

    let root_val = parse_yaml(&content)
        .map_err(|e| format!("YAML 파싱 실패 ({:?}): {}", target_file, e))?;

    let pack_meta = parse_pack_meta(&root_val)?;
    let scenes = parse_scenes(&root_val);

    let mut scene_map = HashMap::new();
    let mut first_scene_id = None;

    for s in scenes {
        if first_scene_id.is_none() {
            first_scene_id = Some(s.scene_id.clone());
        }
        scene_map.insert(s.scene_id.clone(), s);
    }

    let initial_scene_id = pack_meta
        .structure
        .chapters
        .first()
        .and_then(|ch| ch.scenes.first().cloned())
        .or(first_scene_id)
        .unwrap_or_else(|| "scene_01".to_string());

    Ok(LoadedPack {
        meta: pack_meta,
        scenes: scene_map,
        initial_scene_id,
    })
}

fn parse_pack_meta(root: &YamlValue) -> Result<PackMeta, String> {
    let p = root.get("pack").unwrap_or(root);

    let id = p.get_str("id").unwrap_or("heungbu_nolbu").to_string();
    let title = p.get_str("title").unwrap_or("고전문학 게임").to_string();
    let author = p.get_str("author").unwrap_or("작자 미상").to_string();
    let description = p.get_str("description").unwrap_or("").to_string();
    let language = p.get_str("language").unwrap_or("ko").to_string();

    // 문체 파싱
    let mut tones = HashMap::new();
    let mut default_tone = String::new();

    if let Some(tones_map) = p.get("tones").and_then(|v| v.as_map()) {
        if let Some(def_val) = tones_map.get("default").and_then(|v| v.as_str()) {
            default_tone = def_val.to_string();
        }
        for (k, v) in tones_map {
            if k == "default" {
                continue;
            }
            let name = v.get_str("name").unwrap_or(k).to_string();
            let desc = v.get_str("description").unwrap_or("").to_string();
            tones.insert(k.clone(), ToneConfig { name, description: desc });
        }
    }
    if tones.is_empty() {
        tones.insert(
            "casual".to_string(),
            ToneConfig {
                name: "현대 구어체".to_string(),
                description: "친근한 대화체".to_string(),
            },
        );
    }
    if default_tone.is_empty() {
        default_tone = if tones.contains_key("casual") {
            "casual".to_string()
        } else {
            tones.keys().next().cloned().unwrap_or_else(|| "casual".to_string())
        };
    }

    // 세계관 및 수치 파싱
    let world_v = p.get("world");
    let mut metric = MetricConfig::default();
    let mut chapter_term = "막".to_string();
    let mut chapter_term_en = "Act".to_string();
    let mut failure = None;
    let mut password = Some(PasswordConfig {
        enabled: true,
        description: "암호 입력".to_string(),
    });

    if let Some(w) = world_v {
        if let Some(ct) = w.get_str("chapter_term") {
            chapter_term = ct.to_string();
        }
        if let Some(cte) = w.get_str("chapter_term_en") {
            chapter_term_en = cte.to_string();
        }
        if let Some(m) = w.get("metric") {
            metric.name = m.get_str("name").unwrap_or("선행의 씨앗").to_string();
            metric.name_en = m.get_str("name_en").unwrap_or("Seeds of Virtue").to_string();
            metric.icon = m.get_str("icon").unwrap_or("♧").to_string();
            metric.max = m.get_i32("max").unwrap_or(10);
            metric.initial = m.get_i32("initial").unwrap_or(3);
            metric.description = m.get_str("description").unwrap_or("").to_string();
        }
        if let Some(f) = w.get("failure") {
            failure = Some(FailureConfig {
                speaker: f.get_str("speaker").unwrap_or("").to_string(),
                message_key: f.get_str("message_key").unwrap_or("").to_string(),
                return_strategy: f.get_str("return_strategy").unwrap_or("scene_retry").to_string(),
            });
        }
        if let Some(pw) = w.get("password") {
            password = Some(PasswordConfig {
                enabled: pw.get_bool("enabled").unwrap_or(true),
                description: pw.get_str("description").unwrap_or("암호 입력").to_string(),
            });
        }
    }

    let world = WorldConfig {
        metric,
        chapter_term,
        chapter_term_en,
        failure,
        password,
    };

    // 서사 구조 파싱
    let mut chapters = Vec::new();
    let mut structure_type = "linear".to_string();

    if let Some(struct_v) = p.get("structure") {
        if let Some(st) = struct_v.get_str("type") {
            structure_type = st.to_string();
        }
        if let Some(ch_list) = struct_v.get("chapters").and_then(|v| v.as_list()) {
            for ch_item in ch_list {
                let ch_id = ch_item.get_str("id").unwrap_or("").to_string();
                let ch_name = ch_item.get_str("name").unwrap_or("").to_string();
                let password = ch_item.get_str("password").map(|s| s.to_string());
                let scenes = ch_item
                    .get("scenes")
                    .and_then(|v| v.as_list())
                    .map(|l| l.iter().filter_map(|x| x.as_str().map(|s| s.to_string())).collect())
                    .unwrap_or_default();

                chapters.push(ChapterConfig {
                    id: ch_id,
                    name: ch_name,
                    password,
                    scenes,
                    standalone: ch_item.get_bool("standalone"),
                });
            }
        }
    }

    let structure = StructureConfig {
        structure_type,
        chapters,
    };

    // 모드 파싱 (BUG-012)
    let mut modes = HashMap::new();
    if let Some(modes_map) = p.get("modes").and_then(|v| v.as_map()) {
        for (k, v) in modes_map {
            let m_name = v.get_str("name").unwrap_or(k).to_string();
            let m_desc = v.get_str("description").unwrap_or("").to_string();
            let m_chapters = if let Some(ch_list) = v.get("chapters").and_then(|c| c.as_list()) {
                ch_list.iter().filter_map(|x| x.as_str().map(|s| s.to_string())).collect()
            } else if let Some(s) = v.get_str("chapters") {
                vec![s.to_string()]
            } else {
                Vec::new()
            };
            modes.insert(k.clone(), ModeConfig {
                name: m_name,
                description: m_desc,
                chapters: m_chapters,
            });
        }
    }

    // 캐릭터 파싱 (BUG-012)
    let mut characters = CharactersConfig::default();
    if let Some(chars_v) = p.get("characters") {
        let parse_char = |item: &YamlValue| -> Option<CharacterInfo> {
            let id = item.get_str("id")?.to_string();
            let name = item.get_str("name").unwrap_or(&id).to_string();
            let icon = item.get_str("icon").unwrap_or("●").to_string();
            Some(CharacterInfo { id, name, icon })
        };

        if let Some(prot) = chars_v.get("protagonist") {
            characters.protagonist = parse_char(prot);
        }
        if let Some(ant) = chars_v.get("antagonist") {
            characters.antagonist = parse_char(ant);
        }
        if let Some(gd) = chars_v.get("guide") {
            characters.guide = parse_char(gd);
        }
        if let Some(supp_list) = chars_v.get("support").and_then(|v| v.as_list()) {
            for s in supp_list {
                if let Some(ci) = parse_char(s) {
                    characters.support.push(ci);
                }
            }
        }
    }

    // 엔딩 설정 파싱
    let mut endings = Vec::new();
    if let Some(end_list) = p.get("endings").and_then(|v| v.as_list()) {
        for end_item in end_list {
            let end_id = end_item.get_str("id").unwrap_or("").to_string();
            let end_name = end_item.get_str("name").unwrap_or("").to_string();
            let min_virtue = end_item.get_i32("min_virtue").unwrap_or(0);
            let desc = end_item.get_str("description").unwrap_or("").to_string();

            endings.push(EndingConfig {
                id: end_id,
                name: end_name,
                min_virtue,
                description: desc,
            });
        }
    }

    Ok(PackMeta {
        id,
        title,
        author,
        description,
        language,
        default_tone,
        tones,
        world,
        structure,
        modes,
        characters,
        endings,
    })
}

fn parse_scenes(root: &YamlValue) -> Vec<Scene> {
    let mut scenes = Vec::new();

    let scene_list = match root.get("scenes").and_then(|v| v.as_list()) {
        Some(l) => l,
        None => return scenes,
    };

    for s_item in scene_list {
        let scene_id = s_item.get_str("scene_id").unwrap_or("").to_string();
        if scene_id.is_empty() {
            continue;
        }

        let act = (s_item.get_i32("act").unwrap_or(1)).max(1) as u32;
        let act_name = s_item.get_str("act_name").unwrap_or("").to_string();
        let title = s_item.get_str("title").unwrap_or("").to_string();
        let theme = s_item.get_str("theme").unwrap_or("").to_string();
        let message = s_item.get_str("message").unwrap_or("").to_string();
        let is_interpreted = s_item.get_bool("is_interpreted").unwrap_or(false);
        let is_transition = s_item.get_bool("is_transition").unwrap_or(false);
        let next_scene = s_item.get_str("next_scene").map(|s| s.to_string());

        // on_fail 파싱 (BUG-002)
        let on_fail = if let Some(of) = s_item.get("on_fail") {
            let speaker = of.get_str("speaker").unwrap_or("").to_string();
            let text = if let Some(ts) = of.get_str("text") {
                Some(FailText::Simple(ts.to_string()))
            } else if let Some(tm) = of.get("text").and_then(|v| v.as_map()) {
                let mut map = HashMap::new();
                for (k, v) in tm {
                    if let Some(s) = v.as_str() {
                        map.insert(k.clone(), s.to_string());
                    }
                }
                Some(FailText::MultiTone(map))
            } else {
                None
            };
            let return_to = of.get_str("return_to").map(|s| s.to_string());
            Some(OnFailConfig {
                speaker,
                text,
                return_to,
            })
        } else {
            None
        };

        // scene_art / card_template
        let mut scene_art = Vec::new();
        if let Some(art_list) = s_item.get("scene_art").and_then(|v| v.as_list()) {
            for l in art_list {
                if let Some(s) = l.as_str() {
                    scene_art.push(s.to_string());
                }
            }
        }

        let mut card_template = Vec::new();
        if let Some(card_list) = s_item.get("card_template").and_then(|v| v.as_list()) {
            for l in card_list {
                if let Some(s) = l.as_str() {
                    card_template.push(s.to_string());
                }
            }
        }

        // dialogue
        let mut dialogue = HashMap::new();
        if let Some(dlg_map) = s_item.get("dialogue").and_then(|v| v.as_map()) {
            for (tone_k, lines_v) in dlg_map {
                if let Some(lines_list) = lines_v.as_list() {
                    let mut dlg_lines = Vec::new();
                    for line_item in lines_list {
                        let speaker = line_item.get_str("speaker").unwrap_or("").to_string();
                        let text = line_item.get_str("text").unwrap_or("").to_string();
                        dlg_lines.push(DialogueLine { speaker, text });
                    }
                    dialogue.insert(tone_k.clone(), dlg_lines);
                }
            }
        }

        // substitutions
        let mut substitutions = HashMap::new();
        if let Some(sub_map) = s_item.get("substitutions").and_then(|v| v.as_map()) {
            for (tone_k, vars_v) in sub_map {
                if let Some(vars_map) = vars_v.as_map() {
                    let mut inner = HashMap::new();
                    for (k, v) in vars_map {
                        if let Some(s) = v.as_str() {
                            inner.insert(k.clone(), s.to_string());
                        }
                    }
                    substitutions.insert(tone_k.clone(), inner);
                }
            }
        }

        // choices
        let mut choices = Vec::new();
        if let Some(choice_list) = s_item.get("choices").and_then(|v| v.as_list()) {
            for c_item in choice_list {
                let c_id = c_item.get_str("id").unwrap_or("").to_string();
                let c_next = c_item.get_str("next_scene").unwrap_or("").to_string();
                let c_virtue = c_item.get_i32("virtue_change").unwrap_or(0);
                let c_light = c_item.get_i32("light_change");

                let choice_text = if let Some(txt_str) = c_item.get_str("text") {
                    ChoiceText::Simple(txt_str.to_string())
                } else if let Some(txt_map) = c_item.get("text").and_then(|v| v.as_map()) {
                    let mut m = HashMap::new();
                    for (k, v) in txt_map {
                        if let Some(s) = v.as_str() {
                            m.insert(k.clone(), s.to_string());
                        }
                    }
                    ChoiceText::MultiTone(m)
                } else {
                    ChoiceText::Simple(String::new())
                };

                choices.push(Choice {
                    id: c_id,
                    text: choice_text,
                    virtue_change: c_virtue,
                    light_change: c_light,
                    next_scene: c_next,
                });
            }
        }

        // animation 파싱 (6프레임 시네마틱 컷씬)
        let animation = if let Some(anim_map) = s_item.get("animation") {
            let frame_rate_ms = anim_map.get_i32("frame_rate_ms").unwrap_or(300).max(50) as u64;
            let loop_anim = anim_map.get_bool("loop").unwrap_or(false);
            let mut frames = Vec::new();
            if let Some(frame_list) = anim_map.get("frames").and_then(|v| v.as_list()) {
                for f_item in frame_list {
                    if let Some(fl) = f_item.as_list() {
                        let mut frame_lines = Vec::new();
                        for l in fl {
                            if let Some(s) = l.as_str() {
                                frame_lines.push(s.to_string());
                            }
                        }
                        frames.push(frame_lines);
                    }
                }
            }
            if !frames.is_empty() {
                Some(AnimationConfig {
                    frame_rate_ms,
                    loop_anim,
                    frames,
                })
            } else {
                None
            }
        } else {
            None
        };

        scenes.push(Scene {
            scene_id,
            act,
            act_name,
            title,
            theme,
            message,
            is_interpreted,
            is_transition,
            scene_art,
            animation,
            card_template,
            dialogue,
            substitutions,
            choices,
            next_scene,
            on_fail,
        });
    }

    scenes
}
