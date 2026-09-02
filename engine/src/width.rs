// engine/src/width.rs
// 한글 및 유니코드 자폭(Display Width) 계산기 (Zero Dependency)

pub fn char_width(c: char) -> usize {
    let u = c as u32;

    // 제어 문자
    if u < 32 || (u >= 0x7F && u < 0xA0) {
        return 0;
    }

    // 기본 ASCII (1칸)
    if u < 0x7F {
        return 1;
    }

    // 유니코드 점자 패턴 (Braille Patterns: 0x2800..=0x28FF) ➔ 1칸 고정
    if (0x2800..=0x28FF).contains(&u) {
        return 1;
    }

    // 한글 음절 (가-힣)
    if (0xAC00..=0xD7A3).contains(&u) {
        return 2;
    }

    // 한글 자모 및 한글 호환 자모
    if (0x1100..=0x11FF).contains(&u) || (0x3130..=0x318F).contains(&u) {
        return 2;
    }

    // CJK 통합 한자 및 기호
    if (0x2E80..=0x9FFF).contains(&u) {
        return 2;
    }

    // 전각 문자 (Fullwidth)
    if (0xFF01..=0xFF60).contains(&u) || (0xFFE0..=0xFFE6).contains(&u) {
        return 2;
    }

    // 박스 그리기 선(0x2500..=0x257F) 및 블록 요소(0x2580..=0x259F, █, ░, ▒, ▓ 등)는 1칸
    if (0x2500..=0x259F).contains(&u) {
        return 1;
    }

    // 기타 특수 심볼 및 이모지 (◆, ◇, ◈, ♧, ★, ☆, 凸, 凹, 鬼, ☀, ☽, ☠ 등)
    if (0x25A0..=0x27BF).contains(&u) || (0x1F300..=0x1FAFF).contains(&u) {
        return 2;
    }

    // 기본 1칸
    1
}

pub fn str_display_width(s: &str) -> usize {
    s.chars().map(char_width).sum()
}
