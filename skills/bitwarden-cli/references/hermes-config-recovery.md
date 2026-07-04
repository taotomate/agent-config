# Hermes Config Recovery After Reinstallation

When Hermes is reinstalled and the `.env` is wiped, recover settings from state snapshots.

## Discovery
Hermes stores pre-update snapshots at:
```
hermes-data/state-snapshots/<timestamp>-pre-update/.env
```

## Recovery Steps

### 1. Locate the snapshot
```bash
ls hermes-data/state-snapshots/
```
The most recent snapshot before the reinstall contains the complete `.env`.

### 2. Restore .env
```bash
cp hermes-data/state-snapshots/<timestamp>-pre-update/.env ~/.hermes/.env
```

### 3. Verify auth.json credential pool
The `auth.json` at `hermes-data/auth.json` contains a `credential_pool` with API keys that Hermes auto-loads. Check status:
```bash
python -c "import json; d=json.load(open('hermes-data/auth.json')); [print(f'{p}: {c.get(\"label\")} status={c.get(\"last_status\",\"?\")}') for p,creds in d.get('credential_pool',{}).items() for c in creds]"
```

### 4. Check for broken rate limits
If a provider shows `status=exhausted` with `last_error_code=429`, the daily free tier limit was hit. The key itself is still valid — it will reset at `last_error_reset_at`.

### 5. Skills backup
Skills are preserved in `~/.hermes/skills/` across reinstalls. A backup exists at:
```
~/.hermes/skills.bak_<timestamp>/
```
Newer installs may have additional skills not in the backup — this is expected.

## Key Insight
The `.env` file in Hermes is primarily for **new** configuration. Active runtime credentials live in `auth.json`'s `credential_pool`. Restoring `.env` preserves comments and structure; the credential_pool preserves actual working keys.
