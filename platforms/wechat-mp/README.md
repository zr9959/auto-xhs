[中文](README.zh-CN.md) | English

# WeChat Official Accounts module: drafts + manual final publish

## Limits, stated first (must read)

- **Personal uncertified accounts cannot publish through the API**: publish, mass-send, menu, and tag endpoints all return unauthorized. This is not a credential problem — it's an account-type limit. Changing credentials or retrying won't fix it.
- So this module only goes as far as the draft box: articles get built in drafts, and final publish and mass-send happen manually in the web backend. Only enterprise certified accounts get the full API set.
- **Caller IP allowlist**: the official account API only accepts calls from allowlisted fixed egress IPs. A different egress IP gets an allowlist error. Confirm the call really goes out from an allowlisted address before checking anything else.

## Draft box operations

1. **Probe first**: before every call, run the probe — token exchange works, draft count and material count read back — only then is the call chain proven live.
2. **Create a draft**: title, summary, cover, body, and source link filled in one pass; AI-generated content labeled as the platform requires.
3. **Count drafts**: read the count after creating, and only count it as created when the number matches.
4. **Delete drafts**: delete test drafts right after creating them, then read the count again to confirm it went back.
5. **Reuse materials**: upload pictures and audio into the material library first, then reference them; check the material is in the library before publishing — don't upload on the spot and hit the rate limit.

## Content structure template

- **Title**: one sentence saying what the reader gets from this piece, no clickbait.
- **Summary**: two or three sentences with the core conclusion, without spoiling everything.
- **Cover**: one picture that matches the content, not a wordless pure video frame.
- **Body layout**: subheadings to split sections, key numbers and conclusions bolded, steps as lists; long paragraphs split short so they read easily on a phone.
- **Source link**: include it when there is one, never invent one.

## Publish checklist (manual final publish)

1. Build the article in the draft box and confirm by count.
2. Open the draft in the web backend and check item by item: title, summary, cover, body, links, AI label.
3. Publish by hand; record the link, and fill in readership data the next day.
4. After publishing, if you find a typo or factual error: follow the platform's edit rules for changing a draft and republishing — don't quietly swap the link.

## Error code quick reference

- **Allowlist error**: the calling address is not on the allowlist. Confirm which egress the call goes out from first, then change the allowlist — don't suspect the credentials first.
- **Token invalid or expired**: exchange a fresh token on every call; if it still reports invalid, it's a credential or account problem — check the credential file is there and the permissions are right.
- **Unauthorized**: the fixed answer for personal uncertified accounts calling publish, mass-send, menu, or tag endpoints. Don't retry, don't swap credentials — switch to manual final publish.

## Still to come

Topic picking, writing, layout style, and follower growth have no complete playbook yet — that part waits on the official-accounts line to supply it. This module only does drafts + manual final publish for now, and doesn't promise fully automated publishing.

## Runnable code (`scripts/`)

```bash
# 1. Turn a Markdown draft into a draft package (offline, no API calls)
python3 scripts/build_draft.py --md draft.md --title "Title" --author "Author" \
    --digest "Summary" --cover-media-id MEDIA_ID --out draft.json

# 2. Before calling the API, dry-run first (only prints which endpoint it would call and which fields it carries — no requests sent, no credentials printed)
MP_APPID=your-appid MP_SECRET=your-secret python3 scripts/mp_api.py --action probe --dry-run
MP_APPID=your-appid MP_SECRET=your-secret python3 scripts/mp_api.py --action draft-add \
    --draft-json draft.json --dry-run

# 3. Dry run looks good — drop --dry-run to really call
MP_APPID=your-appid MP_SECRET=your-secret python3 scripts/mp_api.py --action probe
MP_APPID=your-appid MP_SECRET=your-secret python3 scripts/mp_api.py --action draft-add \
    --draft-json draft.json
```

Credentials only come from environment variables, never from files. When the script errors, it says directly which case it is (40164 allowlist, 48001 unauthorized, token invalid) — no need to suspect the credentials first.

Test record (2026-10-25): Markdown-to-draft-package fields all present (title, author, summary, body HTML, cover media_id, comment switches); both dry-run steps passed without printing credentials; with no credentials given, exit code 2 with a prompt to set environment variables. Live API calls were not testable — they need your own official-account credentials + an allowlisted egress IP, so confirm both before running.
