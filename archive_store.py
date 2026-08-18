# -*- coding: utf-8 -*-
"""
매일 수집된 원본 데이터를 날짜별 JSON으로 저장하고, 전체 이력을 불러옵니다.
data/YYYY-MM-DD.json 형태로 저장되며, 이 파일들은 GitHub 저장소에
그대로 커밋되어 영구 보관됩니다 (GitHub Actions가 매번 새로 커밋).
"""
import os
import json
from datetime import datetime

DATA_DIR = "data"
LAST_RUN_FILE = os.path.join(DATA_DIR, ".last_run.json")


def save_day(items: list, date_str: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{date_str}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"[저장] {path} ({len(items)}건)")


def load_all_days() -> list:
    """반환: [(date_str, items), ...] 날짜 오름차순 정렬"""
    if not os.path.isdir(DATA_DIR):
        return []

    result = []
    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".json"):
            continue
        date_str = filename[:-5]
        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            result.append((date_str, items))
        except Exception as e:
            print(f"[로드 오류] {path}: {e}")

    result.sort(key=lambda x: x[0])
    return result


def save_cumulative_csv(all_days: list, csv_path: str = os.path.join(DATA_DIR, "전체기록.csv")):
    """
    엑셀/구글시트에서 바로 열 수 있는 누적 CSV 생성.
    구글시트에서 열려면: 새 스프레드시트 만들기 -> 파일 -> 가져오기 -> 이 csv 업로드
    """
    import csv

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["날짜", "카테고리", "출처", "제목", "요약", "링크"])
        for date_str, items in all_days:
            for it in items:
                writer.writerow([
                    date_str,
                    it.get("category", ""),
                    it.get("source", ""),
                    it.get("title", ""),
                    it.get("summary", ""),
                    it.get("link", ""),
                ])

    print(f"[저장] {csv_path} (누적 {sum(len(items) for _, items in all_days)}건)")


def get_last_run_time():
    """
    지난번 실행 완료 시각(datetime, timezone-aware)을 반환.
    기록이 없으면(첫 실행) None을 반환.
    """
    if not os.path.exists(LAST_RUN_FILE):
        return None
    try:
        with open(LAST_RUN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return datetime.fromisoformat(data["last_run"])
    except Exception as e:
        print(f"[마지막 실행 시각 로드 오류] {e}")
        return None


def set_last_run_time(dt):
    """이번 실행 완료 시각을 저장 (다음 실행 때 이 시각부터 계산됨)"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LAST_RUN_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_run": dt.isoformat()}, f)
    print(f"[저장] 마지막 실행 시각 = {dt.isoformat()}")
