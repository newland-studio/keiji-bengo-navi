import json
from unittest.mock import patch, MagicMock


def test_save_firms_writes_json(tmp_path):
    from scripts.collect import save_firms

    firms = [
        {
            "firm_name": "テスト法律事務所",
            "lawyer_name": "山田 太郎",
            "prefecture": "tokyo",
            "phone": "03-1234-5678",
            "address": "東京都千代田区1-1-1",
            "website": "https://example.com",
            "crime_types_raw": ["刑事", "痴漢"],
        }
    ]
    output_path = str(tmp_path / "firms_raw.json")
    save_firms(firms, output_path)

    with open(output_path, encoding="utf-8") as f:
        saved = json.load(f)

    assert len(saved) == 1
    assert saved[0]["firm_name"] == "テスト法律事務所"
    assert saved[0]["prefecture"] == "tokyo"


def test_collect_firms_returns_list():
    from scripts.collect import collect_firms

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body></body></html>"

    with patch("scripts.collect.requests.get", return_value=mock_response):
        result = collect_firms(prefectures=[
            {"slug": "tokyo", "name": "東京都"}
        ])

    assert isinstance(result, list)
