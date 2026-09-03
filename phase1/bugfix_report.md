# Divina Ludus — 버그 수정 완료 보고서 (Bugfix Completion Report)

> **작성일시**: 2026-09-02 15:00  
> **프로젝트**: 고전문학 텍스트 게임 메이커 엔진 (Universal Classic Literature Text Game Engine)  
> **관련 파일**: [bugfix_plan.md](file:///home/krjoylee/code/game/bugfix_plan.md) · [tech_concepts.md](file:///home/krjoylee/code/game/tech_concepts.md) · [todo.md](file:///home/krjoylee/code/game/todo.md)

---

## 1. 개요

`bugfix_plan.md`에 수립된 **엔진 버그 17건(데드락, 화면 고정 버퍼, 대사 포맷터 포함) 및 팩 데이터 이슈 3건**에 대해 전수 수정을 완료하고, 단위 테스트(`cargo test`), 단일 바이너리 릴리즈 빌드(498KB), 2D 가상 화면 버퍼(ScreenBuffer) 기반 실시간 렌더링 검증, 윈도우 11 배포(`D:\game\`)까지 완료하였습니다.

---

## 2. 버그별 원인 분석 및 해결 내역

| 티켓 번호 | 등급 | 발생 원인 | 해결 방법 | 적용 파일 |
|-----------|:---:|-----------|-----------|-----------|
| **BUG-000** | 🔴 CRITICAL | `show_title_screen`에서 `stdin.lock()`을 쥐고 있는 상태에서 `wait_for_enter()`가 `stdin.lock()`을 재호출하여 동일 스레드 Self-Deadlock 발생 (메뉴 2/3 진입 시 영구 멈춤) | `io::stdin().read_line()` 기반 직접 읽기로 전환하고 재진입 락 제거, 재귀 호출 대신 루프 `continue` 구조로 변경 | `input.rs`, `main.rs` |
| **BUG-001** | 🔴 CRITICAL | 팩 메타데이터 톤 키(`casual`/`classic`)와 대화/치환 데이터 톤 키(`tone_casual`/`tone_classic`)의 접두사 불일치 및 초기 톤 HashMap 랜덤 추출 | `tones.default` 기반 초기 톤 설정, 런타임에 `tone_` 접두사 유무와 무관하게 양방향 자동 정규화 조회 지원 | `loader.rs`, `model.rs`, `state.rs`, `renderer.rs`, `main.rs` |
| **BUG-002** | 🔴 CRITICAL | `loader.rs`에서 `world.failure` 및 각 씬의 `on_fail` 블록이 `None`으로 하드코딩되어 실패 시스템 미파싱 | `world.failure` 및 씬별 `on_fail`(speaker, text, return_to) 정상 역직렬화 로직 구현 | `loader.rs` |
| **BUG-003** | 🟠 HIGH | 전환 씬에서 `q` 입력 시 루프 `break` 후 엔딩 화면으로 진입 | `UserAction::Quit` 시 `return`으로 즉시 안전 종료 | `main.rs` |
| **BUG-004** | 🟠 HIGH | `input.rs`에서 `is_transition` 체크가 `q`/`quit` 체크보다 앞에 위치하여 `q`를 눌러도 다음 장면으로 강제 진행 | `q`/`quit` 종료 판정을 최우선으로 배치 | `input.rs` |
| **BUG-005** | 🟠 HIGH | 엔딩 궤적 테이블에서 Rust 기본 포맷터 `{:<10}` 사용으로 한글 2칸 자폭이 무시되어 테두리 깨짐 | 2D ScreenBuffer 기반 절대 그리드 좌표 배치 적용 | `ending.rs` |
| **BUG-006** | 🟠 HIGH | 블록 게이지 문자(`█`, `░`)가 `width.rs`에서 2칸으로 계산되어 10문자 게이지가 20칸을 차지하며 우측 테두리 침범 | Block Elements (`0x2580..=0x259F`) 자폭을 1칸으로 지정 | `width.rs` |
| **BUG-007** | 🟡 MEDIUM | 40칸 대화창에서 단순 글자 수 자르기로 인해 느낌표(`!`)나 따옴표(`"`)가 외톨이로 다음 줄에 파편처럼 떨어짐 | `format_dialogue_speaker`로 단어 단위 줄바꿈 및 둘째 줄 이후 스마트 들여쓰기 적용 | `renderer.rs` |
| **BUG-008** | 🟡 MEDIUM | 타이틀 메뉴에서 1/2/3/Q 이외 입력 시 즉시 게임 시작 | 안내 메시지 출력 및 `wait_for_enter` 후 메뉴 재표시 (`continue`) | `main.rs` |
| **BUG-009** | 🟡 MEDIUM | 선택지 화면에서 `h`/`help` 입력 시 핸들러 부재로 무시 | 도움말 안내 화면 및 계속 진행 프롬프트 추가 | `main.rs` |
| **BUG-010** | 🟡 MEDIUM | 문체 변경 3번 선택 시 `show_title_screen` 재귀 호출로 스택 누적 | 단일 루프 내 상태 갱신 및 `continue`로 리팩터링 | `main.rs` |
| **BUG-011** | 🟡 MEDIUM | `scene_retry` 실패 복구 시 씬 이동이 먼저 수행되어 실패한 씬을 통과해버림 | 실패 검사를 씬 이동 전에 수행하여 실패 시 현재 씬 유지 | `main.rs`, `state.rs` |
| **BUG-012** | 🟡 MEDIUM | `modes`와 `characters` 설정이 빈 값으로 하드코딩됨 | `modes`(전체/맛보기) 및 `characters`(주인공/악역/조력자) 정상 로딩 | `loader.rs` |
| **BUG-013** | 🟢 LOW | `game_over` 시 아무 화면 없이 프로세스 종료 | `render_game_over_screen` 전용 게임오버 카드 렌더러 추가 | `ending.rs`, `main.rs` |
| **BUG-014** | 🟢 LOW | YAML 문자열 내 `\"` 이스케이프가 주석 판정을 오동작시킴 | 이스케이프 백슬래시 상태 추적 로직 추가 | `yaml_parser.rs` |
| **BUG-015** | 🟢 LOW | YAML 파서에서 `\\` (이중 백슬래시) 언이스케이프 누락 | `\\` ➔ `\` 안전 치환 처리 | `yaml_parser.rs` |
| **BUG-016** | 🔴 CRITICAL | 터미널 단순 스트림 출력(`println!`)으로 인해 폰트별 폭 차이 발생 시 프레임 전체 붕괴 | **2D 가상 화면 버퍼(ScreenBuffer[30][78]) 및 ANSI 절대 커서 제어(\x1b[H)**를 도입하여 프레임 물리적 락 고정 | `renderer.rs`, `ending.rs`, `main.rs` |
| **DATA-001** | 🟡 MEDIUM | 씬 아트의 아스키 그림이 좁고 파편처럼 흩어져 있어 시각적 완성도 저하 | 8개 전 씬의 아스키 아트를 74칸 박스형 고밀도 중앙 정렬 아트로 전면 개편 | `4_game_scene.yaml` |
| **DATA-002** | 🟢 LOW | 제6막 대화의 발화자 `도깨비`, `빚쟁이`가 `characters.support`에 미등록 | `goblin`(`鬼`), `creditor`(`₩`) 추가 등록 | `4_game_scene.yaml` |
| **DATA-003** | 🟡 MEDIUM | YAML 대사 문장이 너무 길어 대화창에서 무분별한 쪼개짐 발생 | 1문장 1행 단위의 단정하고 리듬감 있는 대사문으로 정제 | `4_game_scene.yaml` |

---

## 3. 검증 결과

1. **단위 테스트**: `cargo test --target x86_64-unknown-linux-musl` 100% 통과 (8개 씬 파싱 및 검증 완료).
2. **바이너리 빌드**: 크기 **498 KB** (1MB 제한 완벽 준수, 순수 Rust 무의존성).
3. **2D 가상 화면 고정 검증**:
   - 타이틀 / 씬 1~7 / 실패 화면 / 엔딩 화면까지 우측 테두리선(`║`)이 1픽셀도 밀리지 않고 완벽한 직사각형 유지.
   - 대사 줄바꿈 시 화자명 다음 줄 들여쓰기 정상 적용되어 파편 찌꺼기 글자 완전 제거.
   - 8개 씬 아스키 아트가 중앙에 꽉 찬 고화질 삽화 형태로 단정하게 출력됨.
4. **배포**: `D:\game\divina-ludus` 및 `4_game_scene.yaml` 최신화 완료.

---

## 4. 향후 개발 시 재발 방지 대책 ([tech_concepts.md](file:///home/krjoylee/code/game/tech_concepts.md) 반영)

1. **2D ScreenBuffer 프레임 고정**: 터미널 출력은 단순 `println!` 대신 2D 메모리 버퍼에 테두리를 먼저 박고 사각 영역 안에만 덮어쓰기.
2. **스마트 대사 포맷팅**: 긴 대사는 화자 접두사를 고려한 단어 단위 줄바꿈과 들여쓰기(`      `)를 기본 적용.
3. **입력 락 수명 최소화**: `io::stdin().lock()` 중첩을 절대 금지하고 줄 단위 직접 읽기 사용.
4. **키 이름 양방향 정규화**: `tone_` 접두사 유무와 관계없이 유연하게 조회하는 방어적 로직 기본 탑재.
5. **명령어 우선 분기 원칙**: `q`, `h` 등 제어 명령어를 시나리오 전환 로직보다 항상 최우선 평가.
