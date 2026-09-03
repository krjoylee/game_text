// engine/src/state.rs
// 게임 상태 머신 및 진행 관리

use crate::loader::LoadedPack;
use crate::model::{Choice, Scene};

#[derive(Debug, Clone)]
pub struct ChoiceRecord {
    pub act: u32,
    pub act_name: String,
    pub scene_id: String,
    pub choice_id: String,
    pub choice_text: String,
    pub delta: i32,
    pub resulting_metric: i32,
}

#[derive(Debug, Clone)]
pub struct GameState {
    pub pack: LoadedPack,
    pub current_scene_id: String,
    pub metric_value: i32,
    pub current_tone: String,
    pub current_mode: String,
    pub history: Vec<ChoiceRecord>,
    pub checkpoint_scene_id: String,
    pub is_finished: bool,
    pub game_over: bool,
}

impl GameState {
    pub fn new(pack: LoadedPack) -> Self {
        let initial_scene_id = pack.initial_scene_id.clone();
        let initial_metric = pack.meta.world.metric.initial;
        let default_tone = pack.meta.default_tone.clone();

        Self {
            pack,
            current_scene_id: initial_scene_id.clone(),
            metric_value: initial_metric,
            current_tone: if default_tone.is_empty() { "casual".to_string() } else { default_tone },
            current_mode: "full".to_string(),
            history: Vec::new(),
            checkpoint_scene_id: initial_scene_id,
            is_finished: false,
            game_over: false,
        }
    }

    pub fn current_scene(&self) -> Option<&Scene> {
        self.pack.scenes.get(&self.current_scene_id)
    }

    pub fn set_tone(&mut self, tone: String) {
        self.current_tone = tone;
    }

    pub fn set_mode(&mut self, mode: String) {
        self.current_mode = mode;
    }

    pub fn jump_by_password(&mut self, password: &str) -> bool {
        let trimmed = password.trim();
        for chapter in &self.pack.meta.structure.chapters {
            if let Some(pw) = &chapter.password {
                if pw.trim().eq_ignore_ascii_case(trimmed) {
                    if let Some(first_scene) = chapter.scenes.first() {
                        self.current_scene_id = first_scene.clone();
                        self.checkpoint_scene_id = first_scene.clone();
                        return true;
                    }
                }
            }
        }
        false
    }

    pub fn apply_choice(&mut self, choice: &Choice) {
        let delta = choice.get_metric_delta();
        self.metric_value += delta;

        // 범위 클램핑 (0 ~ max)
        let max_val = self.pack.meta.world.metric.max;
        if self.metric_value > max_val {
            self.metric_value = max_val;
        }

        let scene = self.current_scene();
        let act = scene.map(|s| s.act).unwrap_or(1);
        let act_name = scene.map(|s| s.act_name.clone()).unwrap_or_default();

        let choice_text = choice.text.get_for_tone(&self.current_tone);

        self.history.push(ChoiceRecord {
            act,
            act_name,
            scene_id: self.current_scene_id.clone(),
            choice_id: choice.id.clone(),
            choice_text,
            delta,
            resulting_metric: self.metric_value,
        });

        // 씬 이동
        self.advance_to(&choice.next_scene);
    }

    pub fn advance_to(&mut self, next_scene_id: &str) {
        if next_scene_id == "ending" || next_scene_id.is_empty() {
            self.is_finished = true;
            return;
        }

        if let Some(scene) = self.pack.scenes.get(next_scene_id) {
            // 챕터가 바뀌면 체크포인트 갱신
            if let Some(curr) = self.current_scene() {
                if scene.act != curr.act {
                    self.checkpoint_scene_id = next_scene_id.to_string();
                }
            }
            self.current_scene_id = next_scene_id.to_string();
        } else {
            // 다음 씬이 없으면 엔딩 처리
            self.is_finished = true;
        }
    }

    pub fn check_failure(&self) -> bool {
        self.metric_value <= 0
    }

    pub fn handle_failure_return(&mut self) {
        // 씬 커스텀 on_fail.return_to 가 있으면 우선 적용
        let custom_return = self.current_scene().and_then(|s| s.on_fail.as_ref()).and_then(|of| of.return_to.as_ref());
        if let Some(target) = custom_return {
            self.current_scene_id = target.clone();
            self.metric_value = (self.metric_value).max(1);
            return;
        }

        let strategy = self
            .pack
            .meta
            .world
            .failure
            .as_ref()
            .map(|f| f.return_strategy.as_str())
            .unwrap_or("scene_retry");

        match strategy {
            "chapter_start" => {
                self.current_scene_id = self.checkpoint_scene_id.clone();
                self.metric_value = self.pack.meta.world.metric.initial;
            }
            "game_over" => {
                self.game_over = true;
                self.is_finished = true;
            }
            _ => {
                // scene_retry: 현재 씬 유지 및 수치 1 회복
                self.metric_value = (self.metric_value).max(1);
            }
        }
    }
}
