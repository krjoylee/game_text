#!/usr/bin/env bash
# ==============================================================================
# Divina Ludus (디비나 루두스) — WSL / Linux 런처 스크립트
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$SCRIPT_DIR/engine/target/x86_64-unknown-linux-musl/release/divina-ludus"

# 터미널 UTF-8 인코딩 설정
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8

# 화면 클리어
clear

echo "================================================================================"
echo "               🎮 Divina Ludus (신곡: 방황하는 자의 여정) — WSL 런처"
echo "================================================================================"
echo ""
echo "  플레이할 스토리 팩을 선택하세요:"
echo ""
echo "    [1] 흥부놀부전 (Heungbu and Nolbu) — 권선징악과 형제애"
echo "    [2] 제임스와 슈퍼 복숭아 (James and the Giant Peach) — 로알드 달 환상 모험"
echo "    [q] 종료"
echo ""
echo "================================================================================"
read -p "  선택 번호 입력 ▶ " choice

case "$choice" in
  1)
    echo "  [흥부놀부전]을 실행합니다..."
    "$BIN" --pack "$SCRIPT_DIR/packs/heungbu_nolbu/4_game_scene.yaml"
    ;;
  2)
    echo "  [제임스와 슈퍼 복숭아]를 실행합니다..."
    "$BIN" --pack "$SCRIPT_DIR/packs/james_peach/4_game_scene.yaml"
    ;;
  q|Q)
    echo "  게임을 종료합니다. 안녕히 가세요!"
    exit 0
    ;;
  *)
    echo "  올바른 번호를 선택해주세요."
    exit 1
    ;;
esac
