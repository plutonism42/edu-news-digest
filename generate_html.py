# -*- coding: utf-8 -*-
"""수집·요약된 항목들로 정적 HTML 페이지를 생성합니다."""
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

CATEGORY_LABELS = {
    "education": "📘 교육",
    "science": "🔬 과학",
    "policy": "🏛 정책",
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>교육·과학·정책 데일리 다이제스트</title>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    max-width: 720px; margin: 0 auto; padding: 24px 16px 80px;
    background: #fafaf8; color: #222; line-height: 1.6;
  }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .updated {{ color: #888; font-size: 13px; margin-bottom: 12px; }}
  .tabs {{ display: flex; gap: 8px; margin-bottom: 24px; position: sticky; top: 0; background: #fafaf8; padding: 8px 0; }}
  .tabs a {{
    font-size: 13px; padding: 6px 12px; border-radius: 16px; background: #eee;
    color: #555; text-decoration: none; font-weight: 600;
  }}
  .category {{ margin-bottom: 32px; }}
  .category h2 {{ font-size: 17px; border-bottom: 2px solid #333; padding-bottom: 6px; }}
  .item {{ padding: 12px 0; border-bottom: 1px solid #e5e5e0; }}
  .item a {{ font-size: 15px; font-weight: 600; color: #1a1a1a; text-decoration: none; }}
  .item a:hover {{ text-decoration: underline; }}
  .item .meta {{ font-size: 12px; color: #999; margin-top: 3px; }}
  .item .summary {{ font-size: 13px; color: #555; margin-top: 4px; }}
  .empty {{ color: #aaa; font-size: 14px; padding: 12px 0; }}
  details.more {{ margin-top: 4px; }}
  details.more summary {{
    cursor: pointer; color: #2563eb; font-size: 13px; font-weight: 600;
    padding: 10px 0; list-style: none;
  }}
  details.more summary::-webkit-details-marker {{ display: none; }}
  details.more summary::after {{ content: " ▾"; }}
  details.more[open] summary::after {{ content: " ▴"; }}
</style>
</head>
<body>
<h1>📰 교육·과학·정책 데일리 다이제스트</h1>
<div class="updated">{updated_str} 기준 · 최근 24시간 수집</div>
<div class="tabs">
  <a href="#cat-education">📘 교육</a>
  <a href="#cat-science">🔬 과학</a>
  <a href="#cat-policy">🏛 정책</a>
</div>
{sections}
</body>
</html>
"""

SECTION_TEMPLATE = """<div class="category" id="cat-{cat_key}">
  <h2>{label} ({count}건)</h2>
  {visible_items_html}
  {more_html}
</div>
"""

ITEM_TEMPLATE = """<div class="item">
  <a href="{link}" target="_blank" rel="noopener">{title}</a>
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


def generate_html(items: list, output_path: str):
    now_kst = datetime.now(KST)
    updated_str = now_kst.strftime("%Y년 %m월 %d일 %H:%M")

    sections_html = []
    for cat_key, label in CATEGORY_LABELS.items():
        cat_items = [it for it in items if it.get("category") == cat_key]
        if not cat_items:
            items_html = '<div class="empty">오늘은 새 소식이 없어요.</div>'
        else:
            items_html = "\n".join(
                ITEM_TEMPLATE.format(
                    link=it["link"],
                    title=it["title"],
                    source=it["source"],
                    published=_fmt_published(it.get("published")),
                    summary_html=f'<div class="summary">{it["summary"]}</div>' if it.get("summary") else "",
                )
                for it in cat_items
            )
        sections_html.append(SECTION_TEMPLATE.format(label=label, count=len(cat_items), items_html=items_html))

    html = HTML_TEMPLATE.format(updated_str=updated_str, sections="\n".join(sections_html))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[완료] {output_path} 생성됨 (총 {len(items)}건)")
