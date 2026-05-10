"""
都道府県×罪種の組み合わせページ（470件）をWordPressへ一括生成する。
初回のみ実行: make scaffold
"""
import json
import subprocess

PREFECTURES_PATH = "data/prefectures.json"
CRIME_TYPES_PATH = "data/crime_types.json"


def scaffold_pages() -> None:
    with open(PREFECTURES_PATH, encoding="utf-8") as f:
        prefectures = json.load(f)
    with open(CRIME_TYPES_PATH, encoding="utf-8") as f:
        crime_types = json.load(f)

    total = len(prefectures) * len(crime_types)
    count = 0

    for pref in prefectures:
        for crime in crime_types:
            count += 1
            slug = f"ken-{pref['slug']}-{crime['slug']}"
            title = f"{pref['name']}で{crime['name']}に強い弁護士を今すぐ探す"

            result = subprocess.run(
                [
                    "wp", "post", "create",
                    f"--post_title={title}",
                    "--post_type=page",
                    "--post_status=publish",
                    f"--post_name={slug}",
                    "--porcelain",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            lines = [l for l in result.stdout.splitlines()
                     if not l.startswith(("Deprecated:", "PHP Deprecated:", "Warning:", "Notice:"))]
            post_id = lines[-1].strip() if lines else result.stdout.strip()

            meta = {
                "local_courthouse": pref["courthouse"],
                "local_bar_contact": pref["bar_contact"],
                "local_court_name": pref["court_name"],
                "prefecture_ref": pref["slug"],
                "crime_type_ref": crime["slug"],
                "seo_meta_title": (
                    f"{pref['name']}の{crime['name']}弁護士 | 刑事弁護ナビ"
                ),
                "seo_meta_desc": (
                    f"{pref['name']}で{crime['name']}事件の弁護士をお探しの方へ。"
                    f"24時間対応・費用特約対応の事務所を{pref['bar_contact']}の"
                    f"当番弁護士連絡先とあわせてご案内します。"
                ),
                "h1_heading": title,
            }

            for key, value in meta.items():
                subprocess.run(
                    ["wp", "post", "meta", "update", post_id, key, value],
                    check=True,
                    capture_output=True,
                )

            print(f"[{count}/{total}] Created: /{pref['slug']}/{crime['slug']}/")

    print(f"\nScaffolded {count} pages")


if __name__ == "__main__":
    scaffold_pages()
