"""
WP-CLI 経由で事務所データをWordPressへ一括投入するスクリプト。
USE_WPCLI=false の場合は REST API にフォールバック。
"""
import json
import subprocess
import time

import requests

from scripts.config import USE_WPCLI, WP_URL, WP_USER, WP_APP_PASSWORD


def _firm_to_meta(firm: dict) -> dict:
    return {
        "phone_24h": firm.get("phone", ""),
        "plan_tier": "free",
        "is_24h": str(firm.get("is_24h", False)),
        "free_consultation": "1",
        "hiyou_tokuya": "0",
        "chakushukin_min": str(firm.get("chakushukin_min", 300000)),
        "access_address": firm.get("address", ""),
        "profile_text": firm.get("profile_text", ""),
        "website_url": firm.get("website", ""),
        "tracking_url": firm.get("tracking_url", ""),
        "tracking_phone": firm.get("tracking_phone", ""),
    }


def import_via_wpcli(firm: dict) -> str:
    result = subprocess.run(
        [
            "wp", "post", "create",
            f"--post_title={firm['firm_name']}",
            "--post_type=law_firm",
            "--post_status=publish",
            "--porcelain",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [l for l in result.stdout.splitlines()
             if not l.startswith(("Deprecated:", "PHP Deprecated:", "Warning:", "Notice:"))]
    post_id = lines[-1].strip() if lines else result.stdout.strip()

    meta = _firm_to_meta(firm)
    for key, value in meta.items():
        subprocess.run(
            ["wp", "post", "meta", "update", post_id, key, value],
            check=True,
            capture_output=True,
        )

    for crime_slug in firm.get("crime_types_normalized", []):
        subprocess.run(
            ["wp", "post", "term", "add", post_id, "crime_type", crime_slug],
            check=True,
            capture_output=True,
        )

    subprocess.run(
        ["wp", "post", "term", "add", post_id, "prefecture", firm["prefecture"]],
        check=True,
        capture_output=True,
    )

    return post_id


def import_via_rest(firm: dict) -> str:
    auth = (WP_USER, WP_APP_PASSWORD)
    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/law_firm",
        auth=auth,
        json={"title": firm["firm_name"], "status": "publish"},
        timeout=10,
    )
    resp.raise_for_status()
    post_id = str(resp.json()["id"])

    meta = _firm_to_meta(firm)
    requests.post(
        f"{WP_URL}/wp-json/acf/v3/law_firm/{post_id}",
        auth=auth,
        json={"fields": meta},
        timeout=10,
    )

    time.sleep(0.5)
    return post_id


def import_all(input_path: str = "data/firms_generated.json") -> None:
    with open(input_path, encoding="utf-8") as f:
        firms = json.load(f)

    importer = import_via_wpcli if USE_WPCLI else import_via_rest

    for i, firm in enumerate(firms):
        print(f"[{i + 1}/{len(firms)}] {firm['firm_name']}")
        importer(firm)

    print(f"\nImported {len(firms)} firms")


if __name__ == "__main__":
    import_all()
