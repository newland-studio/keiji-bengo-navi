.PHONY: collect generate import scaffold deploy all setup test

# ─────────────────────────────────────
# Step 1: データ収集・AI生成（レビュー前）
# ─────────────────────────────────────
collect:
	python scripts/collect.py

generate:
	python scripts/generate.py

# ─────────────────────────────────────
# Step 2: WP投入 → デプロイ（レビュー後）
# ─────────────────────────────────────
import:
	python scripts/importer.py

deploy:
	wp simply-static run --allow-root
	npx pagefind --site ./static-export --output-path ./static-export/pagefind
	wrangler pages deploy ./static-export --project-name=keiji-bengo-navi

# ─────────────────────────────────────
# 初回セットアップ専用
# ─────────────────────────────────────
scaffold:
	python scripts/scaffold.py

# ─────────────────────────────────────
# 環境構築（初回のみ）
# ─────────────────────────────────────
setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	npm install -g wrangler pagefind
	@which wp || (curl -sO https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp)
	cp .env.example .env
	@echo "⚠️  .env を編集してAPIキーを設定してください"
	@echo "⚠️  WP管理画面 Simply Static > Settings > Delivery Method を"
	@echo "    'Local Directory' に設定し、出力パスを ./static-export/ にしてください"

# ─────────────────────────────────────
# テスト
# ─────────────────────────────────────
test:
	.venv/bin/pytest tests/ -v

# ─────────────────────────────────────
# フルパイプライン（レビュー済みデータ前提）
# ─────────────────────────────────────
all: import deploy
