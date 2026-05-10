"""
弁護士会公式名簿から事務所情報を収集するスクリプト。

収集ソース（優先順）:
1. 各都道府県弁護士会の公式事務所検索ページ（公開情報）
2. Google Maps Places API（任意・APIキーが必要）

注意: 各弁護士会のHTMLは異なるため、prefecture_slug ごとにパーサーを
      `_parse_firms_from_html()` 内で拡張すること。
"""
import json
import time
from typing import Optional, List

import requests
from bs4 import BeautifulSoup


BAR_ASSOCIATION_URLS: dict[str, str] = {
    "tokyo": "https://www.toben.or.jp/search/",
    # 他の都道府県は適宜追加
}


def collect_firms(
    prefectures: Optional[List[dict]] = None,
    output_path: str = "data/firms_raw.json",
) -> List[dict]:
    if prefectures is None:
        with open("data/prefectures.json", encoding="utf-8") as f:
            prefectures = json.load(f)

    firms: list[dict] = []
    for pref in prefectures:
        slug = pref["slug"]
        url = BAR_ASSOCIATION_URLS.get(slug)
        if not url:
            print(f"[SKIP] {pref['name']}: URLが未定義")
            continue

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            parsed = _parse_firms_from_html(resp.text, slug)
            firms.extend(parsed)
            print(f"[OK] {pref['name']}: {len(parsed)}件収集")
        except Exception as e:
            print(f"[ERR] {pref['name']}: {e}")

        time.sleep(1)

    return firms


def _parse_firms_from_html(html: str, prefecture_slug: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    firms: list[dict] = []
    # TODO: 各都道府県弁護士会のHTMLに合わせてパーサーを実装
    return firms


def save_firms(firms: list[dict], path: str = "data/firms_raw.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(firms, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(firms)} firms to {path}")


if __name__ == "__main__":
    firms = collect_firms()
    save_firms(firms)
