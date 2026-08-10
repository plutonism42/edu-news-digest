# -*- coding: utf-8 -*-
"""수집된 항목들을 Claude API로 정리(요약+카테고리 확인)합니다."""
import os
import json
import requests

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-6"

CATEGORY_LABELS = {
    "education": "교육",
    "science": "과학",
    "policy": "정책",
}


def summarize_items(items: list) -> list:
    """
    각 항목에 1~2줄 요약을 추가합니다.
    제목만으로 판단이 애매한 경우가 많아 '제목 기반 핵심 포인트'를 생성합니다.
    (본문 전체를 가져오려면 각 링크를 추가로 fetch해야 하며, 여기서는
     제목/출처만으로 가벼운 정리를 하는 1차 버전입니다.)
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or not items:
        for it in items:
            it["summary"] = ""
        return items

    # 한 번에 여러 건을 묶어서 요청 (토큰 절약)
    numbered = "\n".join(
        f"{i+1}. [{CATEGORY_LABELS.get(it['category'], it['category'])}/{it['source']}] {it['title']}"
        for i, it in enumerate(items)
    )

    prompt = f"""다음은 오늘 수집된 교육/과학/정책 관련 공지·뉴스 제목 목록입니다.
각 항목에 대해 제목만 보고 유추할 수 있는 핵심을 한국어로 1줄(20자 내외)로 정리해주세요.
과장하지 말고 제목에 담긴 사실만 간결하게 정리하세요.

{numbered}

반드시 아래 JSON 배열 형식으로만 답하세요. 다른 설명은 절대 추가하지 마세요.
[{{"index": 1, "summary": "..."}}, {{"index": 2, "summary": "..."}}, ...]
"""

    try:
        resp = requests.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        text = "".join(
            block.get("text", "") for block in data.get("content", [])
            if block.get("type") == "text"
        )
        text = text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text.split("\n", 1)[-1] if "\n" in text else text
        summaries = json.loads(text)
        summary_map = {s["index"]: s["summary"] for s in summaries}
    except Exception as e:
        print(f"[요약 오류] {e}")
        summary_map = {}

    for i, it in enumerate(items):
        it["summary"] = summary_map.get(i + 1, "")

    return items
