# -*- coding: utf-8 -*-
"""
정적 HTML 페이지 생성기.

생성되는 페이지들:
- output/index.html            오늘자 랜딩(큰 버튼 3개 + 시계 + 새로고침 + 실패목록)
- output/education.html        오늘자 "교육분야" 카테고리 전체 목록
- output/policy.html           오늘자 "국가정책" 카테고리 전체 목록
- output/science.html          오늘자 "과학교육" 카테고리 전체 목록
- output/links.html            관련 기관 홈페이지 링크 모음
- output/archive/index.html    지금까지 쌓인 날짜별 아카이브 목록
- output/archive/{날짜}.html    특정 날짜의 종합 다이제스트(그날 전체 항목)
"""
import os
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

CATEGORY_ORDER = ["education", "policy", "science"]
CATEGORY_TEXT = {"education": "교육분야", "policy": "국가정책", "science": "과학교육"}
CATEGORY_EMOJI = {"education": "📘", "policy": "🏛", "science": "🔬"}
CATEGORY_COLOR = {"education": "#2563eb", "policy": "#7c3aed", "science": "#059669"}
CATEGORY_LABELS = {k: f"{CATEGORY_EMOJI[k]} {CATEGORY_TEXT[k]}" for k in CATEGORY_ORDER}

CATEGORY_PAGE_FILE = {
    "education": "education.html",
    "policy": "policy.html",
    "science": "science.html",
}

# 플루토쌤 저장소의 Actions 워크플로 페이지 (새로고침 버튼이 여기로 연결됨)
GITHUB_ACTIONS_URL = "https://github.com/plutonism42/edu-news-digest/actions/workflows/daily.yml"

BASE_STYLE = """
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    max-width: 720px; margin: 0 auto; padding: 24px 16px 80px;
    background: #fafaf8; color: #222; line-height: 1.6;
  }
  h1 { font-size: 22px; margin-bottom: 4px; }
  .updated { color: #888; font-size: 13px; margin-bottom: 12px; }
  .backlink { display: inline-block; margin-bottom: 16px; font-size: 13px; color: #2563eb; text-decoration: none; }
  .tabs { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
  .tabs a {
    font-size: 13px; padding: 6px 12px; border-radius: 16px; background: #eee;
    color: #555; text-decoration: none; font-weight: 600;
  }
  .tabs a.active { background: #222; color: #fff; }
  .archivelink { font-size: 13px; }
  .category { margin-bottom: 32px; }
  .category h2 { font-size: 17px; border-bottom: 2px solid #333; padding-bottom: 6px; }
  .item { padding: 12px 0; border-bottom: 1px solid #e5e5e0; }
  .item a.title { font-size: 15px; font-weight: 600; color: #1a1a1a; text-decoration: none; }
  .item a.title:hover { text-decoration: underline; }
  .item .meta { font-size: 12px; color: #999; margin-top: 3px; }
  .item .summary { font-size: 13px; color: #555; margin-top: 4px; }
  .empty { color: #aaa; font-size: 14px; padding: 12px 0; }
  details.more { margin-top: 4px; }
  details.more summary {
    cursor: pointer; color: #2563eb; font-size: 13px; font-weight: 600;
    padding: 10px 0; list-style: none;
  }
  details.more summary::-webkit-details-marker { display: none; }
  details.more summary::after { content: " ▾"; }
  details.more[open] summary::after { content: " ▴"; }
  .archive-list { list-style: none; padding: 0; }
  .archive-list li { padding: 10px 0; border-bottom: 1px solid #e5e5e0; }
  .archive-list a { color: #1a1a1a; text-decoration: none; font-weight: 600; }
  .archive-list .count { color: #999; font-size: 13px; margin-left: 8px; }
  .refresh-wrap { margin: 16px 0 24px; }
  .refresh-btn {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 700;
    text-decoration: none; background: #2563eb; color: #fff; border: none; cursor: pointer;
  }
  .refresh-btn.disabled {
    background: #eee; color: #999; cursor: not-allowed; pointer-events: none;
  }
  .refresh-note { font-size: 12px; color: #999; margin-top: 6px; }
  .clock-box {
    display: flex; justify-content: space-between; align-items: center;
    background: #fff; border: 1px solid #eee; border-radius: 12px;
    padding: 14px 16px; margin: 16px 0; font-size: 13px; color: #555;
  }
  .clock-box .now { font-size: 20px; font-weight: 700; color: #1a1a1a; font-variant-numeric: tabular-nums; }
  .clock-box .date { font-size: 13px; color: #888; margin-top: 2px; }
  .clock-box .elapsed { text-align: right; }
  .clock-box .elapsed b { color: #2563eb; }
  .landing-grid { display: flex; flex-direction: column; gap: 14px; margin: 20px 0; }
  .landing-card {
    display: flex; align-items: center; gap: 16px;
    padding: 22px 20px; border-radius: 18px; text-decoration: none;
    background: linear-gradient(135deg, var(--accent), var(--accent) 60%, #00000000);
    color: #fff; box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    transition: transform 0.15s ease;
  }
  .landing-card:active { transform: scale(0.98); }
  .landing-emoji { font-size: 34px; }
  .landing-text { flex: 1; }
  .landing-label { font-size: 19px; font-weight: 800; }
  .landing-count { font-size: 13px; opacity: 0.9; margin-top: 2px; }
  .landing-arrow { font-size: 22px; opacity: 0.85; }
  .links-card {
    display: flex; align-items: center; gap: 14px;
    padding: 16px 18px; border-radius: 14px; text-decoration: none;
    background: #fff; border: 1px solid #eee; margin: 8px 0 0;
  }
  .links-emoji { font-size: 30px; }
  .links-label { font-size: 17px; font-weight: 800; color: #1a1a1a; }
  .links-sub { font-size: 12px; color: #999; margin-top: 2px; }
  .inst-group { margin-bottom: 28px; }
  .inst-group h2 { font-size: 16px; border-bottom: 2px solid #333; padding-bottom: 6px; }
  .inst-list { list-style: none; padding: 0; margin: 8px 0 0; }
  .inst-list li { padding: 12px 0; border-bottom: 1px solid #e5e5e0; }
  .inst-list a { color: #1a1a1a; text-decoration: none; font-weight: 600; font-size: 15px; }
  .inst-list a:hover { text-decoration: underline; }
  .failed-box {
    background: #fff8e6; border: 1px solid #f5d98c; border-radius: 12px;
    padding: 14px 16px; margin: 16px 0; font-size: 13px;
  }
  .failed-box .failed-title { font-weight: 800; color: #92650a; margin-bottom: 6px; }
  .failed-box .failed-desc { color: #8a6d1f; margin-bottom: 10px; font-size: 12px; }
  .failed-box ul { list-style: none; padding: 0; margin: 0; }
  .failed-box li { padding: 6px 0; border-top: 1px solid #f0e0b0; }
  .failed-box li:first-child { border-top: none; }
  .failed-box a { color: #92650a; font-weight: 700; text-decoration: none; }
  .failed-box a:hover { text-decoration: underline; }
  .related-badge {
    display: inline-block; font-size: 11px; color: #7c3aed; background: #f3e8ff;
    padding: 2px 8px; border-radius: 10px; margin-left: 6px; font-weight: 700;
  }
"""

PAGE_SHELL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{style}</style>
</head>
<body>
{body}
</body>
</html>
"""

ITEM_TEMPLATE = """<div class="item">
  <a class="title" href="{link}" target="_blank" rel="noopener">{title}</a>
  <div class="meta">{source}{published}</div>
  {summary_html}
</div>
"""

VISIBLE_COUNT_PER_CATEGORY = 8


def _fmt_published(published_iso: str) -> str:
    if not published_iso:
        return ""
    try:
        dt = datetime.fromisoformat(published_iso).astimezone(KST)
        return f" · {dt.strftime('%m/%d %H:%M')}"
    except Exception:
        return ""


def _sort_items(items: list) -> list:
    items = list(items)
    items.sort(key=lambda it: it.get("published") or "", reverse=True)
    items.sort(key=lambda it: it.get("published") is None)
    return items


def _related_badge_html(it: dict) -> str:
    related = it.get("related_categories") or []
    if not related:
        return ""
    names = [CATEGORY_TEXT.get(c, c) for c in related]
    return f'<span class="related-badge">🔗 {", ".join(names)}에도 관련</span>'


def _render_items(items: list) -> str:
    return "\n".join(
        ITEM_TEMPLATE.format(
            link=it["link"],
            title=it["title"],
            source=it["source"],
            published=_fmt_published(it.get("published")),
            summary_html=(
                f'<div class="summary">{it["summary"]}{_related_badge_html(it)}</div>'
                if it.get("summary")
                else (f'<div class="summary">{_related_badge_html(it)}</div>' if it.get("related_categories") else "")
            ),
        )
        for it in items
    )


def _render_category_block(cat_key: str, label: str, cat_items: list, cap: int) -> str:
    if not cat_items:
        return f'<div class="category"><h2>{label} (0건)</h2><div class="empty">해당 기간 새 소식이 없어요.</div></div>'

    visible = cat_items[:cap] if cap else cat_items
    rest = cat_items[cap:] if cap else []

    html = f'<div class="category" id="cat-{cat_key}"><h2>{label} ({len(cat_items)}건)</h2>'
    html += _render_items(visible)
    if rest:
        html += f'<details class="more"><summary>{len(rest)}건 더보기</summary>{_render_items(rest)}</details>'
    html += "</div>"
    return html


def _tabs_html(active_key: str, category_hrefs: dict) -> str:
    parts = []
    for cat_key, label in CATEGORY_LABELS.items():
        cls = ' class="active"' if cat_key == active_key else ""
        parts.append(f'<a href="{category_hrefs[cat_key]}"{cls}>{label}</a>')
    return '<div class="tabs">' + "\n".join(parts) + "</div>"


def _clock_widget_html(last_updated_iso: str) -> str:
    """실시간 시계(한국시간) + '마지막 업데이트로부터 N시간 전' 표시"""
    return f"""
<div class="clock-box">
  <div>
    <div class="now" id="clock-now">--:--:--</div>
    <div class="date" id="clock-date">-</div>
  </div>
  <div class="elapsed" id="clock-elapsed"></div>
</div>
<script>
(function() {{
  var lastUpdated = new Date("{last_updated_iso}");
  var nowEl = document.getElementById('clock-now');
  var dateEl = document.getElementById('clock-date');
  var elapsedEl = document.getElementById('clock-elapsed');
  var dateFmt = new Intl.DateTimeFormat('ko-KR', {{ timeZone: 'Asia/Seoul', year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' }});
  var timeFmt = new Intl.DateTimeFormat('ko-KR', {{ timeZone: 'Asia/Seoul', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }});

  function tick() {{
    var now = new Date();
    nowEl.textContent = timeFmt.format(now);
    dateEl.textContent = dateFmt.format(now);

    var diffMs = now - lastUpdated;
    var diffH = Math.floor(diffMs / 3600000);
    var diffMForRemainder = Math.floor((diffMs % 3600000) / 60000);
    var text;
    if (diffH < 1) {{
      text = diffMForRemainder + '분 전 업데이트';
    }} else if (diffH < 24) {{
      text = diffH + '시간 ' + diffMForRemainder + '분 전 업데이트';
    }} else {{
      text = Math.floor(diffH / 24) + '일 전 업데이트';
    }}
    elapsedEl.innerHTML = '<b>' + text + '</b>';
  }}
  tick();
  setInterval(tick, 1000);
}})();
</script>
"""


def _refresh_button_html(last_updated_date_str: str) -> str:
    """
    오늘 이미 업데이트했으면 버튼을 자동으로 비활성화(회색)하고,
    아니면 GitHub Actions 실행 화면으로 연결되는 버튼을 만듭니다.
    """
    return f"""
<div class="refresh-wrap">
  <a id="refresh-btn" class="refresh-btn" href="{GITHUB_ACTIONS_URL}" target="_blank" rel="noopener">🔄 지금 새로고침</a>
  <div class="refresh-note" id="refresh-note"></div>
</div>
<script>
(function() {{
  var lastUpdated = "{last_updated_date_str}";
  var fmt = new Intl.DateTimeFormat('en-CA', {{ timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }});
  var todayKST = fmt.format(new Date());
  var btn = document.getElementById('refresh-btn');
  var note = document.getElementById('refresh-note');
  if (lastUpdated === todayKST) {{
    btn.classList.add('disabled');
    btn.textContent = '✅ 오늘은 이미 업데이트했어요';
    btn.removeAttribute('href');
    note.textContent = '내일 다시 새로고침할 수 있어요.';
  }} else {{
    note.textContent = 'GitHub 로그인 후 "Run workflow" 버튼을 한 번 더 눌러야 실제로 실행돼요.';
  }}
}})();
</script>
"""


def _landing_buttons_html(by: dict) -> str:
    cards = []
    for cat_key in CATEGORY_ORDER:
        count = len(by[cat_key])
        cards.append(f"""
<a class="landing-card" href="{CATEGORY_PAGE_FILE[cat_key]}" style="--accent: {CATEGORY_COLOR[cat_key]}">
  <div class="landing-emoji">{CATEGORY_EMOJI[cat_key]}</div>
  <div class="landing-text">
    <div class="landing-label">{CATEGORY_TEXT[cat_key]}</div>
    <div class="landing-count">{count}건 새 소식</div>
  </div>
  <div class="landing-arrow">→</div>
</a>""")
    return '<div class="landing-grid">' + "".join(cards) + "</div>"


def _links_button_html() -> str:
    return """
<a class="links-card" href="links.html">
  <div class="links-emoji">🔗</div>
  <div>
    <div class="links-label">관련 기관 홈페이지</div>
    <div class="links-sub">직접 방문해서 확인하기</div>
  </div>
</a>
"""


def _failed_sources_html(failed_sources: list) -> str:
    if not failed_sources:
        return ""

    rows = "\n".join(
        f'<li><a href="{f.get("url")}" target="_blank" rel="noopener">{f["name"]}</a></li>'
        for f in failed_sources
    )
    return f"""
<div class="failed-box">
  <div class="failed-title">⚠️ 오늘 접속이 안 된 사이트 ({len(failed_sources)}개)</div>
  <div class="failed-desc">네트워크 문제로 자동 수집에 실패했어요. 새 소식이 있을 수 있으니 직접 확인해보세요.</div>
  <ul>
    {rows}
  </ul>
</div>
"""


def generate_today_pages(items: list, date_str: str, output_dir: str, failed_sources: list = None):
    """오늘자 index.html(랜딩) + 카테고리별 전체 페이지 생성"""
    os.makedirs(output_dir, exist_ok=True)
    now_kst = datetime.now(KST)
    updated_str = now_kst.strftime("%Y년 %m월 %d일 %H:%M")
    updated_iso = now_kst.isoformat()

    by = {k: _sort_items([it for it in items if it.get("category") == k]) for k in CATEGORY_LABELS}

    # ── index.html (랜딩: 큰 버튼 3개만, 목록 없음) ──
    clock = _clock_widget_html(updated_iso)
    refresh_btn = _refresh_button_html(date_str)
    landing = _landing_buttons_html(by)
    links_btn = _links_button_html()
    failed_html = _failed_sources_html(failed_sources)
    body = f"""
<h1>📰 교육·과학·정책 데일리 다이제스트</h1>
<div class="updated">{updated_str} 기준 · 최근 24시간 수집</div>
{clock}
{landing}
{links_btn}
{refresh_btn}
{failed_html}
<div><a class="archivelink" href="archive/index.html">📂 지난 기록 전체 보기 →</a></div>
"""
    html = PAGE_SHELL.format(title="교육·과학·정책 데일리 다이제스트", style=BASE_STYLE, body=body)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # ── 카테고리별 전체 페이지 (더보기 없이 전부 표시) ──
    for cat_key, label in CATEGORY_LABELS.items():
        tabs = _tabs_html(active_key=cat_key, category_hrefs=CATEGORY_PAGE_FILE)
        section = _render_category_block(cat_key, label, by[cat_key], cap=0)
        body = f"""
<a class="backlink" href="index.html">← 오늘의 다이제스트로</a>
<h1>{label} 전체 목록</h1>
<div class="updated">{updated_str} 기준</div>
{tabs}
{section}
"""
        html = PAGE_SHELL.format(title=f"{label} - 데일리 다이제스트", style=BASE_STYLE, body=body)
        with open(os.path.join(output_dir, CATEGORY_PAGE_FILE[cat_key]), "w", encoding="utf-8") as f:
            f.write(html)

    print(f"[완료] index.html + 카테고리별 페이지 생성됨 (총 {len(items)}건)")


def generate_links_page(institution_links: list, output_dir: str):
    """기관별 홈페이지 링크 모음 페이지 생성 (links.html)"""
    os.makedirs(output_dir, exist_ok=True)

    groups_html = []
    for cat_key in CATEGORY_ORDER:
        label = CATEGORY_LABELS[cat_key]
        group_links = [l for l in institution_links if l["category"] == cat_key]
        if not group_links:
            continue
        rows = "\n".join(
            f'<li><a href="{l["url"]}" target="_blank" rel="noopener">{l["name"]}</a></li>'
            for l in group_links
        )
        groups_html.append(f'<div class="inst-group"><h2>{label}</h2><ul class="inst-list">{rows}</ul></div>')

    body = f"""
<a class="backlink" href="index.html">← 오늘의 다이제스트로</a>
<h1>🔗 관련 기관 홈페이지</h1>
<div class="updated">자동 수집이 안 되는 곳도 있어 직접 확인할 수 있게 모아뒀어요.</div>
{''.join(groups_html)}
"""
    html = PAGE_SHELL.format(title="관련 기관 홈페이지 - 데일리 다이제스트", style=BASE_STYLE, body=body)
    with open(os.path.join(output_dir, "links.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[완료] links.html 생성됨 ({len(institution_links)}개 기관)")


def generate_archive_pages(all_days: list, archive_dir: str):
    """
    all_days: [(date_str, items), ...] 오래된 날짜 -> 최신 날짜 순
    각 날짜별 종합 페이지 + 전체 목록 인덱스 페이지 생성
    """
    os.makedirs(archive_dir, exist_ok=True)

    for date_str, items in all_days:
        by_cat = {k: _sort_items([it for it in items if it.get("category") == k]) for k in CATEGORY_LABELS}
        sections = "".join(
            _render_category_block(k, label, by_cat[k], cap=0)
            for k, label in CATEGORY_LABELS.items()
        )
        body = f"""
<a class="backlink" href="index.html">← 아카이브 목록으로</a>
<h1>📰 {date_str} 다이제스트</h1>
<div class="updated">총 {len(items)}건 수집됨</div>
{sections}
"""
        html = PAGE_SHELL.format(title=f"{date_str} 다이제스트", style=BASE_STYLE, body=body)
        with open(os.path.join(archive_dir, f"{date_str}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    rows = "\n".join(
        f'<li><a href="{date_str}.html">{date_str}</a><span class="count">{len(items)}건</span></li>'
        for date_str, items in reversed(all_days)
    )
    if not rows:
        rows = '<div class="empty">아직 쌓인 기록이 없어요.</div>'

    body = f"""
<a class="backlink" href="../index.html">← 오늘의 다이제스트로</a>
<h1>📂 전체 아카이브</h1>
<div class="updated">총 {len(all_days)}일치 기록</div>
<ul class="archive-list">
{rows}
</ul>
"""
    html = PAGE_SHELL.format(title="아카이브 - 데일리 다이제스트", style=BASE_STYLE, body=body)
    with open(os.path.join(archive_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[완료] 아카이브 {len(all_days)}일치 페이지 생성됨")
