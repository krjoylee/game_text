// engine/src/input.rs
// 사용자 입력 처리 모듈 (데드락 방지 및 종료 우선 처리)

use std::io::{self, Write};

pub enum UserAction {
    Select(usize),
    AnyKey,
    Quit,
    Help,
}

pub fn get_user_choice(max_choices: usize, is_transition: bool) -> UserAction {
    loop {
        if is_transition {
            print!("  [Enter] 키를 누르면 다음으로 이동합니다... ('q' 종료) ");
        } else {
            print!("  선택할 번호를 입력하세요 (1~{} / 'h' 도움말 / 'q' 종료) ▶ ", max_choices);
        }
        let _ = io::stdout().flush();

        let mut line = String::new();
        match io::stdin().read_line(&mut line) {
            Ok(0) => {
                // EOF 도달
                return UserAction::Quit;
            }
            Err(_) => {
                return UserAction::Quit;
            }
            Ok(_) => {}
        }

        let trimmed = line.trim();

        // 1. 종료 명령어 최우선 처리 (BUG-004 해결)
        if trimmed.eq_ignore_ascii_case("q") || trimmed.eq_ignore_ascii_case("quit") {
            return UserAction::Quit;
        }

        // 2. 도움말 명령어
        if trimmed.eq_ignore_ascii_case("h") || trimmed.eq_ignore_ascii_case("help") {
            return UserAction::Help;
        }

        // 3. 전환 씬인 경우 아무 키나 Enter 입력 시 진행
        if is_transition {
            return UserAction::AnyKey;
        }

        if max_choices == 0 {
            return UserAction::AnyKey;
        }

        if let Ok(num) = trimmed.parse::<usize>() {
            if num >= 1 && num <= max_choices {
                return UserAction::Select(num - 1);
            }
        }

        println!("  ⚠️ 올바른 번호(1~{})를 입력해주세요.\n", max_choices);
    }
}

pub fn wait_for_enter() {
    let mut line = String::new();
    let _ = io::stdin().read_line(&mut line);
}
