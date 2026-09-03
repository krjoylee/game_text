// engine/src/ending.rs
// 엔딩 화면 렌더링 및 플레이어 성향 분석 (2D ScreenBuffer 기반 40줄 시네마틱 렌더링)

use crate::renderer::{ScreenBuffer, CARD_HEIGHT, CARD_WIDTH};
use crate::state::GameState;
use crate::width::str_display_width;

pub fn render_ending_screen(state: &GameState) {
    let mut buf = ScreenBuffer::new(CARD_WIDTH, CARD_HEIGHT);
    buf.clear();

    let w = CARD_WIDTH;
    let h = CARD_HEIGHT;

    // 외곽 테두리
    buf.draw_hline(1, w - 2, 0, '═');
    buf.draw_hline(1, w - 2, h - 1, '═');
    buf.draw_vline(0, 1, h - 2, '║');
    buf.draw_vline(w - 1, 1, h - 2, '║');
    buf.grid[0][0] = crate::renderer::Cell::new('╔');
    buf.grid[0][w - 1] = crate::renderer::Cell::new('╗');
    buf.grid[h - 1][0] = crate::renderer::Cell::new('╚');
    buf.grid[h - 1][w - 1] = crate::renderer::Cell::new('╝');

    // 제목
    buf.put_str_center(1, 2, "─── 여 정 의  끝 ───", w - 2);

    let metric = &state.pack.meta.world.metric;
    let score_line = format!(
        "당신의 {}: {}/{} ({})",
        metric.name,
        state.metric_value,
        metric.max,
        metric.icon.repeat((state.metric_value.max(0) as usize).min(10))
    );
    buf.put_str_center(1, 4, &score_line, w - 2);

    // 구분선 1
    buf.draw_hline(1, w - 2, 6, '─');
    buf.grid[6][0] = crate::renderer::Cell::new('╠');
    buf.grid[6][w - 1] = crate::renderer::Cell::new('╣');

    // 여정 궤적 요약 (최대 8개 기록 표시)
    buf.put_str(3, 8, "[ 선택의 궤적 ]", w - 6);
    for (i, record) in state.history.iter().take(8).enumerate() {
        let delta_str = if record.delta > 0 {
            format!("+{}", record.delta)
        } else if record.delta < 0 {
            format!("{}", record.delta)
        } else {
            " 0".to_string()
        };

        let row = 10 + i * 2;
        let act_str = format!("제{}막 {}", record.act, record.act_name);
        buf.put_str(4, row, &act_str, 16);
        buf.put_str(22, row, "──", 4);
        buf.put_str(26, row, &record.choice_text, 40);
        let delta_display = format!("[{}]", delta_str);
        buf.put_str(w - 10, row, &delta_display, 8);
    }

    // 구분선 2
    let sep2_row = 28;
    buf.draw_hline(1, w - 2, sep2_row, '─');
    buf.grid[sep2_row][0] = crate::renderer::Cell::new('╠');
    buf.grid[sep2_row][w - 1] = crate::renderer::Cell::new('╣');

    // 엔딩 성향 분석 매칭
    let mut sorted_endings = state.pack.meta.endings.clone();
    sorted_endings.sort_by(|a, b| b.min_virtue.cmp(&a.min_virtue));

    let mut matched_ending = None;
    for ending in &sorted_endings {
        if state.metric_value >= ending.min_virtue {
            matched_ending = Some(ending);
            break;
        }
    }

    let default_desc = "모든 여정을 마치고 깨달음을 얻은 순례자".to_string();
    let (ending_name, ending_desc) = if let Some(end) = matched_ending {
        (end.name.clone(), end.description.clone())
    } else {
        ("순례의 완성".to_string(), default_desc)
    };

    buf.put_str_center(1, sep2_row + 2, &format!("★ 칭호: [{}] ★", ending_name), w - 2);

    let desc_lines = wrap_text_display_width(&ending_desc, 64);
    for (i, line) in desc_lines.iter().take(6).enumerate() {
        buf.put_str_center(1, sep2_row + 4 + i, line, w - 2);
    }

    buf.render_to_terminal();
    println!("\n  게임을 플레이해주셔서 감사합니다. [Enter]를 누르면 종료합니다.");
}

pub fn render_game_over_screen(state: &GameState) {
    let mut buf = ScreenBuffer::new(CARD_WIDTH, CARD_HEIGHT);
    buf.clear();

    let w = CARD_WIDTH;
    let h = CARD_HEIGHT;

    buf.draw_hline(1, w - 2, 0, '═');
    buf.draw_hline(1, w - 2, h - 1, '═');
    buf.draw_vline(0, 1, h - 2, '║');
    buf.draw_vline(w - 1, 1, h - 2, '║');
    buf.grid[0][0] = crate::renderer::Cell::new('╔');
    buf.grid[0][w - 1] = crate::renderer::Cell::new('╗');
    buf.grid[h - 1][0] = crate::renderer::Cell::new('╚');
    buf.grid[h - 1][w - 1] = crate::renderer::Cell::new('╝');

    buf.put_str_center(1, 8, "☠  여 정 의  중 단  ☠", w - 2);

    buf.draw_hline(1, w - 2, 14, '─');
    buf.grid[14][0] = crate::renderer::Cell::new('╠');
    buf.grid[14][w - 1] = crate::renderer::Cell::new('╣');

    buf.put_str_center(1, 18, "수치가 바닥나 더 이상 나아갈 수 없습니다.", w - 2);
    buf.put_str_center(
        1,
        22,
        &format!("최종 {}: 0/{}", state.pack.meta.world.metric.name, state.pack.meta.world.metric.max),
        w - 2,
    );

    buf.render_to_terminal();
    println!("\n  [Enter]를 누르면 종료합니다.");
}

fn wrap_text_display_width(s: &str, max_width: usize) -> Vec<String> {
    let mut lines = Vec::new();
    let mut current = String::new();

    for word in s.split_whitespace() {
        let space_w = if current.is_empty() { 0 } else { 1 };
        let word_w = str_display_width(word);

        if str_display_width(&current) + space_w + word_w > max_width {
            if !current.is_empty() {
                lines.push(current);
            }
            current = word.to_string();
        } else {
            if !current.is_empty() {
                current.push(' ');
            }
            current.push_str(word);
        }
    }

    if !current.is_empty() {
        lines.push(current);
    }

    lines
}
