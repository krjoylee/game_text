// engine/src/main.rs
// Divina Ludus — 고전문학 텍스트 게임 메이커 엔진 (Zero Dependency Core)
// 2D ScreenBuffer 프레임 고정 기반 렌더링

mod ending;
mod input;
mod loader;
mod model;
mod renderer;
mod state;
mod width;
mod yaml_parser;

use ending::{render_ending_screen, render_game_over_screen};
use input::{get_user_choice, wait_for_enter, UserAction};
use loader::load_pack_from_path;
use renderer::{clear_screen, render_card_frame, ScreenBuffer, CARD_HEIGHT, CARD_WIDTH};
use state::GameState;
use std::env;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

fn main() {
    let args: Vec<String> = env::args().collect();

    // 팩 경로 결정 (--pack 옵션 또는 기본 샘플)
    let pack_path = if args.len() >= 3 && args[1] == "--pack" {
        PathBuf::from(&args[2])
    } else if args.len() >= 2 && !args[1].starts_with('-') {
        PathBuf::from(&args[1])
    } else {
        let candidates = [
            "packs/heungbu_nolbu/4_game_scene.yaml",
            "packs/heungbu_nolbu/3_scene.yaml",
            "../packs/heungbu_nolbu/4_game_scene.yaml",
            "../packs/heungbu_nolbu/3_scene.yaml",
        ];

        let mut found = PathBuf::from("packs/heungbu_nolbu/4_game_scene.yaml");
        for c in &candidates {
            if Path::new(c).exists() {
                found = PathBuf::from(c);
                break;
            }
        }
        found
    };

    let pack = match load_pack_from_path(&pack_path) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("\n❌ 팩 로딩 오류: {}\n", e);
            eprintln!("사용법: divina-ludus [--pack <팩_경로>]");
            return;
        }
    };

    let mut state = GameState::new(pack);

    // 1. 타이틀 화면 (ScreenBuffer 기반)
    show_title_screen(&mut state);

    // 2. 메인 게임 루프
    while !state.is_finished {
        let current_scene = match state.current_scene() {
            Some(s) => s.clone(),
            None => {
                break;
            }
        };

        // 2D ScreenBuffer 카드 프레임 렌더링 (절대좌표 덮어쓰기)
        render_card_frame(&current_scene, &state);

        // 입력 처리
        if current_scene.is_transition {
            let action = get_user_choice(0, true);
            match action {
                UserAction::Quit => {
                    println!("\n  게임을 종료합니다. 안녕히 가세요!");
                    return;
                }
                _ => {
                    let next = current_scene.next_scene.as_deref().unwrap_or("ending");
                    state.advance_to(next);
                }
            }
        } else {
            let action = get_user_choice(current_scene.choices.len(), false);
            match action {
                UserAction::Select(idx) => {
                    if let Some(choice) = current_scene.choices.get(idx) {
                        let delta = choice.get_metric_delta();
                        state.metric_value += delta;
                        state.metric_value = state.metric_value.min(state.pack.meta.world.metric.max);

                        if state.check_failure() {
                            clear_screen();
                            show_fail_screen(&current_scene, &state);
                            state.handle_failure_return();
                        } else {
                            state.apply_choice(choice);
                        }
                    }
                }
                UserAction::Help => {
                    println!("\n  📖 도움말:");
                    println!("    • 숫자 (1~{}): 선택지를 고릅니다.", current_scene.choices.len());
                    println!("    • 'h' / 'help': 본 도움말을 표시합니다.");
                    println!("    • 'q' / 'quit': 게임을 종료합니다.");
                    print!("\n  계속하려면 [Enter]를 누르세요...");
                    let _ = io::stdout().flush();
                    wait_for_enter();
                }
                UserAction::Quit => {
                    println!("\n  게임을 종료합니다. 안녕히 가세요!");
                    return;
                }
                _ => {}
            }
        }
    }

    // 3. 엔딩 및 게임오버 화면 출력 (ScreenBuffer 기반)
    clear_screen();
    if state.game_over {
        render_game_over_screen(&state);
    } else {
        render_ending_screen(&state);
    }
    wait_for_enter();
}

fn show_title_screen(state: &mut GameState) {
    loop {
        clear_screen();
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

        let cur_tone_name = state
            .pack
            .meta
            .tones
            .get(&state.current_tone)
            .map(|t| t.name.as_str())
            .unwrap_or(&state.current_tone);

        buf.put_str_center(1, 4, &format!("◆ {} ◆", state.pack.meta.title), w - 2);
        buf.put_str_center(1, 6, &format!("원작: {}", state.pack.meta.author), w - 2);

        buf.draw_hline(1, w - 2, 9, '─');
        buf.grid[9][0] = crate::renderer::Cell::new('╠');
        buf.grid[9][w - 1] = crate::renderer::Cell::new('╣');

        buf.put_str_center(1, 13, &state.pack.meta.description, w - 2);

        buf.put_str(8, 20, "  [1] 새로운 여정 시작하기", w - 16);
        buf.put_str(8, 23, "  [2] 암호(Password) 입력하고 이어하기", w - 16);
        buf.put_str(8, 26, &format!("  [3] 문체 변경 (현재: {})", cur_tone_name), w - 16);
        buf.put_str(8, 29, "  [Q] 게임 종료", w - 16);

        buf.render_to_terminal();

        print!("\n  메뉴를 선택하세요 (1~3 / 'Q' 종료) ▶ ");
        let _ = io::stdout().flush();

        let mut line = String::new();
        if io::stdin().read_line(&mut line).is_err() {
            return;
        }

        let trimmed = line.trim();
        match trimmed {
            "1" => break,
            "2" => {
                print!("  암호(Password)를 입력하세요 ▶ ");
                let _ = io::stdout().flush();
                let mut pw = String::new();
                let _ = io::stdin().read_line(&mut pw);
                if state.jump_by_password(&pw) {
                    println!("\n  ✨ 암호가 확인되었습니다. 해당 막으로 이동합니다!");
                    print!("  [Enter]를 누르면 시작합니다...");
                    let _ = io::stdout().flush();
                    wait_for_enter();
                    break;
                } else {
                    println!("\n  ⚠️ 유효하지 않은 암호입니다. (예: 제비, 박씨, 금은보화)");
                    print!("  [Enter]를 누르면 메뉴로 돌아갑니다...");
                    let _ = io::stdout().flush();
                    wait_for_enter();
                    continue;
                }
            }
            "3" => {
                let tone_keys: Vec<String> = state.pack.meta.tones.keys().cloned().collect();
                if !tone_keys.is_empty() {
                    let cur_idx = tone_keys.iter().position(|k| k == &state.current_tone).unwrap_or(0);
                    let next_idx = (cur_idx + 1) % tone_keys.len();
                    let next_tone = tone_keys[next_idx].clone();
                    state.set_tone(next_tone.clone());

                    let new_name = state.pack.meta.tones.get(&next_tone).map(|t| t.name.as_str()).unwrap_or(&next_tone);
                    println!("\n  ✨ 문체가 변경되었습니다: [{}]", new_name);
                    print!("  [Enter]를 누르면 계속합니다...");
                    let _ = io::stdout().flush();
                    wait_for_enter();
                }
                continue;
            }
            "q" | "Q" => {
                std::process::exit(0);
            }
            _ => {
                println!("\n  ⚠️ 1, 2, 3, Q 중에서 올바른 메뉴를 선택해주세요.");
                print!("  [Enter]를 누르면 계속합니다...");
                let _ = io::stdout().flush();
                wait_for_enter();
                continue;
            }
        }
    }
}

fn show_fail_screen(scene: &crate::model::Scene, state: &GameState) {
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

    buf.put_str_center(1, 6, "⚠️  수치가 소진되었습니다  ⚠️", w - 2);

    buf.draw_hline(1, w - 2, 11, '─');
    buf.grid[11][0] = crate::renderer::Cell::new('╠');
    buf.grid[11][w - 1] = crate::renderer::Cell::new('╣');

    let fail_text = if let Some(on_fail) = &scene.on_fail {
        match &on_fail.text {
            Some(crate::model::FailText::Simple(s)) => s.clone(),
            Some(crate::model::FailText::MultiTone(map)) => {
                map.get(&state.current_tone)
                    .or_else(|| map.get("tone_casual"))
                    .or_else(|| map.get("casual"))
                    .cloned()
                    .unwrap_or_else(|| "선택의 결과로 더 이상 나아갈 수 없습니다.".to_string())
            }
            None => "선택의 결과로 더 이상 나아갈 수 없습니다.".to_string(),
        }
    } else {
        "선택의 결과로 더 이상 나아갈 수 없습니다.".to_string()
    };

    buf.put_str_center(1, 16, &fail_text, w - 2);
    buf.put_str_center(1, 22, "▶ 현재 막의 처음으로 돌아가 다시 도전합니다.", w - 2);

    buf.render_to_terminal();
    print!("\n  [Enter]를 누르면 계속합니다...");
    let _ = io::stdout().flush();
    wait_for_enter();
}
