import json
from unittest.mock import patch, MagicMock


def _mock_run(post_counter=None):
    if post_counter is None:
        post_counter = {"n": 0}

    def side_effect(args, **kwargs):
        mock = MagicMock()
        if args[1:3] == ["post", "create"]:
            post_counter["n"] += 1
            mock.stdout = f"{post_counter['n']}\n"
        else:
            mock.stdout = ""
        return mock
    return side_effect


def test_scaffold_creates_pages_for_all_combinations(tmp_path):
    prefectures = [
        {"name": "東京都", "slug": "tokyo",
         "courthouse": "東京拘置所", "bar_contact": "03-3580-0082", "court_name": "東京地裁"},
        {"name": "大阪府", "slug": "osaka",
         "courthouse": "大阪拘置所", "bar_contact": "06-6364-3591", "court_name": "大阪地裁"},
    ]
    crime_types = [
        {"name": "痴漢・盗撮", "slug": "chikan"},
        {"name": "薬物事件", "slug": "yakubutsu"},
    ]

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "prefectures.json").write_text(
        json.dumps(prefectures), encoding="utf-8"
    )
    (tmp_path / "data" / "crime_types.json").write_text(
        json.dumps(crime_types), encoding="utf-8"
    )

    counter = {"n": 0}
    with patch("subprocess.run", side_effect=_mock_run(counter)):
        with patch("scripts.scaffold.PREFECTURES_PATH",
                   str(tmp_path / "data" / "prefectures.json")):
            with patch("scripts.scaffold.CRIME_TYPES_PATH",
                       str(tmp_path / "data" / "crime_types.json")):
                from scripts import scaffold
                scaffold.scaffold_pages()

    # 2都道府県 × 2罪種 = 4ページ
    assert counter["n"] == 4


def test_scaffold_sets_seo_meta_fields(tmp_path):
    prefectures = [
        {"name": "東京都", "slug": "tokyo",
         "courthouse": "東京拘置所", "bar_contact": "03-3580-0082", "court_name": "東京地裁"},
    ]
    crime_types = [
        {"name": "痴漢・盗撮", "slug": "chikan"},
    ]

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "prefectures.json").write_text(json.dumps(prefectures))
    (tmp_path / "data" / "crime_types.json").write_text(json.dumps(crime_types))

    calls = []

    def record_run(args, **kwargs):
        calls.append(list(args))
        m = MagicMock()
        m.stdout = "1\n"
        return m

    with patch("subprocess.run", side_effect=record_run):
        with patch("scripts.scaffold.PREFECTURES_PATH",
                   str(tmp_path / "data" / "prefectures.json")):
            with patch("scripts.scaffold.CRIME_TYPES_PATH",
                       str(tmp_path / "data" / "crime_types.json")):
                from scripts import scaffold
                scaffold.scaffold_pages()

    # args: ["wp", "post", "meta", "update", post_id, key, value] → index 5 is key
    meta_keys = [c[5] for c in calls if c[1:3] == ["post", "meta"]]
    assert "seo_meta_title" in meta_keys
    assert "seo_meta_desc" in meta_keys
    assert "h1_heading" in meta_keys


def test_scaffold_sets_page_template(tmp_path):
    prefectures = [
        {"name": "東京都", "slug": "tokyo",
         "courthouse": "東京拘置所", "bar_contact": "03-3580-0082", "court_name": "東京地裁"},
    ]
    crime_types = [
        {"name": "痴漢・盗撮", "slug": "chikan"},
    ]

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "prefectures.json").write_text(json.dumps(prefectures))
    (tmp_path / "data" / "crime_types.json").write_text(json.dumps(crime_types))

    calls = []

    def record_run(args, **kwargs):
        calls.append(list(args))
        m = MagicMock()
        m.stdout = "1\n"
        return m

    with patch("subprocess.run", side_effect=record_run):
        with patch("scripts.scaffold.PREFECTURES_PATH",
                   str(tmp_path / "data" / "prefectures.json")):
            with patch("scripts.scaffold.CRIME_TYPES_PATH",
                       str(tmp_path / "data" / "crime_types.json")):
                from scripts import scaffold
                scaffold.scaffold_pages()

    meta_keys = [c[5] for c in calls if c[1:3] == ["post", "meta"]]
    assert "_wp_page_template" in meta_keys
    template_values = [c[6] for c in calls if c[1:3] == ["post", "meta"] and c[5] == "_wp_page_template"]
    assert template_values == ["page-ken-crime.php"]
