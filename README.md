# 刑事弁護ナビ（keiji-bengo-navi）

逮捕・刑事事件に直面した人が、都道府県×罪種×24h対応で弁護士を即座に探せるディレクトリメディア。

## クイックスタート

```bash
make setup          # 初回環境構築
# .env を編集してAPIキーを設定
make scaffold       # 都道府県×罪種ページ一括生成（初回のみ）
make collect        # 事務所データ収集
make generate       # AIプロフィール生成
# data/firms_generated.json をレビュー・修正
make all            # WP投入 → デプロイ
```

## 技術スタック

WordPress（ローカル）+ Simply Static → Cloudflare Pages（Wrangler CLI）

詳細は [設計仕様書](https://github.com/newland-studio/newland-workspace/blob/main/docs/superpowers/specs/2026-05-10-keiji-bengo-navi-design.md) を参照。
