# Divina Ludus — 버그 리스트 및 수정 계획서

> **작성일시**: 2026-09-02 13:48  
> **검증 방법**: 자동화 플레이스루 테스트 + 소스 코드 전수 감사 + YAML 데이터 검증 + 입력 스트림 데드락 분석  
> **관련 파일**: [main.rs](file:///home/krjoylee/code/game/engine/src/main.rs) · [renderer.rs](file:///home/krjoylee/code/game/engine/src/renderer.rs) · [state.rs](file:///home/krjoylee/code/game/engine/src/state.rs) · [loader.rs](file:///home/krjoylee/code/game/engine/src/loader.rs) · [ending.rs](file:///home/krjoylee/code/game/engine/src/ending.rs) · [input.rs](file:///home/krjoylee/code/game/engine/src/input.rs) · [width.rs](file:///home/krjoylee/code/game/engine/src/width.rs) · [4_game_scene.yaml](file:///home/krjoylee/code/game/packs/heungbu_nolbu/4_game_scene.yaml)

---

## 🏛️ 수정 원칙 (Operating Hierarchy 적용)

```
Philosophy > Spec > Tech Concepts > 이 문서
```
- **엔진 코드 수정**: `engine/src/` 내 `.rs` 파일 변경
- **팩 데이터 수정**: `packs/heungbu_nolbu/4_game_scene.yaml` 변경
- **반드시 구분**: 엔진 코드 문제인지 vs 팩 데이터(양식) 문제인지 각 티켓에 명시

---

## 📋 버그 티켓 목록

### 심각도 범례

| 등급 | 의미 |
|------|------|
| 🔴 **CRITICAL** | 프로그램 멈춤(데드락), 게임 진행 불가 또는 핵심 기능 완전 고장 |
| 🟠 **HIGH** | 주요 기능 비작동 또는 화면 심각 깨짐 |
| 🟡 **MEDIUM** | 부분 기능 미작동 또는 시각적 불일치 |
| 🟢 **LOW** | 사용성/코드 품질 개선 |

---

### 🔴 BUG-000: 타이틀 메뉴에서 `stdin.lock()` 중복 획득으로 인한 데드락 (Hang/Freeze)

| 항목 | 내용 |
|------|------|
| **심각도** | 🔴 CRITICAL (치명적) |
| **분류** | 엔진 코드 (`main.rs`, `input.rs`) |
| **현상** | **타이틀 화면에서 메뉴 [2] 암호 입력 또는 메뉴 [3] 문체 변경을 선택하면 프로그램이 즉시 멈추고(무한 대기/데드락) 아무런 반응을 하지 않는다.** (Test 2, Test 3 백그라운드 태스크가 멈춰있던 근본 원인) |
| **근거** | 1. `main.rs:138-139`: `show_title_screen()` 함수 내부에서 `let stdin = io::stdin(); let mut handle = stdin.lock();` 로 표준 입력 락을 획득함.<br>2. `main.rs:160, 164, 173`: 메뉴 2와 3 처리 내부에서 `wait_for_enter()`를 호출함.<br>3. `input.rs:66-67`: `wait_for_enter()` 내부에서 `let stdin = io::stdin(); let mut handle = stdin.lock();` 로 **동일 스레드에서 stdin 락을 다시 획득하려고 시도함**.<br>4. Rust의 표준 라이브러리 `Stdin::lock()`은 재진입 불가(Non-reentrant) 뮤텍스이므로 **즉시 자기 자신과의 교착상태(Self-Deadlock)에 빠져 영구 정지**함.<br>5. 메뉴 3(문체 변경)에서 `show_title_screen(state)`를 재귀 호출할 때도 이전 락이 해제되지 않아 동일한 데드락 발생. |

**수정 계획:**

1. **[엔진] `input.rs` — `wait_for_enter()` 및 입력 함수 리팩터링**
   - `Stdin::lock()`을 중복으로 걸지 않고, 단순 버퍼 읽기 함수는 `io::stdin().read_line(&mut String)`을 직접 사용하도록 수정하거나 핸들을 분리.
   ```rust
   // input.rs
   pub fn wait_for_enter() {
       let mut line = String::new();
       let _ = io::stdin().read_line(&mut line);
   }
   ```

2. **[엔진] `main.rs` — `show_title_screen` 루프 구조 개선**
   - 함수 내부에서 영구 `handle` 락을 쥐고 있지 말고, 각 입력 시점마다 `io::stdin().read_line(&mut line)`을 사용.
   - 메뉴 3(문체 변경) 시 재귀 호출(`show_title_screen(state)`)을 완전히 제거하고, 상위 `loop`의 `continue`를 통해 화면을 다시 그리고 입력을 받도록 수정.

---

### 🔴 BUG-001: 문체(tone) 키 불일치 — 대화/선택지가 문체 전환에 반응하지 않음

| 항목 | 내용 |
|------|------|
| **심각도** | 🔴 CRITICAL |
| **분류** | 엔진 코드 + 팩 데이터 양쪽 |
| **현상** | 문체를 변경해도 대화(dialogue)와 선택지(choices)에 반영되지 않는 경우가 있다. 실행할 때마다 초기 문체가 무작위로 `casual` 또는 `classic`으로 설정된다 (5회 반복 테스트 결과 확인). |
| **근거** | 1. `pack.tones`의 키는 `casual`/`classic`이지만, `dialogue` 및 `substitutions` 데이터의 키는 `tone_casual`/`tone_classic`이다 (접두사 `tone_` 불일치).<br>2. `state.rs:36-42`: `pack.meta.tones.keys().next()` — HashMap은 순서가 없어 실행마다 초기 톤이 달라진다.<br>3. `main.rs:170`: 토글이 `"casual"` ↔ `"classic"` 하드코딩으로만 전환되어 다른 키 이름으로는 동작 안 함.<br>4. `renderer.rs:121`: 대화 폴백 키가 `"tone_casual"`이지만 상태 키는 `"casual"` — 항상 폴백에만 걸린다.<br>5. `model.rs:189`: 선택지 폴백도 `"casual"`인데 실제 맵 키는 `"tone_casual"`. |

**수정 계획:**

1. **[엔진] `state.rs` — 초기 톤 결정 로직 수정** (파일: `state.rs:36-42`)
   - `HashMap.keys().next()` 대신, YAML의 `tones.default` 값을 파싱하여 사용한다.
   - `loader.rs`에서 `tones.default` 키를 읽어 `PackMeta`에 `default_tone: String` 필드 추가.
   - `state.rs:36`에서 `pack.meta.default_tone.clone()` 사용.

2. **[엔진] `main.rs` — 톤 토글 일반화** (파일: `main.rs:168-176`)
   - `"casual"` / `"classic"` 하드코딩 제거.
   - `pack.meta.tones.keys()`를 순회하며 현재 톤 다음 키로 순환 토글.

3. **[엔진 또는 팩 데이터] 키 이름 통일** — 둘 중 하나 선택:
   - **방법 A (권장 — 엔진 수정)**: `renderer.rs:121,193` 및 `model.rs:189`의 폴백 키를 `"tone_casual"` → `"casual"`로 통일하지 말고, **런타임에 `"tone_" + state.current_tone` 형태로 합성**하여 대화/치환 맵 조회.
   - **방법 B (팩 데이터 수정)**: `4_game_scene.yaml` 전체에서 `tone_casual` → `casual`, `tone_classic` → `classic`으로 교체 (약 80군데).

> [!IMPORTANT]
> 방법 A를 권장한다. 팩 데이터의 `tone_casual`/`tone_classic` 형식이 더 가독성이 좋고 명시적이므로, **엔진이 조회 시 접두사를 붙이는 것이 맞다**.

---

### 🔴 BUG-002: `on_fail` 및 `world.failure` 설정 미파싱 — 실패 시스템 완전 무시

| 항목 | 내용 |
|------|------|
| **심각도** | 🔴 CRITICAL |
| **분류** | 엔진 코드 |
| **현상** | `loader.rs`에서 `world.failure`와 각 씬의 `on_fail` 블록을 전혀 파싱하지 않는다. 수치가 0 이하로 떨어져도 실패 화면이 뜨긴 하지만, YAML에 정의된 커스텀 메시지와 복구 전략이 적용되지 않는다. |
| **근거** | `loader.rs:139` → `failure: None` 하드코딩.<br>`loader.rs:336` → `on_fail: None` 하드코딩. |

**수정 계획:**

1. **[엔진] `loader.rs:135-144` — `world.failure` 파싱 추가**
   ```rust
   // world 맵에서 failure 블록 파싱
   let failure = w.get("failure").map(|f| FailureConfig {
       return_strategy: f.get_str("return_strategy").unwrap_or("scene_retry").to_string(),
       speaker: f.get_str("speaker").unwrap_or("").to_string(),
       message_key: f.get_str("message_key").unwrap_or("").to_string(),
   });
   ```

2. **[엔진] `loader.rs:320-337` — 각 씬의 `on_fail` 파싱 추가**
   ```rust
   let on_fail = s_item.get("on_fail").map(|of| OnFailConfig {
       speaker: of.get_str("speaker").unwrap_or("").to_string(),
       text: of.get_str("text").map(|t| FailText::Simple(t.to_string())),
       return_to: of.get_str("return_to").map(|s| s.to_string()),
   });
   ```

---

### 🟠 BUG-003: 전환 씬에서 `q` 입력 시 종료 대신 엔딩 화면 출력

| 항목 | 내용 |
|------|------|
| **심각도** | 🟠 HIGH |
| **분류** | 엔진 코드 |
| **현상** | 전환 씬(transition scene)에서 유저가 `q`를 입력하면 즉시 종료되지 않고 엔딩 화면이 출력된다. 선택지 씬에서는 `return`으로 즉시 종료되지만, 전환 씬에서는 `break`로 루프를 빠져나가 엔딩 화면으로 흘러간다. |
| **근거** | `main.rs:80` → `UserAction::Quit => break` (엔딩 화면으로 감).<br>`main.rs:102` → `UserAction::Quit => { println!(...); return; }` (즉시 종료). |

**수정 계획:**

1. **[엔진] `main.rs:80` 수정**
   ```rust
   UserAction::Quit => {
       println!("\n게임을 종료합니다. 안녕히 가세요!");
       return;
   },
   ```

---

### 🟠 BUG-004: 전환 씬에서 `q` 입력이 먹히지 않음

| 항목 | 내용 |
|------|------|
| **심각도** | 🟠 HIGH |
| **분류** | 엔진 코드 |
| **현상** | 전환 씬(transition scene)에서 `q`를 입력하면 종료 대신 다음 씬으로 그냥 넘어간다. |
| **근거** | `input.rs:39-41` → `is_transition`이 true이면 입력 내용과 관계없이 무조건 `UserAction::AnyKey`를 반환한다. `q`/`quit` 체크(line 43)가 실행되지 않는다. |

**수정 계획:**

1. **[엔진] `input.rs:37-41` 수정 — `q` 체크를 transition 체크보다 먼저 배치**
   ```rust
   let trimmed = line.trim();
   
   // 종료 체크를 항상 먼저
   if trimmed.eq_ignore_ascii_case("q") || trimmed.eq_ignore_ascii_case("quit") {
       return UserAction::Quit;
   }
   
   if is_transition {
       return UserAction::AnyKey;
   }
   ```

---

### 🟠 BUG-005: 엔딩 선택 궤적(여정 히스토리) 테이블 한글 정렬 깨짐

| 항목 | 내용 |
|------|------|
| **심각도** | 🟠 HIGH |
| **분류** | 엔진 코드 |
| **현상** | 엔딩 화면의 `[ 선택의 궤적 ]` 테이블에서 한글 막이름/선택지 텍스트의 정렬이 뒤틀린다. `[+1]`, `[+2]` 점수 표기가 줄마다 뒤죽박죽으로 밀려 테두리를 넘어간다. |
| **근거** | `ending.rs:39` → `{:<10}`, `{:<24}` Rust format 매크로가 바이트/chars 기준으로 정렬하며, **한글 표시 자폭(display width)을 고려하지 않는다.** 한글 1문자 = 2칸인데 1칸으로 계산하여 공백이 부족해진다. |

**수정 계획:**

1. **[엔진] `ending.rs:38-44` — `width.rs`의 `pad_right` 함수를 사용하여 정렬**
   ```rust
   let act_name_padded = pad_right(&record.act_name, 12);  // 12 display-width
   let choice_padded = pad_right(&truncate_to_width(&record.choice_text, 28), 28);
   let summary = format!(
       "  제{}막 {} ── {} [{}]",
       record.act, act_name_padded, choice_padded, delta_str
   );
   ```

2. **[엔진] `ending.rs:78-86` — `truncate_str` 함수를 `truncate_to_width` 기반으로 교체**
   - 현재 char 수 기반 → display width 기반으로 변경.

3. **[엔진] `ending.rs:88-108` — `wrap_text` 함수의 `.len()` → `str_display_width()` 교체**
   - `current.len()` → `str_display_width(&current)` (UTF-8 바이트가 아닌 표시 폭 기준).

---

### 🟠 BUG-006: 메트릭 바(█░) 자폭 계산 오류 — 상태창 정렬 깨짐

| 항목 | 내용 |
|------|------|
| **심각도** | 🟠 HIGH |
| **분류** | 엔진 코드 |
| **현상** | 상태창(우측 45%)에서 메트릭 바 `███░░░░░░░` 뒤의 숫자/텍스트 정렬이 일관되지 않다. 바 길이가 바뀔 때마다 `3/10` 등의 숫자가 밀린다. |
| **근거** | `width.rs:39-44` → `█`(U+2588), `░`(U+2591)의 char_width가 **2**로 반환된다. 10개의 bar 문자 → 표시 폭 20칸. 그런데 `renderer.rs:94`에서 `bar_len = 10`으로 10문자를 생성하므로 **실제 20칸을 차지하게 되어** 우측 35칸 영역을 침범한다. |

**수정 계획:**

1. **[엔진] `width.rs` — `█`(U+2588), `░`(U+2591) 등 Block Elements의 자폭을 1로 처리**
   - Block Elements 범위 `0x2580..=0x259F`를 Box Drawing Lines(`0x2500..=0x257F`)와 동일하게 1칸 처리.
   ```rust
   // 박스 그리기 선 및 블록 요소는 1칸
   if (0x2500..=0x259F).contains(&u) {
       return 1;
   }
   ```

---

### 🟡 BUG-007: 대화 텍스트 줄 잘림 — 긴 대사가 중간에 끊김

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 + 팩 데이터 |
| **현상** | 좌측 대화 영역이 40칸으로 고정되어 있어, 긴 대사가 `"흥부: "어? 저게 작년에 다리 고쳐준 그 제│"` 식으로 중간에 잘린다. 뒷부분이 아예 표시되지 않는다. |
| **근거** | `renderer.rs:180` → `left_w = 40` 하드코딩.<br>`renderer.rs:251` → `pad_right(left_c, left_w)` → 40칸 초과 시 `truncate_to_width`로 절삭.<br>대사 줄바꿈(word wrap) 로직 없음. 7줄 이상은 드롭. |

**수정 계획:**

1. **[엔진] `renderer.rs:184-205` — 대사 자동 줄바꿈(word-wrap) 로직 추가**
   - `speaker: "text"` 형식으로 결합한 뒤, `left_w` 초과 시 다음 줄에 이어서 출력.
   - 7줄 넘김을 완전히 막을 수는 없지만, 가능한 한 줄바꿈하여 최대한 표시.

2. **[팩 데이터] 대사 길이 점검** — `4_game_scene.yaml`의 모든 `text` 필드를 검토하여:
   - `speaker + ": \"" + text + "\""` 결합 시 표시 폭이 38칸(40 - 테두리 2칸) 이내인지 확인.
   - 초과하는 대사는 2줄로 분할.

---

### 🟡 BUG-008: 타이틀 메뉴에서 잘못된 입력 시 게임 시작됨

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 |
| **현상** | 타이틀 화면에서 `1`, `2`, `3`, `q` 이외의 키(예: `5`, `a`, 빈 Enter)를 누르면 에러 메시지 없이 바로 게임이 시작된다. |
| **근거** | `main.rs:180-182` → `_ => { break; }` — 미식별 입력 시 루프를 빠져나가 게임이 시작됨. |

**수정 계획:**

1. **[엔진] `main.rs:180-182` 수정**
   ```rust
   _ => {
       println!("  ⚠️ 1, 2, 3, Q 중에서 선택해주세요.");
       continue;
   }
   ```

---

### 🟡 BUG-009: `UserAction::Help` 입력 시 아무 반응 없음

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 |
| **현상** | 선택지 씬에서 `h` 또는 `help`를 입력하면 아무 일도 일어나지 않는다. 도움말 기능이 선언되어 있으나 구현되어 있지 않다. |
| **근거** | `input.rs:47-49` → `UserAction::Help` 반환.<br>`main.rs:105` → `_ => {}` — 아무 처리 없이 무시. |

**수정 계획:**

1. **[엔진] `main.rs:105` — Help 메시지 출력 추가**
   ```rust
   UserAction::Help => {
       println!("  📖 도움말:");
       println!("    숫자 1~{}: 선택지 선택", current_scene.choices.len());
       println!("    q: 게임 종료");
       println!("    h: 도움말 보기");
   }
   ```

---

### 🟡 BUG-010: 문체 토글 시 재귀 호출 — 3번 반복 시 스택 오버플로우 위험

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 |
| **현상** | 타이틀 메뉴에서 3번(문체 변경)을 반복 선택하면 `show_title_screen`이 재귀적으로 호출되어 스택이 쌓인다. 충분히 반복하면 스택 오버플로우가 발생한다. |
| **근거** | `main.rs:174` → `show_title_screen(state)` 재귀 호출. |

**수정 계획:**

1. **[엔진] `main.rs:168-176` — 재귀 대신 루프의 `continue` 사용**
   - `show_title_screen`을 단일 루프 기반으로 리팩터링하여 문체 변경 후 화면을 다시 그리고 입력을 대기하도록 수정.

---

### 🟡 BUG-011: `scene_retry` 실패 복구 전략이 씬을 되돌리지 않음

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 |
| **현상** | 수치가 0 이하로 떨어졌을 때 `scene_retry` 전략이 실행되면, 수치만 1로 복구될 뿐 현재 씬이 다음 씬으로 이미 이동된 상태다. 즉 재시도가 아니라 **그냥 통과**한다. |
| **근거** | `state.rs:85-113` → `apply_choice`에서 `advance_to`를 먼저 호출한 뒤 `main.rs:94`에서 `check_failure` 체크.<br>`state.rs:158-161` → `scene_retry` 시 `current_scene_id`를 되돌리지 않음. |

**수정 계획:**

1. **[엔진] `main.rs:89-99` — 실패 체크를 씬 이동 전에 수행하도록 순서 변경**
   ```rust
   UserAction::Select(idx) => {
       if let Some(choice) = current_scene.choices.get(idx) {
           let delta = choice.get_metric_delta();
           state.metric_value += delta;
           state.metric_value = state.metric_value.min(state.pack.meta.world.metric.max);
           
           if state.check_failure() {
               show_fail_screen(&current_scene, &state);
               state.handle_failure_return();
           } else {
               state.advance_to(&choice.next_scene);
           }
       }
   }
   ```

---

### 🟡 BUG-012: `modes`와 `characters` 설정 미파싱

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 엔진 코드 |
| **현상** | YAML에 정의된 `modes`(전체/맛보기)와 `characters`(흥부, 놀부, 아내, 화자) 데이터가 로드되지 않는다. `modes`는 빈 HashMap, `characters`는 기본값으로 채워진다. |
| **근거** | `loader.rs:208-209` → `modes: HashMap::new()`, `characters: CharactersConfig::default()` 하드코딩. |

**수정 계획:**

1. **[엔진] `loader.rs` — modes/characters 파싱 추가**
   - `modes`: `p.get("modes")` → `ModeConfig` HashMap 생성.
   - `characters`: `p.get("characters")` → protagonist, antagonist, guide, support 파싱.

---

### 🟢 BUG-013: 게임 오버(game_over) 시 아무 메시지 없이 프로그램 종료

| 항목 | 내용 |
|------|------|
| **심각도** | 🟢 LOW |
| **분류** | 엔진 코드 |
| **현상** | `game_over` 전략으로 실패 시, `is_finished = true`와 `game_over = true`가 동시에 설정된다. 루프를 빠져나가면 `if !state.game_over` 조건에 걸려 엔딩 화면도 출력되지 않고, 게임 오버 전용 메시지도 없이 프로그램이 그냥 꺼진다. |
| **근거** | `main.rs:111` → `if !state.game_over { render_ending_screen(...); }` — game_over 시 아무것도 출력 안 함. |

**수정 계획:**

1. **[엔진] `main.rs:110-115` — game_over 전용 화면 추가**
   ```rust
   if state.game_over {
       clear_screen();
       render_game_over_screen(&state);
       wait_for_enter();
   } else {
       clear_screen();
       render_ending_screen(&state);
       wait_for_enter();
   }
   ```

---

### 🟢 BUG-014: YAML 파서 — 이스케이프된 따옴표가 주석 파서를 오동작시킴

| 항목 | 내용 |
|------|------|
| **심각도** | 🟢 LOW |
| **분류** | 엔진 코드 |
| **현상** | YAML 문자열 안에 이스케이프된 따옴표(`\"`)가 있으면, `strip_comment` 함수가 `in_quote` 상태를 잘못 추적하여 문자열 중간에 있는 `#`을 주석으로 인식해 내용을 잘라버린다. |
| **근거** | `yaml_parser.rs:100-116` → `strip_comment` 함수에 `\"` 이스케이프 처리 없음. |

**수정 계획:**

1. **[엔진] `yaml_parser.rs:100-116` — 이스케이프 시퀀스 처리 추가**
   ```rust
   fn strip_comment(line: &str) -> &str {
       let mut in_quote = false;
       let mut quote_c = ' ';
       let mut prev_backslash = false;
       for (i, c) in line.char_indices() {
           if prev_backslash {
               prev_backslash = false;
               continue;
           }
           if c == '\\' {
               prev_backslash = true;
               continue;
           }
           if c == '"' || c == '\'' {
               if in_quote && c == quote_c {
                   in_quote = false;
               } else if !in_quote {
                   in_quote = true;
                   quote_c = c;
               }
           } else if c == '#' && !in_quote {
               return &line[..i];
           }
       }
       line
   }
   ```

---

### 🟢 BUG-015: YAML 파서 — `\\` (이중 백슬래시) 언이스케이프 누락

| 항목 | 내용 |
|------|------|
| **심각도** | 🟢 LOW |
| **분류** | 엔진 코드 |
| **현상** | YAML 문자열 `"text with \\\\"` → `\\`로 표시되어야 하지만, 파서가 `\\`를 그대로 통과시켜 `\\`가 2글자로 남는다. |
| **근거** | `yaml_parser.rs:254-257` → `replace("\\\"", "\"")`, `replace("\\n", "\n")` 만 있고 `replace("\\\\", "\\")` 없음. |

**수정 계획:**

1. **[엔진] `yaml_parser.rs:256` — `\\` 언이스케이프 추가**
   ```rust
   let unescaped = trimmed[1..trimmed.len() - 1]
       .replace("\\\\", "\x00BACKSLASH\x00")
       .replace("\\\"", "\"")
       .replace("\\n", "\n")
       .replace("\x00BACKSLASH\x00", "\\");
   ```

---

### 🔴 BUG-016: 터미널 단순 스트림 출력(`println!`)으로 인한 테두리 파편화 및 프레임 붕괴

| 항목 | 내용 |
|------|------|
| **심각도** | 🔴 CRITICAL |
| **분류** | 엔진 코드 (`renderer.rs`, `ending.rs`, `main.rs`) |
| **현상** | CJK 폰트 자폭 차이나 줄바꿈 누적으로 인해 우측 테두리(`║`)가 밀려나면서 화면 프레임이 깨지고 조각난 글자들이 흩뿌려짐. |
| **근거** | 단순 문자열 `println!` 방식은 이전 줄의 폭 오류가 다음 줄 테두리 위치에 누적되는 구조적 취약점이 있음. |

**수정 계획:**
1. **[엔진] `renderer.rs` — 2D 가상 화면 버퍼 (`ScreenBuffer[30][78]`) 구축**
   - 메모리에 78x30 크기의 셀 그리드를 만들고 5개 영역 테두리 뼈대를 먼저 각인.
   - 각 영역 내부 좌표에만 글자를 덮어쓰도록 하여 우측 테두리선(Col 77) 침범을 물리적으로 100% 차단.
   - `\x1b[H` 절대 커서 제어로 화면 깜빡임 없이 고정 프레임 덮어쓰기 출력.

---

## 📐 팩 데이터(양식) 수정 필요 항목

### 🟡 DATA-001: `scene_art` 아스키 그림의 흩뿌려진 기호 및 좌측 쏠림

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 팩 데이터 (`4_game_scene.yaml`) |
| **현상** | 아스키 기호(`~ ~ ~`, `>v<`, `凸`)들이 여백 속에 듬성듬성 배치되어 텍스트 파편처럼 보임. |
| **근거** | 8개 씬의 아스키 아트가 단편적인 기호 나열식으로 작성됨. |

**수정 계획:**
1. **[팩 데이터] 8개 전 씬의 아스키 아트를 74칸 박스형 중앙 정렬 완성형 일러스트로 전면 개편**
   - 대문, 초가 처마, 제비 비행 궤적, 황금 박, 화해의 악수 등 완성도 높은 장면 아트로 교체.

---

### 🟢 DATA-002: `pack.characters.support`에 도깨비, 빚쟁이 미등록

| 항목 | 내용 |
|------|------|
| **심각도** | 🟢 LOW |
| **분류** | 팩 데이터 (`4_game_scene.yaml`) |
| **현상** | 제6막 대화에서 `도깨비`와 `빚쟁이`가 발화자로 사용되지만, 조력자 목록에 미등록. |
| **근거** | YAML 155~162줄 vs YAML 566~574줄. |

**수정 계획:**
1. **[팩 데이터] `4_game_scene.yaml`의 `characters.support`에 `goblin`(`鬼`), `creditor`(`₩`) 추가**

---

### 🟡 DATA-003: 대화 문장의 과도한 길이로 인한 부호/따옴표 파편 분리

| 항목 | 내용 |
|------|------|
| **심각도** | 🟡 MEDIUM |
| **분류** | 팩 데이터 + 엔진 포맷터 (`4_game_scene.yaml`, `renderer.rs`) |
| **현상** | 40~70칸에 달하는 긴 문장이 38칸 제한에 걸려 느낌표(`!`)나 따옴표(`"`) 하나만 다음 줄로 넘어가는 파편 현상 발생. |
| **근거** | 1줄에 3개 이상의 문장이 줄바꿈 없이 하나의 대화 블록으로 묶여 있음. |

**수정 계획:**
1. **[팩 데이터] 1문장 1행 단위의 정갈한 대화문으로 전면 재작성.**
2. **[엔진] `format_dialogue_speaker`를 도입하여 화자명 기준 스마트 단어 줄바꿈 및 들여쓰기(`      `) 자동 적용.**

---

## 🔧 수정 작업 순서 (Priority Execution Order)

> [!IMPORTANT]
> **작은 모델이 작업을 시작할 때 반드시 이 순서대로 단계별 진행**하도록 지시하세요.

### Phase A: 핵심 기능 및 데드락 복구 (최우선 작업)

| 순서 | 티켓 | 변경 대상 | 테스트 방법 |
|------|------|-----------|-------------|
| 1 | **BUG-000** | `main.rs`, `input.rs` | 타이틀에서 [2] 암호 입력 및 [3] 문체 변경 시 데드락 없이 즉시 반응하는지 확인 |
| 2 | **BUG-006** | `width.rs` | `cargo test` + 메트릭 바(`███░░░`) 1칸 판정 및 상태창 테두리 정렬 육안 확인 |
| 3 | **BUG-001** | `loader.rs`, `state.rs`, `main.rs`, `renderer.rs`, `model.rs` | 5회 반복 실행하여 초기 톤 일관성 확인 + 톤 토글 후 대화/선택지 실제 변경 확인 |
| 4 | **BUG-004** | `input.rs` | 전환 씬에서 `q` 입력 → 즉시 종료 확인 |
| 5 | **BUG-003** | `main.rs` | 전환 씬에서 `q` 입력 → 엔딩 화면 없이 즉시 종료 확인 |

### Phase B: 화면 깨짐 및 줄바꿈 수정

| 순서 | 티켓 | 변경 대상 | 테스트 방법 |
|------|------|-----------|-------------|
| 6 | **BUG-005** | `ending.rs` | 엔딩 궤적 테이블 한글 자폭 정렬 육안 확인 |
| 7 | **BUG-007** | `renderer.rs` + `4_game_scene.yaml` | 대사 40칸 초과 시 잘림 없이 다음 줄로 줄바꿈 확인 |

### Phase C: 메뉴 및 기능 로직 보완

| 순서 | 티켓 | 변경 대상 | 테스트 방법 |
|------|------|-----------|-------------|
| 8 | **BUG-008** | `main.rs` | 타이틀에서 `5`, `a`, Enter 입력 → 안내 문구 출력 후 재입력 대기 확인 |
| 9 | **BUG-010** | `main.rs` | 문체 변경 10회 연속 실행 → 재귀 없이 정상 루프 동작 확인 |
| 10 | **BUG-011** | `main.rs`, `state.rs` | 수치 0 도달 → 현재 씬에서 정상 재시도(Retry) 확인 |
| 11 | **BUG-002** | `loader.rs` | YAML `failure` 및 `on_fail` 블록 정상 파싱 확인 |
| 12 | **BUG-009** | `main.rs` | 선택지에서 `h` 입력 → 도움말 안내 출력 확인 |
| 13 | **BUG-012** | `loader.rs` | modes/characters 정상 파싱 확인 |
| 14 | **BUG-013** | `main.rs` | game_over 시 전용 게임오버 화면 출력 확인 |

### Phase D: 파서 안정화 및 팩 데이터 정비

| 순서 | 티켓 | 변경 대상 | 테스트 방법 |
|------|------|-----------|-------------|
| 15 | **BUG-014** | `yaml_parser.rs` | 이스케이프 따옴표(`\"`) 포함 YAML 파싱 테스트 |
| 16 | **BUG-015** | `yaml_parser.rs` | `\\` 포함 아스키 아트 정상 출력 확인 |
| 17 | **DATA-002** | `4_game_scene.yaml` | 도깨비/빚쟁이 캐릭터 support 등록 확인 |

---

## 🏁 최종 검증 체크리스트

수정 완료 후 반드시 아래 항목을 순서대로 통과해야 합니다:

- [ ] `cargo test --target x86_64-unknown-linux-musl` 통과
- [ ] `cargo build --target x86_64-unknown-linux-musl --release` 빌드 성공 (크기 1MB 미만)
- [ ] 타이틀 메뉴 [2]번 암호("제비") 입력 시 제2막으로 즉시 점프
- [ ] 타이틀 메뉴 [3]번 문체 변경 시 데드락 없이 즉시 토글 반영
- [ ] 전환 씬에서 `q` 입력 시 즉시 게임 종료 (엔딩 화면 안 뜸)
- [ ] 7막 전체 플레이 후 엔딩 궤적 테이블 한글 정렬 칼각 유지
- [ ] 메트릭 바 `███░░░`와 상태창 우측 테두리 정렬 완벽 일치
- [ ] `D:\game\run_game.bat` 윈도우 11 실행 검증
- [ ] `todo.md`에 완료 일시 기록
