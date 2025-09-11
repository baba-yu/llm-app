# 0週目まとめ (更新版 week0-2)

## 本番環境特有

- DB: 本番は **AWS RDS for PostgreSQL** を利用すること
- 接続設定: `.env` 経由で RDS の接続情報（ホスト・ユーザー・パスワード・DB名・ポート）を渡すこと
- pgvector: Django Migration (`RunSQL`) で  
  ```sql
  CREATE EXTENSION IF NOT EXISTS vector;
  ```
  を実行し、一貫性を確保すること

## 開発環境

- OS: **WSL2 (Ubuntu)**
- Python: **3.11.11（pyenv管理）**
- Django: **REST Framework, CORS, Redis対応 (django-redis)** を含む
- DB: **Docker Compose** で Postgres (5434) + pgvector 拡張  
  - イメージは **pgvector/pgvector:<固定タグ>** を利用すること  
  - 例: `pgvector/pgvector:0.8.0-pg16`
- Redis: **Docker Compose** で Redis (6380, requirepass 有効)
- Node.js: **v20 LTS（nvm管理）**
- Frontend: **Vue3 + Vite + TypeScript + Pinia + axios**
- その他:  
  - `.env` / `.env.example` による設定管理  
  - `.gitignore` で秘密情報や生成物を除外  

## 設計方針

- **pgvector拡張は Migration 管理に含める**  
  - 開発Dockerと本番RDSの両方で再現性を担保
- Redis はキャッシュ・セッション・短期記憶用に利用  
  永続性の必要なデータは PostgreSQL に保存
- CORS は開発中は全許可、本番は必要なオリジンに限定

## 成果 (0週目)

- **Monorepo 構成**を作成（backend, frontend, infra）
- Postgres / Redis を **Docker Compose** で起動し、`.env` による接続管理を統一
- Django `runserver` 起動確認済み
- `/api/health` API を `system` アプリに移設し、Redis・Postgres 両方の疎通確認を返すように実装  
  → `{"postgres": true, "redis": true}` を確認
- `.env.example` を整備し、チーム共有可能な形に更新

## 今回追加した成果

- **pgvector を Migration で有効化**
  - `core` アプリを作成し、空マイグレーションを追加  
  - `RunSQL("CREATE EXTENSION IF NOT EXISTS vector;", reverse_sql=noop)` を実装  
  - `python manage.py migrate` にて反映
- **DB/ユーザー作成確認**
  - `docker compose exec postgres psql -U postgres -d postgres -c "\l"` でDB一覧確認
  - DBが存在しない場合は `CREATE DATABASE llmapp OWNER llmuser;` を実施
- **固定タグ利用を徹底**  
  - `latest` は使用せず、Postgres メジャーに合わせたタグ (`0.8.0-pg16` など) を利用する  

## 学び

- プロジェクト名が `app` で混乱を招くためリファクタリング済み (`config` / `system` に分割)
- Redis / Postgres のヘルスチェックを Docker Compose に追加済み  
  CI/CD では `docker compose ps` による状態確認を利用可能
- SECRET_KEY に `$` を含めると Compose が変数展開してしまうので注意  
  → `$$` でエスケープするか、`$` を含まないキーを推奨
- RDS 環境では初回 `pgvector` 有効化に管理者権限が必要な場合がある

## 申し送り

- **ankane/pgvector** はすでに archived → 今後は **pgvector/pgvector** を利用すること  
  （infra/docker-compose.yml のイメージ指定を修正済み）
- 本番環境（RDS）向けに pgvector の確認・初期化を行う Migration コマンドを整備すること  
- CI/CD で自動化する際、**DB/ユーザー作成＋拡張有効化までをMigrationで担保**すること
