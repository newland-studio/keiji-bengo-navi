import json
from unittest.mock import patch, MagicMock


SAMPLE_FIRM = {
    "firm_name": "テスト刑事法律事務所",
    "lawyer_name": "鈴木 一郎",
    "prefecture": "tokyo",
    "phone": "03-9999-9999",
    "address": "東京都新宿区1-1-1",
    "website": "https://example.com",
    "crime_types_raw": ["刑事", "痴漢", "薬物"],
}

MOCK_API_RESPONSE = {
    "profile_text": "テスト刑事法律事務所は痴漢・薬物事件を専門に扱う事務所です。24時間対応で逮捕直後からサポートします。",
    "crime_types_normalized": ["chikan", "yakubutsu"],
    "is_24h": True,
    "chakushukin_min": 300000,
}


def _make_mock_message(content_text: str):
    mock_content = MagicMock()
    mock_content.text = content_text
    mock_message = MagicMock()
    mock_message.content = [mock_content]
    return mock_message


def test_generate_profile_returns_expected_fields():
    from scripts.generate import generate_profile

    mock_message = _make_mock_message(json.dumps(MOCK_API_RESPONSE))

    with patch("scripts.generate.client") as mock_client:
        mock_client.messages.create.return_value = mock_message
        result = generate_profile(SAMPLE_FIRM)

    assert "profile_text" in result
    assert "crime_types_normalized" in result
    assert "is_24h" in result
    assert "chakushukin_min" in result
    assert isinstance(result["crime_types_normalized"], list)
    assert isinstance(result["is_24h"], bool)
    assert isinstance(result["chakushukin_min"], int)


def test_generate_profile_uses_haiku_model():
    from scripts.generate import generate_profile

    mock_message = _make_mock_message(json.dumps(MOCK_API_RESPONSE))

    with patch("scripts.generate.client") as mock_client:
        mock_client.messages.create.return_value = mock_message
        generate_profile(SAMPLE_FIRM)

    call_kwargs = mock_client.messages.create.call_args.kwargs
    assert "haiku" in call_kwargs["model"]


def test_generate_all_merges_fields(tmp_path):
    from scripts.generate import generate_all

    input_path = str(tmp_path / "firms_raw.json")
    output_path = str(tmp_path / "firms_generated.json")

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump([SAMPLE_FIRM], f)

    mock_message = _make_mock_message(json.dumps(MOCK_API_RESPONSE))

    with patch("scripts.generate.client") as mock_client:
        mock_client.messages.create.return_value = mock_message
        generate_all(input_path, output_path)

    with open(output_path, encoding="utf-8") as f:
        results = json.load(f)

    assert len(results) == 1
    assert results[0]["firm_name"] == SAMPLE_FIRM["firm_name"]
    assert results[0]["profile_text"] == MOCK_API_RESPONSE["profile_text"]
