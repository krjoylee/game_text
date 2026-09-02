# 🎮 Divina Ludus (디비나 루두스)

> **"1MB 미만의 미학 — 텍스트와 서브픽셀 도트로 빚어내는 고전 시네마틱 텍스트 어드벤처"**  
> 고전 명작 문학의 감동을 터미널 속 78×40 시네마틱 프레임과 순차 애니메이션 컷씬으로 복원하는 독립 게임 엔진 & 스토리 팩 플랫폼입니다.

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Engine](https://img.shields.io/badge/engine-Rust%20(Zero%20Dependency)-orange.svg)](engine/)
[![Binary Size](https://img.shields.io/badge/binary-~500KB%20(musl%20static)-green.svg)](engine/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL%20%7C%20Windows-lightgrey.svg)](run_game.sh)

---

## 📖 프로젝트 소개

**Divina Ludus(디비나 루두스)**는 수십 기가바이트의 용량과 화려한 3D 엔진이 범람하는 시대에, **"과거 1MB 롬팩에 모든 세계를 담아내던 고전 명작 게임들의 극소 용량 미학과 상상력"**을 현대적인 기술로 되살리는 프로젝트입니다.

엔진 코어는 외부 런타임 의존성 없는 **순수 Rust 500KB 단일 정적 바이너리**로 구동되며, 고전 명작 어드벤처(PC-98, 패미컴, MSX)의 문법을 현대 터미널에 계승하였습니다.

---

## ✨ 핵심 특징 (Key Features)

1. **초경량 독립 런타임 (Ultra Lightweight & Standalone)**
   * Rust `musl` 타겟의 **단일 500KB 바이너리** (DLL, 런타임, 외부 프레임워크 설치 불필요).
   * 윈도우 11, WSL, Linux 터미널 어디서든 즉시 실행 가능.

2. **78×40 시네마틱 5영역 화면 버퍼 (2D Virtual Screen Buffer)**
   * ANSI 커서 절대 좌표 제어를 통해 화면 깜빡임(Flicker) 없는 부드러운 고정 프레임 렌더링.
   * **Scene Art(23줄)**, **Dialogue(8줄)**, **Status(8줄 게이지)**, **Choice(4줄)**의 완벽한 정보 구획.

3. **8배 초고해상도 서브픽셀 도트 & 시네마틱 애니메이션 컷씬**
   * **Braille Subpixel**: 1문자 공간을 2×4 서브픽셀로 쪼개어 가로 148 × 세로 92 픽셀 수준의 인물 흉상/표정 도트 구현.
   * **6-Frame Cutscene**: 씬 진입 시 0.35초 간격으로 연속 재생되는 고전 게임 스타일 컷씬 애니메이션 엔진 탑재.

4. **문체 전환 & 5단계 표준 팩 디자인 파이프라인**
   * 하나의 스토리를 **현대 구어체(Casual)**와 **고전 문학체(Classic)**로 실시간 스위칭.
   * `1_원작 서사` ➔ `1-1_서사 구조 설계` ➔ `2_아스키 콘티` ➔ `3_프로토타입 YAML` ➔ `4_정식 게임 팩`의 체계적인 저작 파이프라인.

---

## 📚 수록 스토리 팩 (Story Packs)

| 팩 ID | 작품명 | 원작 / 테마 | 서사 구조 | 핵심 수치 (Metric) |
|:---:|:---|:---|:---:|:---:|
| `heungbu_nolbu` | **흥부놀부전** | 한국 고전 설화 · 권선징악과 형제의 정 | Linear | 선행의 씨앗 (♧ 0~10) |
| `james_peach` | **제임스와 슈퍼 복숭아** | 로알드 달 · 대서양 횡단 환상 모험 | Linear | 모험의 용기 (★ 0~10) |
| `demian` *(기획 완료)* | **데미안** | 헤르만 헤세 · 알을 깨고 나오는 성장 | Growth | 자아의 빛 (✧ 0~10) |

---

## 🚀 빠른 시작 (Quick Start)

### 1. Linux / WSL 환경

```bash
# 리포지토리 클론
git clone https://github.com/krjoylee/game_text.git
cd game_text

# WSL 원클릭 런처 실행
./run_game.sh
```

직접 특정 팩을 실행하려면:
```bash
./engine/target/x86_64-unknown-linux-musl/release/divina-ludus --pack packs/heungbu_nolbu/4_game_scene.yaml
```

### 2. Windows 11 환경

* WSL에서 빌드된 정적 바이너리와 배포 팩은 `D:\game` 경로에서 배치 파일(`run_game.bat`)을 통해 바로 구동할 수 있습니다.

---

## 🛠️ 자체 제작 도구: AsciiArt Studio (`tools/ascii_studio/`)

텍스트 게임의 해상도 한계를 극복하기 위해 프로젝트 내부에 탑재된 단독 이미지 변환 툴체인입니다:
* **Zero-Dependency**: 외부 라이브러리 없이 순수 Python 표준 라이브러리로 작동하는 BMP/PNM 디코더.
* **Sobel Edge & Bilinear Scaling**: 인물 흉상 외곽선 추출 및 명암 대비 보정.
* **Braille 8x Dot Generator**: 148×92 도트를 74×23 터미널 유니코드로 즉시 압축 변환 및 YAML 내보내기 지원.

```bash
# 이미지 파일 ➔ 8배 초고해상도 Braille 도트 변환
python3 tools/ascii_studio/ascii_studio.py <image_path> --format braille
```

---

## 🏛️ 프로젝트 아키텍처 및 철학

* [philosophy.md](philosophy.md): 프로젝트 개발 철학 및 엔진-팩 분리 원칙
* [spec.md](spec.md): 게임 런타임 엔진 기술 규격서 (78×40 프레임 레이아웃)
* [spec_image_engine.md](spec_image_engine.md): AsciiArt Studio 이미지 저작 엔진 규격서
* [tech_concepts.md](tech_concepts.md): 비개발자를 위한 5대 핵심 기술 개념 가이드
* [todo.md](todo.md): 단계별 마일스톤 및 완료 이력 (D-01 ~ D-20)

### 📌 버전 관리 원칙 (Git Commit Convention)
* 모든 커밋 메시지는 **한글로 작성**합니다.
* 단순 작업 나열이 아닌 **"무엇이 안 되거나 부족하여 ➔ 어떤 목적을 위해 무엇을 해결했는가"**의 목적 중심 인과관계를 명시합니다.

---

## 📜 라이선스

This project is licensed under the MIT License.
