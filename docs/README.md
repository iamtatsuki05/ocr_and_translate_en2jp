## CI: HF→GitHub 同期（リリース連携）

参照資料（sync_hf_github.md）を基に、以下のGitHub Actionsを追加しました。

- `.github/workflows/hf_to_github.yml`: Webhook/`repository_dispatch` で即時同期（推奨）
- `.github/workflows/hf_to_github_cron.yml`: 定期同期（フォールバック）

設定手順:

- Secrets: `HF_TOKEN`（必要に応じて）をGitHubリポジトリに登録
- 変数: 各YAMLの `HF_REPO` と `REF` を環境に合わせて変更

使い方:

- 即時同期: `repository_dispatch`（type: `hf-sync`）で呼び出し
  - `client_payload` 例
    - `{"mode":"mirror","hf_repo":"org/name","skip_lfs":false}`
    - `{"mode":"main","hf_repo":"org/name"}`
    - `{"mode":"paths","hf_repo":"org/name","paths":["path/a","path/b"]}`
- 手動実行: Actionsの `Run workflow` から
- 定期同期: cronに従って自動実行
