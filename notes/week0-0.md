# 要件

## 本番環境特有

- DB: 本番は AWS RDS for PostgreSQL を利用すること
- 接続設定: .env 経由で RDS の接続情報（ホスト・ユーザー・パスワード・DB名）を渡すこと
- pgvector: Django Migration (RunSQL) で CREATE EXTENSION IF NOT EXISTS vector; を実行し、一貫性を確保すること

## 開発環境

- OS: WSL2 (Ubuntu)
- Python: 3.11.11（pyenv管理）
- Django: REST Framework, CORS, Redis対応 (django-redis) を含む
- DB: Docker Compose で Postgres (5434) + pgvector 拡張
- Redis: Docker Compose で Redis (6380, requirepass 有効)
- Node.js: v20 LTS（nvm管理）
- Frontend: Vue3 + Vite + TypeScript + Pinia + axios
- その他: .env / .env.example による設定管理、.gitignore で秘密情報や生成物を除外

## 設計方針

- pgvector拡張は Django Migration に含め、開発Dockerと本番RDSの両方で再現性を担保する
- Redis はキャッシュ・セッション・短期記憶用に利用し、永続性の必要なデータは PostgreSQL に保存する
- CORS は開発中は全許可、本番は必要なオリジンに限定する

## 申し送り

- プロジェクト名が app で混乱を招くためリファクタリングを行うこと, app → core などサービス全体を示す名前に変更
- ヘルスチェックAPI (/api/health) を system アプリに移設すること
- Redis と Postgres の疎通確認を含めた View/URL を整理してヘルスチェックの続きをやる