# -*- coding: utf-8 -*-
"""
정적 HTML 페이지 생성기.

생성되는 페이지들:
- output/index.html            오늘자 종합 요약 (카테고리당 상위 8개 + 더보기)
- output/education.html        오늘자 "교육" 카테고리 전체 목록
- output/science.html          오늘자 "과학" 카테고리 전체 목록
- output/policy.html           오늘자 "정책" 카테고리 전체 목록
- output/archive/index.html    지금까지 쌓인 날짜별 아카이브 목록
- output/archive/{날짜}.html    특정 날짜의 종합 다이제스트(그날 전체 항목)
"""
import os
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

CATEGORY_LABELS = {
    "education": "📘 교육",
    "science": "🔬 과학",
    "policy": "🏛 정책",
}

CATEGORY_PAGE_FILE = {
    "education": "education.html",
    "science": "science.html",
    "policy": "policy.html",
}

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


def _render_items(items: list) -> str:
    return "\n".join(
        ITEM_TEMPLATE.format(
            link=it["link"],
            title=it["title"],
            source=it["source"],
            published=_fmt_published(it.get("published")),
            summary_html=f'<div class="summary">{it["summary"]}</div>' if it.get("summary") else "",
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


def generate_today_pages(items: list, date_str: str, output_dir: str):
    """오늘자 index.html + 카테고리별 전체 페이지(education/science/policy.html) 생성"""
    os.makedirs(output_dir, exist_ok=True)
    updated_str = datetime.now(KST).strftime("%Y년 %m월 %d일 %H:%M")

    by_cat = {k: _sort_items([it for it in items if it.get("category") == k]) for k in CATEGORY_LABELS}

    # ── index.html (요약: 카테고리당 상위 N개만) ──
    tabs = _tabs_html(active_key=None, category_hrefs=CATEGORY_PAGE_FILE)
    sections = "".join(
        _render_category_block(k, label, by_cat[k], cap=VISIBLE_COUNT_PER_CATEGORY)
        for k, label in CATEGORY_LABELS.items()
    )
    body = f"""
<h1>📰 교육·과학·정책 데일리 다이제스트</h1>
<div class="updated">{updated_str} 기준 · 최근 24시간 수집</div>
{tabs}
<div><a class="archivelink" href="archive/index.html">📂 지난 기록 전체 보기 →</a></div>
<br>
{sections}
"""
    html = PAGE_SHELL.format(title="교육·과학·정책 데일리 다이제스트", style=BASE_STYLE, body=body)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # ── 카테고리별 전체 페이지 (더보기 없이 전부 표시) ──
    for cat_key, label in CATEGORY_LABELS.items():
        tabs = _tabs_html(active_key=cat_key, category_hrefs=CATEGORY_PAGE_FILE)
        section = _render_category_block(cat_key, label, by_cat[cat_key], cap=0)
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


def generate_archive_pages(all_days: list, archive_dir: str):
    """
    all_days: [(date_str, items), ...] 오래된 날짜 -> 최신 날짜 순
    각 날짜별 종합 페이지 + 전체 목록 인덱스 페이지 생성
    """
    os.makedirs(archive_dir, exist_ok=True)

    # ── 날짜별 상세 페이지 ──
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

    # ── 아카이브 목록 (최신 날짜가 위로) ──
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
