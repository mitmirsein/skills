#!/zsh
# ============================================================
# google_scholar_quick_search.sh - Playwright CLI 기반 빠른 Scholar 검색
# ============================================================
# 용도: 간단한 Google Scholar 검색을 토큰 효율적으로 수행
# ============================================================

set -e

QUERY=$1
OUTPUT_DIR="${2:-/tmp/google-scholar-quick}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_ID="scholar_${TIMESTAMP}"

log() {
  echo "[$(date '+%H:%M:%S')] $1"
}

show_usage() {
  echo "📚 Google Scholar Quick Search - Playwright CLI"
  echo ""
  echo "Usage: $0 \"<search_query>\" [output_dir]"
  echo ""
  echo "Examples:"
  echo "  $0 \"Barth justification theology\""
  echo "  $0 \"Bonhoeffer ethics\" /path/to/output"
}

if [[ -z "$QUERY" ]]; then
  show_usage
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# URL 인코딩
ENCODED_QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")
SCHOLAR_URL="https://scholar.google.com/scholar?q=${ENCODED_QUERY}&hl=en"

log "🔍 Scholar 검색: $QUERY"
log "📂 출력: $OUTPUT_DIR"

# 1. 브라우저 열기
log "🌐 브라우저 세션 시작..."
playwright-cli -s="$SESSION_ID" open "$SCHOLAR_URL" 2>/dev/null || true
sleep 3

# 2. 스냅샷 캡처
log "📸 검색 결과 스냅샷..."
playwright-cli -s="$SESSION_ID" snapshot > "$OUTPUT_DIR/scholar_snapshot_${TIMESTAMP}.txt" 2>/dev/null || true

# 3. 스크린샷
log "🖼️ 스크린샷..."
playwright-cli -s="$SESSION_ID" screenshot > "$OUTPUT_DIR/scholar_screenshot_${TIMESTAMP}.png" 2>/dev/null || true

# 4. 검색 결과 추출 (제목 + 링크)
log "📋 논문 목록 추출..."
playwright-cli -s="$SESSION_ID" eval "JSON.stringify(Array.from(document.querySelectorAll('.gs_rt a')).slice(0, 10).map(function(a) { return {title: a.textContent, url: a.href}; }))" > "$OUTPUT_DIR/papers_${TIMESTAMP}.json" 2>/dev/null || true

# 5. 세션 종료
log "🔒 세션 종료..."
playwright-cli -s="$SESSION_ID" close 2>/dev/null || true

log "✅ 검색 완료"
echo ""
echo "=== SCHOLAR SEARCH SUMMARY ==="
echo "Query: $QUERY"
echo "Output: $OUTPUT_DIR"
echo ""
echo "📁 결과물:"
ls -la "$OUTPUT_DIR/"*${TIMESTAMP}* 2>/dev/null || echo "(파일 없음)"
echo ""
echo "📄 논문 목록:"
cat "$OUTPUT_DIR/papers_${TIMESTAMP}.json" 2>/dev/null || echo "(추출 실패)"
echo "==============================="
