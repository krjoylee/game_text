# Divina Ludus — 프로젝트 TODO & 실행 체계

> **최종 갱신**: 2026-09-02 14:26
> **관련 문서**: [philosophy.md](file:///home/krjoylee/code/game/philosophy.md) · [spec.md](file:///home/krjoylee/code/game/spec.md) · [tech_concepts.md](file:///home/krjoylee/code/game/tech_concepts.md) · [completion_report.md](file:///home/krjoylee/code/game/completion_report.md) · [bugfix_plan.md](file:///home/krjoylee/code/game/bugfix_plan.md) · [bugfix_report.md](file:///home/krjoylee/code/game/bugfix_report.md)

---

## 🏛️ 의사결정 및 개발 계층 구조 (Operating Hierarchy)

```
┌─────────────────────────────────────────────────────────────┐
│ 🥇 Level 1: 철학 (philosophy.md) — 최우선 원칙              │
│    • 게임이 아니라 게임을 만드는 엔진(메이커)이다.            │
│    • 팩(Pack) 교체만으로 어떤 고전문학이든 구동되어야 한다. │
│    • 원작 훼손 금지, 팩 간 완전 독립, 누구나 쉬운 오픈 포맷 │
├─────────────────────────────────────────────────────────────┤
│ 🥈 Level 2: 기술 규격 (spec.md) — 구현 기준                 │
│    • 78컬럼 5영역 카드 프레임 레이아웃 준수                 │
│    • 3대 진행 구조 (linear, growth, episodic) 지원          │
│    • Rust 단일 바이너리 (1MB 이하) 목표                     │
│    • 정해진 모듈 및 데이터 모델(Struct) 구조 준수          │
├─────────────────────────────────────────────────────────────┤
│ 🥉 Level 3: 실전 기술 (tech_concepts.md) — 단순화 패턴       │
│    • 데이터 주도 설계 (하드코딩 금지, YAML로 모든 로직 위임)│
│    • 템플릿 치환 ({placeholder} 활용 대사/문체 교체)         │
│    • GameState 단일 가방 패턴으로 상태 관리                 │
│    • unicode-width 기반 한글/특수문자 칼각 자폭 정렬        │
│    • 5영역 레고 블록 조립형 렌더링                          │
├─────────────────────────────────────────────────────────────┤
│ 🎯 Level 4: 실행 계획 (todo.md) — 빠짐없는 단계별 진행       │
│    • 한 번에 한 항목씩 구현 -> 테스트 검증 -> 완료 일시 기록│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔴 [Phase 1] 엔진 개발 & 윈도우 11 배포 (Rust Engine & Windows Deploy)

- [x] **E-00** Rust 개발 환경 및 빌드 툴체인 준비 (musl 정적 링크 툴체인 완비) (2026-09-01 12:01)
- [x] **E-01** `engine/` 디렉토리에 Rust 프로젝트 생성 (`cargo new --bin engine`) (2026-09-01 12:01)
- [x] **E-02** Cargo.toml 무의존성/초경량 릴리즈 최적화 구성 (`profile.release` LTO, z-opt) (2026-09-01 12:04)
- [x] **E-03** 데이터 모델 구현 (`engine/src/model.rs`) (2026-09-01 12:04)
  - `PackMeta`, `WorldConfig`, `MetricConfig`, `Scene`, `Choice`, `DialogueLine`, `EndingConfig` 등 정의
- [x] **E-04** 경량 순수 Rust YAML 팩 로더 구현 (`engine/src/yaml_parser.rs`, `engine/src/loader.rs`) (2026-09-01 12:06)
  - 팩 메타데이터 및 8개 씬 YAML 파싱 검증 완료
- [x] **E-05** 터미널 렌더러 기초 및 한글 자폭 계산기 구현 (`engine/src/width.rs`) (2026-09-01 12:04)
  - `str_display_width`, `pad_right`, `pad_center`, `truncate_to_width`
- [x] **E-06** 78컬럼 5영역 카드 프레임 렌더러 구현 (`engine/src/renderer.rs`) (2026-09-01 12:04)
  - Header(2줄) / Scene Art(14줄) / Dialogue(55%)+Status(45%)(7줄) / Choice(5줄)
- [x] **E-07** 게임 상태 머신 (`engine/src/state.rs`) (2026-09-01 12:03)
  - `GameState`, `apply_choice`, `advance_to`, `check_failure`, `handle_failure_return`
- [x] **E-08** 키보드 입력 핸들러 (`engine/src/input.rs`) (2026-09-01 12:05)
  - 번호 선택(1~N), 전환씬(Enter), 'q' 종료, EOF 안전 탈출
- [x] **E-09** 메인 게임 루프 (`engine/src/main.rs`) (2026-09-01 12:04)
  - 타이틀 화면 -> 문체 선택 -> 씬 루프 -> 엔딩 화면
- [x] **E-10** 암호(Password) 시스템 연동 (2026-09-01 12:04)
  - 챕터별 암호 입력 시 해당 씬으로 바로 이동
- [x] **E-11** 엔딩 화면 및 성향 분석 (`engine/src/ending.rs`) (2026-09-01 12:03)
  - 선택의 궤적 히스토리 표 및 성향 칭호 매칭
- [x] **E-12** CLI 인자 처리 (`--pack <path>`) (2026-09-01 12:04)
- [x] **E-13** 리눅스 정적 단일 바이너리 릴리즈 빌드 완료 (크기: **477KB**, 1MB 이하 목표 달성) (2026-09-01 12:06)
- [x] **E-14** 7막 전체 시나리오 플레이스루 통합 테스트 완료 (2026-09-01 12:06)
- [x] **E-15** 윈도우 11 배포 (`/mnt/d/game/`) 및 원클릭 실행 파일 구성 (2026-09-01 12:06)
  - `D:\game\run_game.bat`, `D:\game\run_terminal.bat`, `D:\game\안내문.txt` 생성 완료

---

## 🟠 [Phase 1.5] UI/화면 테두리 정밀 튜닝 (미해결 과제 / 추후 진행)

- [ ] **UI-01** 터미널 환경/폰트별 우측 테두리선(`║`) 및 여백 1px 칼각 정밀 보정
  - Windows Terminal / ConHost / WSL 환경별 전각/반각 폰트 렌더링 오차 완벽 튜닝
  - 가상 화면 버퍼 좌표계 및 패딩 여백 최종 미세 조정

---

## 🟡 [Phase 2] 팩 생성 도구 및 이미지 생성 엔진 (Tools & Engine)

- [x] **T-01** `4_game_scene.yaml` 흥부놀부전 7막+대체씬 전체 8씬 정식 완성 (2026-09-01 12:01)
- [ ] **T-02** 팩 유효성 검증 도구 (`tools/validate.sh`)
- [ ] **T-03** LLM 기반 팩 생성 Skill/MCP 워크플로우 명세
- [ ] **T-04** 빈 팩 템플릿 (`packs/_template/`) 패키징
- [x] **T-05** **아스키 아트 생성 엔진 (`AsciiArt Studio`) 구축** (2026-09-02 17:36)
  - 이미지 ➔ 74x23 씬 카드 규격 고밀도 Grayscale / Sobel Edge 변환 파이프라인
  - YAML 씬 아트 스니펫 자동 생성 CLI 저작 도구 ([tools/ascii_studio/ascii_studio.py](file:///home/krjoylee/code/game/tools/ascii_studio/ascii_studio.py))

---

## 🟢 [Phase 3] 추가 레퍼런스 팩 제작 (Expansion)

- [ ] **P-01** 단테 · 신곡 천국편 (`packs/paradiso/`) — Linear 구조
- [ ] **P-02** 헤르만 헤세 · 데미안 (`packs/demian/`) — Growth 구조
  - [x] **P-02-1** 원작 서사 정리 (`packs/demian/1_story.md`) (2026-09-02 15:05)
  - [x] **P-02-2** 서사 구조 설계 및 씬 그래프 (`packs/demian/1-1_story_structure.md`) (2026-09-02 15:05)
  - [x] **P-02-3** 9개 씬 아스키 아트 콘티 및 대사 초안 (`packs/demian/2_conti.md`) (2026-09-02 15:05)
  - [ ] **P-02-4** 씬 YAML 및 최종 패키징 (`3_scene.yaml`, `4_game_scene.yaml`)
- [ ] **P-03** 레프 톨스토이 · 단편집 (`packs/tolstoy_stories/`) — Episodic 구조
- [x] **P-04** **로알드 달 · 제임스와 슈퍼 복숭아 (`packs/james_peach/`) — Linear 모험 구조** (2026-09-02 20:16)
  - [x] **P-04-1** 원작 서사 정리 (`packs/james_peach/1_story.md`) (2026-09-02 20:12)
  - [x] **P-04-2** 서사 구조 설계 및 씬 그래프 (`packs/james_peach/1-1_story_structure.md`) (2026-09-02 20:12)
  - [x] **P-04-3** 8개 씬 시네마틱 아스키 콘티 및 대사 초안 (`packs/james_peach/2_conti.md`) (2026-09-02 20:12)
  - [x] **P-04-4** 씬 YAML 및 최종 패키징 (`3_scene.yaml`, `4_game_scene.yaml`) (2026-09-02 20:16)

---

## 📌 완료된 항목 총괄 (Done Summary)

- [x] **D-01** 프로젝트 철학 및 팩 분리 원칙 수립 (`philosophy.md`) (2026-09-01 07:45)
- [x] **D-02** 엔진 기술 스펙 및 13단계 상세 구현 계획 수립 (`spec.md`) (2026-09-01 10:16)
- [x] **D-03** 비개발자를 위한 5대 단순화 실전 기술 가이드 작성 (`tech_concepts.md`) (2026-09-01 11:53)
- [x] **D-04** 흥부놀부전 파일럿 원문 정리 (`packs/heungbu_nolbu/1_story.md`) (2026-09-01 08:44)
- [x] **D-05** 흥부놀부전 아스키 콘티 작성 (`packs/heungbu_nolbu/2_conti.md`) (2026-09-01 08:46)
- [x] **D-06** 흥부놀부전 구동용 초안 씬 작성 (`packs/heungbu_nolbu/3_scene.yaml`) (2026-09-01 08:48)
- [x] **D-07** 흥부놀부전 78컬럼 5영역 정식 씬 프레임 틀 생성 (`packs/heungbu_nolbu/4_game_scene.yaml`) (2026-09-01 10:13)
- [x] **D-08** 운영 하이라키(Level 1~4) 및 에이전트 작업 수칙 설정 (2026-09-01 11:56)
- [x] **D-09** 윈도우 11 배포 및 일시 표기 실행 체계 구성 (2026-09-01 12:01)
- [x] **D-10** Rust 엔진 코어 구현 및 477KB 정적 단일 바이너리 빌드 (2026-09-01 12:06)
- [x] **D-11** D:\game 배포 및 윈도우 11 원클릭 런처 완비 (2026-09-01 12:06)
- [x] **D-12** 흥부놀부전 1-1 서사 구조 설계 완료 (`packs/heungbu_nolbu/1-1_story_structure.md`) (2026-09-02 15:17)
- [x] **D-13** 기술 스펙에 5단계 팩 디자인 표준 파이프라인 반영 (`spec.md`) (2026-09-02 15:17)
- [x] **D-14** 78x40 고화질 시네마틱 프레임(23줄 캔버스) 및 고전 게임 인물 배치 렌더러 구현 배포 (2026-09-02 17:33)
- [x] **D-15** AsciiArt Studio 단독 이미지 생성 엔진 프로젝트 및 Sobel/Grayscale 74x23 변환기 구현 완료 (2026-09-02 17:36)
- [x] **D-16** 흥부놀부전 전체 8개 씬 74x23 시네마틱 고밀도 아스키 아트 생성 및 팩 전면 교체 배포 (2026-09-02 17:45)
- [x] **D-17** 6프레임 시네마틱 애니메이션 컷씬 재생 엔진 구현 및 흥부놀부전 1막 애니메이션 적용 배포 (2026-09-02 17:59)
- [x] **D-18** 《제임스와 슈퍼 복숭아》 팩 5단계 전 과정 완성 및 WSL 전용 원클릭 런처 (`run_game.sh`) 구축 (2026-09-02 20:16)

---

## 📝 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-09-01 | TODO 초판 작성 |
| 2026-09-01 | 운영 하이라키 및 윈도우 11 배포 체계 추가 |
| 2026-09-01 | **Phase 1 엔진 개발 전 항목(E-00~E-15) 및 윈도우 11 배포 완료 (실시간 타임스탬프 기록)** |
