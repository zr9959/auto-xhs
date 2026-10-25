#!/usr/bin/env python3
"""Official-account API calls: probe + create draft. Credentials come only from environment variables, never from files.

Usage:
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action probe --dry-run
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action probe
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action draft-add \\
        --draft-json draft.json --dry-run
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action draft-add \\
        --draft-json draft.json

Two hard limits to know first (see the module README — read before running):
  1. The caller IP must be on the official-account backend allowlist, or the call fails with 40164 — confirm the egress IP first.
  2. Personal uncertified accounts cannot call publish or mass-send endpoints (48001); this script only probes and creates drafts,
     and final publishing happens manually in the web backend.
--dry-run only prints which endpoint it would call and which fields it carries — no requests sent, no credentials printed.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE = "https://api.weixin.qq.com"


def fail(msg, code=2):
    print(msg, file=sys.stderr)
    return code


def api_get(path, params):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    try:
        with urllib.request.urlopen(f"{BASE}{path}?{qs}", timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"errcode": e.code, "errmsg": f"HTTP {e.code}"}


def api_post(path, params, payload):
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(
        f"{BASE}{path}?{qs}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"errcode": e.code, "errmsg": f"HTTP {e.code}"}


def explain(res):
    code = res.get("errcode", 0)
    if code == 0:
        return None
    if code == 40164:
        return "40164: the calling address is not on the IP allowlist — confirm the egress IP first, then change the allowlist; don't suspect the credentials first."
    if code == 48001:
        return "48001: endpoint unauthorized. Personal uncertified accounts get this answer for publish, mass-send, menu, and tag endpoints — switch to manual final publish."
    if code in (40001, 42001):
        return "Token invalid or expired: check whether the credential file exists and the permissions are right."
    return f"API returned errcode={code} errmsg={res.get('errmsg')}"


def main():
    ap = argparse.ArgumentParser(description="Official-account API: probe + create draft")
    ap.add_argument("--action", choices=["probe", "draft-add"], required=True)
    ap.add_argument("--draft-json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    appid = os.environ.get("MP_APPID", "")
    secret = os.environ.get("MP_SECRET", "")
    if not appid or not secret:
        return fail("No credentials given: set the MP_APPID and MP_SECRET environment variables first (never in any repo file)")
    if args.action == "draft-add" and not args.draft_json:
        return fail("draft-add needs --draft-json with the package build_draft.py generated")

    if args.dry_run:
        print(f"[dry run] First call: GET /cgi-bin/token (token exchange, showing only the first 4 chars of appid, masked: {appid[:4]}****)")
        if args.action == "probe":
            print("[dry run] Then: GET /cgi-bin/draft/count (read draft count)")
        else:
            payload = json.loads(open(args.draft_json, encoding="utf-8").read())
            titles = [a.get("title", "") for a in payload.get("articles", [])]
            print(f"[dry run] Then: POST /cgi-bin/draft/add, {len(titles)} article{'s' if len(titles) != 1 else ''}: {titles}")
        print("[dry run] No requests sent. Drop --dry-run to really call.")
        return 0

    token_res = api_get("/cgi-bin/token", {
        "grant_type": "client_credential", "appid": appid, "secret": secret})
    hint = explain(token_res)
    if hint or "access_token" not in token_res:
        return fail("Token exchange failed: " + (hint or str(token_res)))
    token = token_res["access_token"]
    print("Token exchanged (value not printed).")

    if args.action == "probe":
        res = api_get("/cgi-bin/draft/count", {"access_token": token})
        hint = explain(res)
        if hint:
            return fail("Probe failed: " + hint)
        print(f"Probe passed: draft count {res.get('total_count')}")
        return 0

    payload = json.loads(open(args.draft_json, encoding="utf-8").read())
    res = api_post("/cgi-bin/draft/add", {"access_token": token}, payload)
    hint = explain(res)
    if hint:
        return fail("Draft creation failed: " + hint)
    print(f"Draft created: media_id {res.get('media_id')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
