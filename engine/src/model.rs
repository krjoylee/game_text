// engine/src/model.rs
// Divina Ludus 데이터 모델 정의 (Zero Dependency)

use std::collections::HashMap;

#[derive(Debug, Clone, Default)]
pub struct PackMeta {
    pub id: String,
    pub title: String,
    pub author: String,
    pub description: String,
    pub language: String,
    pub default_tone: String,
    pub tones: HashMap<String, ToneConfig>,
    pub world: WorldConfig,
    pub structure: StructureConfig,
    pub modes: HashMap<String, ModeConfig>,
    pub characters: CharactersConfig,
    pub endings: Vec<EndingConfig>,
}

#[derive(Debug, Clone, Default)]
pub struct ToneConfig {
    pub name: String,
    pub description: String,
}

#[derive(Debug, Clone, Default)]
pub struct WorldConfig {
    pub metric: MetricConfig,
    pub chapter_term: String,
    pub chapter_term_en: String,
    pub failure: Option<FailureConfig>,
    pub password: Option<PasswordConfig>,
}

#[derive(Debug, Clone)]
pub struct MetricConfig {
    pub name: String,
    pub name_en: String,
    pub icon: String,
    pub max: i32,
    pub initial: i32,
    pub description: String,
}

impl Default for MetricConfig {
    fn default() -> Self {
        Self {
            name: "선행의 씨앗".to_string(),
            name_en: "Seeds of Virtue".to_string(),
            icon: "♧".to_string(),
            max: 10,
            initial: 3,
            description: "".to_string(),
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct FailureConfig {
    pub speaker: String,
    pub message_key: String,
    pub return_strategy: String,
}

#[derive(Debug, Clone, Default)]
pub struct PasswordConfig {
    pub enabled: bool,
    pub description: String,
}

#[derive(Debug, Clone)]
pub struct StructureConfig {
    pub structure_type: String,
    pub chapters: Vec<ChapterConfig>,
}

impl Default for StructureConfig {
    fn default() -> Self {
        Self {
            structure_type: "linear".to_string(),
            chapters: Vec::new(),
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct ChapterConfig {
    pub id: String,
    pub name: String,
    pub password: Option<String>,
    pub scenes: Vec<String>,
    pub standalone: Option<bool>,
}

#[derive(Debug, Clone, Default)]
pub struct ModeConfig {
    pub name: String,
    pub description: String,
    pub chapters: Vec<String>,
}

#[derive(Debug, Clone, Default)]
pub struct CharactersConfig {
    pub protagonist: Option<CharacterInfo>,
    pub antagonist: Option<CharacterInfo>,
    pub guide: Option<CharacterInfo>,
    pub support: Vec<CharacterInfo>,
}

#[derive(Debug, Clone, Default)]
pub struct CharacterInfo {
    pub id: String,
    pub name: String,
    pub icon: String,
}

#[derive(Debug, Clone, Default)]
pub struct EndingConfig {
    pub id: String,
    pub name: String,
    pub min_virtue: i32,
    pub description: String,
}

#[derive(Debug, Clone, Default)]
pub struct Scene {
    pub scene_id: String,
    pub act: u32,
    pub act_name: String,
    pub title: String,
    pub theme: String,
    pub message: String,
    pub is_interpreted: bool,
    pub is_transition: bool,
    pub scene_art: Vec<String>,
    pub animation: Option<AnimationConfig>,
    pub card_template: Vec<String>,
    pub dialogue: HashMap<String, Vec<DialogueLine>>,
    pub substitutions: HashMap<String, HashMap<String, String>>,
    pub choices: Vec<Choice>,
    pub next_scene: Option<String>,
    pub on_fail: Option<OnFailConfig>,
}

#[derive(Debug, Clone, Default)]
pub struct AnimationConfig {
    pub frame_rate_ms: u64,
    pub loop_anim: bool,
    pub frames: Vec<Vec<String>>,
}

#[derive(Debug, Clone, Default)]
pub struct DialogueLine {
    pub speaker: String,
    pub text: String,
}

#[derive(Debug, Clone, Default)]
pub struct Choice {
    pub id: String,
    pub text: ChoiceText,
    pub virtue_change: i32,
    pub light_change: Option<i32>,
    pub next_scene: String,
}

impl Choice {
    pub fn get_metric_delta(&self) -> i32 {
        if self.virtue_change != 0 {
            self.virtue_change
        } else {
            self.light_change.unwrap_or(0)
        }
    }
}

#[derive(Debug, Clone)]
pub enum ChoiceText {
    Simple(String),
    MultiTone(HashMap<String, String>),
}

impl Default for ChoiceText {
    fn default() -> Self {
        ChoiceText::Simple(String::new())
    }
}

impl ChoiceText {
    pub fn get_for_tone(&self, tone: &str) -> String {
        match self {
            ChoiceText::Simple(s) => s.clone(),
            ChoiceText::MultiTone(map) => {
                // tone_casual / casual 양쪽 키 유연하게 조회
                let prefixed = if tone.starts_with("tone_") {
                    tone.to_string()
                } else {
                    format!("tone_{}", tone)
                };
                let raw = tone.trim_start_matches("tone_");

                if let Some(txt) = map.get(&prefixed) {
                    txt.clone()
                } else if let Some(txt) = map.get(raw) {
                    txt.clone()
                } else if let Some(txt) = map.get("tone_casual") {
                    txt.clone()
                } else if let Some(txt) = map.get("casual") {
                    txt.clone()
                } else if let Some((_, txt)) = map.iter().next() {
                    txt.clone()
                } else {
                    "".to_string()
                }
            }
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct OnFailConfig {
    pub speaker: String,
    pub text: Option<FailText>,
    pub return_to: Option<String>,
}

#[derive(Debug, Clone)]
pub enum FailText {
    Simple(String),
    MultiTone(HashMap<String, String>),
}
