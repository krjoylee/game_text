// engine/src/renderer.rs
// Divina Ludus 2D 가상 화면 그리드 버퍼 렌더러 (Virtual Screen Grid Buffer)
// 78 x 40 고화질 시네마틱 프레임 (Scene Art 23줄 초대형 캔버스)

use crate::model::Scene;
use crate::state::GameState;
use crate::width::{char_width, str_display_width};
use std::collections::HashMap;
use std::io::{self, Write};
use std::thread;
use std::time::Duration;

pub const CARD_WIDTH: usize = 78;
pub const CARD_HEIGHT: usize = 40;

/// 16색 고전 하이브리드 팔레트 (ANSI 256 코드)
pub const PALETTE_ANSI: [u8; 16] = [
    237, // 0: 한옥벽 배경 회갈색 (#3A3A3A)
    16,  // 1: 칠흑 먹선, 갓, 눈썹, 수염 (#000000)
    223, // 2: 뽀샤시한 밝은 살구 피부 (#FFCC99)
    179, // 3: 피부 음영 황토 (#D49B6A)
    186, // 4: 누런 삼베옷 (#C2B280)
    94,  // 5: 누더기 갈색 (#8B5A2B)
    196, // 6: 비단 주홍 깃 (#E74C3C)
    25,  // 7: 비단 군청 도포 (#2471A3)
    81,  // 8: 흥부 눈물 하늘 (#5DADE2)
    231, // 9: 순백 반사광 / 치아 (#FFFFFF)
    31,  // 10: 비단 광택 청록 (#0087AF)
    137, // 11: 거친 삼베 음영 (#AF875F)
    220, // 12: ★ 놀부 황금 앞니 (#F4D03F)
    36,  // 13: 도깨비 녹색
    244, // 14: 쇠몽둥이 회색
    41,  // 15: 화해 들판
];

/// 2D 가상 화면 버퍼 셀 (컬러 버퍼 확장: fg/bg 색상 속성 탑재)
#[derive(Clone, Copy)]
pub struct Cell {
    pub ch: char,
    pub is_continuation: bool, // 2칸 문자(한글/전각)의 두 번째 칸 표시
    pub fg: Option<u8>,        // 전경색 (0..15 인덱스 또는 ANSI 코드)
    pub bg: Option<u8>,        // 배경색 (0..15 인덱스 또는 ANSI 코드)
}

impl Cell {
    pub fn new(ch: char) -> Self {
        Self {
            ch,
            is_continuation: false,
            fg: None,
            bg: None,
        }
    }
}

impl Default for Cell {
    fn default() -> Self {
        Self {
            ch: ' ',
            is_continuation: false,
            fg: None,
            bg: None,
        }
    }
}

/// 2D 가상 화면 버퍼 (Width 78 x Height 40)
pub struct ScreenBuffer {
    pub width: usize,
    pub height: usize,
    pub grid: Vec<Vec<Cell>>,
}

impl ScreenBuffer {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            width,
            height,
            grid: vec![vec![Cell::default(); width]; height],
        }
    }

    /// 화면 전체 공백 초기화
    pub fn clear(&mut self) {
        for y in 0..self.height {
            for x in 0..self.width {
                self.grid[y][x] = Cell::default();
            }
        }
    }

    /// 특정 (x, y) 좌표에 문자열 안전하게 쓰기 (테두리 침범 절대 불가)
    pub fn put_str(&mut self, start_x: usize, y: usize, s: &str, max_width: usize) {
        if y >= self.height || start_x >= self.width {
            return;
        }

        let mut cur_x = start_x;
        let limit_x = (start_x + max_width).min(self.width);

        for c in s.chars() {
            let cw = char_width(c);
            if cw == 0 {
                continue;
            }
            if cur_x + cw > limit_x {
                break;
            }

            if cw == 1 {
                self.grid[y][cur_x] = Cell {
                    ch: c,
                    is_continuation: false,
                    fg: None,
                    bg: None,
                };
                cur_x += 1;
            } else if cw == 2 {
                self.grid[y][cur_x] = Cell {
                    ch: c,
                    is_continuation: false,
                    fg: None,
                    bg: None,
                };
                if cur_x + 1 < limit_x {
                    self.grid[y][cur_x + 1] = Cell {
                        ch: ' ',
                        is_continuation: true,
                        fg: None,
                        bg: None,
                    };
                }
                cur_x += 2;
            }
        }
    }

    /// 특정 (x, y) 좌표에 컬러 도트 찍기 (하프블록 등)
    pub fn put_pixel(&mut self, x: usize, y: usize, ch: char, fg: Option<u8>, bg: Option<u8>) {
        if y < self.height && x < self.width {
            self.grid[y][x] = Cell {
                ch,
                is_continuation: false,
                fg,
                bg,
            };
        }
    }

    /// ANSI 컬러 시퀀스가 포함된 문자열을 파싱하여 버퍼에 안전하게 컬러로 쓰기
    pub fn put_ansi_str(&mut self, start_x: usize, y: usize, s: &str, max_width: usize) {
        if y >= self.height || start_x >= self.width {
            return;
        }

        let mut cur_x = start_x;
        let limit_x = (start_x + max_width).min(self.width);
        let mut cur_fg: Option<u8> = None;
        let mut cur_bg: Option<u8> = None;

        let bytes = s.as_bytes();
        let mut i = 0;

        while i < bytes.len() {
            // ANSI 이스케이프 파싱 (\x1b[...)
            if bytes[i] == 0x1b && i + 1 < bytes.len() && bytes[i + 1] == b'[' {
                let mut j = i + 2;
                while j < bytes.len() && bytes[j] != b'm' {
                    j += 1;
                }
                if j < bytes.len() && bytes[j] == b'm' {
                    let seq = std::str::from_utf8(&bytes[i + 2..j]).unwrap_or("");
                    // 파싱: 38;5;Nm (fg), 48;5;Nm (bg), 0 (reset), 39 (default fg), 49 (default bg)
                    let parts: Vec<&str> = seq.split(';').collect();
                    let mut p_idx = 0;
                    while p_idx < parts.len() {
                        match parts[p_idx] {
                            "0" => {
                                cur_fg = None;
                                cur_bg = None;
                                p_idx += 1;
                            }
                            "39" => {
                                cur_fg = None;
                                p_idx += 1;
                            }
                            "49" => {
                                cur_bg = None;
                                p_idx += 1;
                            }
                            "38" if p_idx + 2 < parts.len() && parts[p_idx + 1] == "5" => {
                                if let Ok(val) = parts[p_idx + 2].parse::<u8>() {
                                    cur_fg = Some(val);
                                }
                                p_idx += 3;
                            }
                            "48" if p_idx + 2 < parts.len() && parts[p_idx + 1] == "5" => {
                                if let Ok(val) = parts[p_idx + 2].parse::<u8>() {
                                    cur_bg = Some(val);
                                }
                                p_idx += 3;
                            }
                            _ => {
                                p_idx += 1;
                            }
                        }
                    }
                    i = j + 1;
                    continue;
                }
            }

            // UTF-8 일반 문자 디코딩
            let ch_str = match std::str::from_utf8(&bytes[i..]) {
                Ok(s) => s,
                Err(e) => {
                    let valid_up_to = e.valid_up_to();
                    if valid_up_to == 0 {
                        i += 1;
                        continue;
                    }
                    std::str::from_utf8(&bytes[i..i + valid_up_to]).unwrap_or("")
                }
            };

            if let Some(c) = ch_str.chars().next() {
                let cw = char_width(c);
                if cur_x + cw > limit_x {
                    break;
                }

                if cw == 1 {
                    self.grid[y][cur_x] = Cell {
                        ch: c,
                        is_continuation: false,
                        fg: cur_fg,
                        bg: cur_bg,
                    };
                    cur_x += 1;
                } else if cw == 2 {
                    self.grid[y][cur_x] = Cell {
                        ch: c,
                        is_continuation: false,
                        fg: cur_fg,
                        bg: cur_bg,
                    };
                    if cur_x + 1 < limit_x {
                        self.grid[y][cur_x + 1] = Cell {
                            ch: ' ',
                            is_continuation: true,
                            fg: cur_fg,
                            bg: cur_bg,
                        };
                    }
                    cur_x += 2;
                }
                i += c.len_utf8();
            } else {
                i += 1;
            }
        }
    }

    /// 특정 (x, y) 영역에 문자열 가운데 정렬하여 쓰기
    pub fn put_str_center(&mut self, start_x: usize, y: usize, s: &str, field_width: usize) {
        let sw = str_display_width(s);
        let pad = if field_width > sw {
            (field_width - sw) / 2
        } else {
            0
        };
        self.put_str(start_x + pad, y, s, field_width.saturating_sub(pad));
    }

    /// 수평 선 그리기
    pub fn draw_hline(&mut self, x1: usize, x2: usize, y: usize, ch: char) {
        if y >= self.height {
            return;
        }
        let end = x2.min(self.width - 1);
        for x in x1..=end {
            self.grid[y][x] = Cell {
                ch,
                is_continuation: false,
                fg: None,
                bg: None,
            };
        }
    }

    /// 수직 선 그리기
    pub fn draw_vline(&mut self, x: usize, y1: usize, y2: usize, ch: char) {
        if x >= self.width {
            return;
        }
        let end = y2.min(self.height - 1);
        for y in y1..=end {
            self.grid[y][x] = Cell {
                ch,
                is_continuation: false,
                fg: None,
                bg: None,
            };
        }
    }

    /// 5영역 고정 프레임 골격 구축 (40줄 시네마틱 레이아웃)
    pub fn build_card_skeleton(&mut self) {
        let w = self.width;
        let h = self.height;

        // 1. 외곽 사각 테두리
        // 상단 / 하단 가로선
        self.draw_hline(1, w - 2, 0, '═');
        self.draw_hline(1, w - 2, h - 1, '═');

        // 좌측 / 우측 세로선
        self.draw_vline(0, 1, h - 2, '║');
        self.draw_vline(w - 1, 1, h - 2, '║');

        // 모서리
        self.grid[0][0] = Cell { ch: '╔', is_continuation: false, fg: None, bg: None };
        self.grid[0][w - 1] = Cell { ch: '╗', is_continuation: false, fg: None, bg: None };
        self.grid[h - 1][0] = Cell { ch: '╚', is_continuation: false, fg: None, bg: None };
        self.grid[h - 1][w - 1] = Cell { ch: '╝', is_continuation: false, fg: None, bg: None };

        // 2. 헤더 구분선 (Row 2)
        self.draw_hline(1, w - 2, 2, '═');
        self.grid[2][0] = Cell { ch: '╠', is_continuation: false, fg: None, bg: None };
        self.grid[2][w - 1] = Cell { ch: '╣', is_continuation: false, fg: None, bg: None };

        // 3. 씬 아트 하단 구분선 (Row 26: Scene Art 23줄 Row 3..=25 끝)
        // 대화창(Col 1~41) + 상태창(Col 43~76) 분할선 (Col 42)
        self.draw_hline(1, w - 2, 26, '═');
        self.grid[26][0] = Cell { ch: '╠', is_continuation: false, fg: None, bg: None };
        self.grid[26][42] = Cell { ch: '╤', is_continuation: false, fg: None, bg: None };
        self.grid[26][w - 1] = Cell { ch: '╣', is_continuation: false, fg: None, bg: None };

        // 4. 대화창 & 상태창 중앙 세로 분할선 (Row 27~34, 8줄)
        self.draw_vline(42, 27, 34, '│');

        // 5. 선택지 상단 구분선 (Row 35)
        self.draw_hline(1, w - 2, 35, '═');
        self.grid[35][0] = Cell { ch: '╠', is_continuation: false, fg: None, bg: None };
        self.grid[35][42] = Cell { ch: '╧', is_continuation: false, fg: None, bg: None };
        self.grid[35][w - 1] = Cell { ch: '╣', is_continuation: false, fg: None, bg: None };
    }

    /// 화면 출력: ANSI 절대 커서 이동 (\x1b[H)으로 깜빡임 없이 컬러 고정 출력
    pub fn render_to_terminal(&self) {
        let mut out = io::stdout();
        let _ = write!(out, "\x1b[H");

        for y in 0..self.height {
            let mut line_str = String::with_capacity(self.width * 8);
            let mut cur_fg: Option<u8> = None;
            let mut cur_bg: Option<u8> = None;

            for x in 0..self.width {
                let cell = &self.grid[y][x];
                if !cell.is_continuation {
                    // 전경색 또는 배경색 변경 시 ANSI 코드 주입
                    if cell.fg != cur_fg || cell.bg != cur_bg {
                        cur_fg = cell.fg;
                        cur_bg = cell.bg;

                        match (cur_fg, cur_bg) {
                            (Some(f), Some(b)) => {
                                line_str.push_str(&format!("\x1b[38;5;{};48;5;{}m", f, b));
                            }
                            (Some(f), None) => {
                                line_str.push_str(&format!("\x1b[38;5;{}m\x1b[49m", f));
                            }
                            (None, Some(b)) => {
                                line_str.push_str(&format!("\x1b[39;48;5;{}m", b));
                            }
                            (None, None) => {
                                line_str.push_str("\x1b[0m");
                            }
                        }
                    }
                    line_str.push(cell.ch);
                }
            }
            if cur_fg.is_some() || cur_bg.is_some() {
                line_str.push_str("\x1b[0m");
            }
            let _ = writeln!(out, "{}", line_str);
        }
        let _ = out.flush();
    }
}

/// 화면 클리어 (ANSI 이스케이프 코드)
pub fn clear_screen() {
    print!("\x1b[2J\x1b[H");
    let _ = io::stdout().flush();
}

/// 템플릿 문자열 치환 ({var_name} -> 치환값)
pub fn substitute_template(
    line: &str,
    substitutions: &HashMap<String, String>,
    state: &GameState,
) -> String {
    let mut result = line.to_string();

    result = result.replace("{pack_title}", &state.pack.meta.title);
    result = result.replace("{pack_author}", &state.pack.meta.author);
    result = result.replace("{chapter_term}", &state.pack.meta.world.chapter_term);

    // 수치 바 치환 (10칸 게이지)
    let max_v = state.pack.meta.world.metric.max.max(1) as usize;
    let curr_v = state.metric_value.max(0) as usize;
    let bar_len = 10;
    let filled_len = (curr_v * bar_len / max_v).min(bar_len);
    let empty_len = bar_len - filled_len;

    let mut metric_bar = String::new();
    for _ in 0..filled_len {
        metric_bar.push('█');
    }
    for _ in 0..empty_len {
        metric_bar.push('░');
    }
    result = result.replace("{metric_bar}", &metric_bar);
    result = result.replace("{virtue_bar}", &metric_bar);
    result = result.replace("{light_bar}", &metric_bar);

    for (k, v) in substitutions {
        let pattern = format!("{{{}}}", k);
        result = result.replace(&pattern, v);
    }

    result
}

/// 78컬럼 40줄 5영역 전체 카드 프레임 렌더링 (2D 가상 화면 버퍼 방식)
pub fn render_card_frame(scene: &Scene, state: &GameState) {
    let mut buf = ScreenBuffer::new(CARD_WIDTH, CARD_HEIGHT);
    buf.clear();
    buf.build_card_skeleton();

    let tone_key = &state.current_tone;
    let prefixed_tone = if tone_key.starts_with("tone_") {
        tone_key.to_string()
    } else {
        format!("tone_{}", tone_key)
    };
    let raw_tone = tone_key.trim_start_matches("tone_");

    let substitutions = scene
        .substitutions
        .get(&prefixed_tone)
        .or_else(|| scene.substitutions.get(raw_tone))
        .or_else(|| scene.substitutions.get("tone_casual"))
        .or_else(|| scene.substitutions.get("casual"))
        .cloned()
        .unwrap_or_default();

    // ──────────────────────────────────────────────
    // 1. REGION 1: HEADER (Row 1)
    // ──────────────────────────────────────────────
    let left_header = format!("  {}", state.pack.meta.title);
    let right_header = format!(
        "{} · {}",
        if !scene.act_name.is_empty() {
            format!("제{}{}", scene.act, state.pack.meta.world.chapter_term)
        } else {
            "".to_string()
        },
        scene.act_name
    );

    buf.put_str(1, 1, &left_header, 35);
    let right_w = str_display_width(&right_header);
    let right_x = (CARD_WIDTH - 2).saturating_sub(right_w);
    buf.put_str(right_x, 1, &right_header, 35);

    // ──────────────────────────────────────────────
    // 3. REGION 3: DIALOGUE (Row 27..=34, Col 2..41, 8줄)
    // ──────────────────────────────────────────────
    let mut left_lines = Vec::new();
    let dlg_list_opt = scene
        .dialogue
        .get(&prefixed_tone)
        .or_else(|| scene.dialogue.get(raw_tone))
        .or_else(|| scene.dialogue.get("tone_casual"))
        .or_else(|| scene.dialogue.get("casual"));

    if let Some(dlg_list) = dlg_list_opt {
        for dlg in dlg_list {
            for raw_line in dlg.text.lines() {
                let wrapped = format_dialogue_speaker(&dlg.speaker, raw_line, 38);
                for w in wrapped {
                    left_lines.push(w);
                }
            }
        }
    } else {
        for (k, v) in &substitutions {
            if k.ends_with("_line") {
                let wrapped = format_dialogue_speaker("해설", v, 38);
                for w in wrapped {
                    left_lines.push(w);
                }
            }
        }
    }

    for (i, line) in left_lines.iter().take(8).enumerate() {
        buf.put_str(2, 27 + i, line, 39);
    }

    // ──────────────────────────────────────────────
    // 4. REGION 4: STATUS (Row 27..=34, Col 44..76, 8줄)
    // ──────────────────────────────────────────────
    let metric = &state.pack.meta.world.metric;
    let total_acts = state.pack.meta.structure.chapters.len();

    let tone_name = state
        .pack
        .meta
        .tones
        .get(raw_tone)
        .or_else(|| state.pack.meta.tones.get(&prefixed_tone))
        .map(|t| t.name.as_str())
        .unwrap_or(&state.current_tone);

    let right_lines = [
        format!("{} {}", metric.icon, metric.name),
        format!(
            "{}  {}/{}",
            substitute_template("{metric_bar}", &substitutions, state),
            state.metric_value,
            metric.max
        ),
        "".to_string(),
        format!(
            "◈ 제{}{}/전{}{}",
            scene.act, state.pack.meta.world.chapter_term, total_acts, state.pack.meta.world.chapter_term
        ),
        format!("◈ 문체: {}", tone_name),
        format!("◈ 모드: {}", state.current_mode),
        "".to_string(),
        "".to_string(),
    ];

    for (i, line) in right_lines.iter().enumerate() {
        if !line.is_empty() {
            buf.put_str(44, 27 + i, line, 32);
        }
    }

    // ──────────────────────────────────────────────
    // 5. REGION 5: CHOICE (Row 36..=38, Col 2..76, 3줄)
    // ──────────────────────────────────────────────
    if scene.is_transition {
        buf.put_str(2, 36, "▶ (아무 키나 눌러 계속 진행합니다)", 74);
        buf.put_str(2, 38, "입력 [Enter] ▶", 74);
    } else {
        for (idx, choice) in scene.choices.iter().take(2).enumerate() {
            let text = choice.text.get_for_tone(&state.current_tone);
            let choice_line = format!("{}. {}", idx + 1, text);
            buf.put_str(2, 36 + idx, &choice_line, 74);
        }
        buf.put_str(2, 38, "선택 번호 입력 ▶", 74);
    }

    // ──────────────────────────────────────────────
    // 2. REGION 2: SCENE ART / ANIMATION (Row 3..=25, 23줄 초대형 캔버스)
    // ──────────────────────────────────────────────
    // 애니메이션 컷씬(6프레임)이 정의되어 있으면 전체 프레임과 함께 순차적으로 부드럽게 재생
    if let Some(anim) = &scene.animation {
        if !anim.frames.is_empty() {
            for (f_idx, frame) in anim.frames.iter().enumerate() {
                // 이전 프레임 지우고 새 프레임 쓰기
                for y in 3..=25 {
                    for x in 2..76 {
                        buf.grid[y][x] = Cell::default();
                    }
                }
                for (i, line) in frame.iter().take(23).enumerate() {
                    let sub_line = substitute_template(line, &substitutions, state);
                    buf.put_ansi_str(2, 3 + i, &sub_line, 74);
                }
                buf.render_to_terminal();

                // 마지막 프레임이 아니면 딜레이 후 다음 컷 전환
                if f_idx + 1 < anim.frames.len() {
                    thread::sleep(Duration::from_millis(anim.frame_rate_ms));
                }
            }
        }
    } else {
        let art_lines: Vec<String> = if !scene.scene_art.is_empty() {
            scene
                .scene_art
                .iter()
                .map(|l| substitute_template(l, &substitutions, state))
                .collect()
        } else if !scene.card_template.is_empty() {
            scene
                .card_template
                .iter()
                .map(|l| substitute_template(l, &substitutions, state))
                .collect()
        } else {
            vec!["".to_string()]
        };

        // 23줄 캔버스에 컬러 렌더링
        for i in 0..23 {
            let y = 3 + i;
            if i < art_lines.len() {
                buf.put_ansi_str(2, y, &art_lines[i], 74);
            }
        }
        buf.render_to_terminal();
    }


}

/// 대사 포맷팅: 화자명과 첫 줄, 그리고 다음 줄 자동 들여쓰기 처리
fn format_dialogue_speaker(speaker: &str, text: &str, max_width: usize) -> Vec<String> {
    let mut lines = Vec::new();
    let prefix = format!("{}: ", speaker);
    let indent_spaces = " ".repeat(str_display_width(&prefix));

    let first_limit = max_width.saturating_sub(str_display_width(&prefix));
    let cont_limit = max_width.saturating_sub(indent_spaces.len());

    let mut words = text.split_whitespace().peekable();
    let mut cur_line = String::new();
    let mut cur_w = 0;
    let mut is_first_line = true;

    while let Some(word) = words.next() {
        let word_w = str_display_width(word);
        let space_w = if cur_line.is_empty() { 0 } else { 1 };
        let limit = if is_first_line { first_limit } else { cont_limit };

        if cur_w + space_w + word_w > limit {
            if !cur_line.is_empty() {
                if is_first_line {
                    lines.push(format!("{}{}", prefix, cur_line));
                    is_first_line = false;
                } else {
                    lines.push(format!("{}{}", indent_spaces, cur_line));
                }
                cur_line = word.to_string();
                cur_w = word_w;
            } else {
                // 단어 하나가 너무 길면 강제 분할
                if is_first_line {
                    lines.push(format!("{}{}", prefix, word));
                    is_first_line = false;
                } else {
                    lines.push(format!("{}{}", indent_spaces, word));
                }
                cur_line = String::new();
                cur_w = 0;
            }
        } else {
            if !cur_line.is_empty() {
                cur_line.push(' ');
                cur_w += 1;
            }
            cur_line.push_str(word);
            cur_w += word_w;
        }
    }

    if !cur_line.is_empty() {
        if is_first_line {
            lines.push(format!("{}{}", prefix, cur_line));
        } else {
            lines.push(format!("{}{}", indent_spaces, cur_line));
        }
    }

    lines
}
