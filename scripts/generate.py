"""
Claude Haiku API を使い、事務所プロフィール文を一括生成するスクリプト。
入力: data/firms_raw.json
出力: data/firms_generated.json
"""
import json

import anthropic

from scripts.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

PROMPT_TEMPLATE = """以下の弁護士事務所情報から、刑事事件で逮捕された人の家族が
読む想定のプロフィール文（200字）を生成してください。

条件:
- 24時間対応の有無を明記（情報がない場合は「要確認」と記載）
- 得意な罪種（刑事事件の種類）を具体的に
- 初回相談の費用感に言及
- 「今すぐ相談できる」という緊急対応感を出す
- 過度な宣伝文句は避ける

事務所情報:
{firm_data}

以下のJSON形式のみで返してください（説明文や```は不要）:
{{
  "profile_text": "プロフィール文（200字以内）",
  "crime_types_normalized": ["chikan", "yakubutsu"],
  "is_24h": true,
  "chakushukin_min": 300000
}}

crime_types_normalized に使えるslug:
chikan, yakubutsu, sagi, shogai, sesshu, seihanzai, dv, shonen, kotsu, sonota"""


def generate_profile(firm: dict) -> dict:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[
            {
                "role": "user",
                "content": PROMPT_TEMPLATE.format(
                    firm_data=json.dumps(firm, ensure_ascii=False, indent=2)
                ),
            }
        ],
    )
    return json.loads(response.content[0].text)


def generate_all(
    input_path: str = "data/firms_raw.json",
    output_path: str = "data/firms_generated.json",
) -> None:
    with open(input_path, encoding="utf-8") as f:
        firms = json.load(f)

    results: list[dict] = []
    for i, firm in enumerate(firms):
        print(f"[{i + 1}/{len(firms)}] {firm['firm_name']}")
        generated = generate_profile(firm)
        results.append({**firm, **generated})

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nGenerated {len(results)} profiles → {output_path}")


if __name__ == "__main__":
    generate_all()
