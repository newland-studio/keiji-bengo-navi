import json
from unittest.mock import patch, MagicMock


SAMPLE_FIRM = {
    "firm_name": "テスト法律事務所",
    "prefecture": "tokyo",
    "phone": "03-1234-5678",
    "is_24h": True,
    "chakushukin_min": 300000,
    "crime_types_normalized": ["chikan", "yakubutsu"],
    "profile_text": "テストプロフィール文",
    "address": "東京都千代田区1-1",
    "website": "https://example.com",
    "tracking_url": "",
    "tracking_phone": "",
}


def _mock_run_factory(post_id="42"):
    def side_effect(args, **kwargs):
        mock = MagicMock()
        if args[1:3] == ["post", "create"]:
            mock.stdout = f"{post_id}\n"
        else:
            mock.stdout = ""
        return mock
    return side_effect


def test_import_via_wpcli_creates_post():
    from scripts.importer import import_via_wpcli

    with patch("subprocess.run", side_effect=_mock_run_factory("99")) as mock_run:
        post_id = import_via_wpcli(SAMPLE_FIRM)

    assert post_id == "99"
    create_call = mock_run.call_args_list[0][0][0]
    assert create_call[:3] == ["wp", "post", "create"]
    assert "--post_type=law_firm" in create_call


def test_import_via_wpcli_sets_meta_fields():
    from scripts.importer import import_via_wpcli

    with patch("subprocess.run", side_effect=_mock_run_factory("42")) as mock_run:
        import_via_wpcli(SAMPLE_FIRM)

    meta_calls = [
        c[0][0] for c in mock_run.call_args_list
        if c[0][0][1:3] == ["post", "meta"]
    ]
    meta_keys = [c[5] for c in meta_calls]
    assert "profile_text" in meta_keys
    assert "is_24h" in meta_keys
    assert "tracking_url" in meta_keys


def test_import_via_wpcli_assigns_taxonomies():
    from scripts.importer import import_via_wpcli

    with patch("subprocess.run", side_effect=_mock_run_factory("42")) as mock_run:
        import_via_wpcli(SAMPLE_FIRM)

    term_calls = [
        c[0][0] for c in mock_run.call_args_list
        if c[0][0][1:3] == ["post", "term"]
    ]
    assigned_terms = [(c[5], c[6]) for c in term_calls]
    assert ("crime_type", "chikan") in assigned_terms
    assert ("crime_type", "yakubutsu") in assigned_terms
    assert ("prefecture", "tokyo") in assigned_terms


def test_import_all_processes_all_firms(tmp_path):
    from scripts.importer import import_all

    firms = [SAMPLE_FIRM, {**SAMPLE_FIRM, "firm_name": "別の法律事務所"}]
    input_path = str(tmp_path / "firms_generated.json")
    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(firms, f)

    with patch("subprocess.run", side_effect=_mock_run_factory()):
        with patch("scripts.importer.USE_WPCLI", True):
            import_all(input_path)
