#!/usr/bin/env python3
"""公众号 API 调用：探针 + 建草稿。凭据只从环境变量读，绝不写进文件。

用法：
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action probe --dry-run
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action probe
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action draft-add \\
        --draft-json draft.json --dry-run
    MP_APPID=xxx MP_SECRET=xxx python3 mp_api.py --action draft-add \\
        --draft-json draft.json

注意两条硬限制（见模块 README，先读再跑）：
  1. 调用方 IP 必须在公众号后台的白名单里，否则报 40164——先确认出口 IP。
  2. 个人未认证号调不通发布、群发接口（48001），本脚本只做探针和建草稿，
     最终发布在网页后台手动做。
--dry-run 只打印「会调哪个接口、带什么字段」，不发任何请求、不打印凭据。
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
        return "40164：调用地址不在 IP 白名单里——先确认出口 IP，再改白名单，不要先怀疑凭据。"
    if code == 48001:
        return "48001：接口未授权。个人未认证号调发布、群发、菜单、标签接口都是这个答案，改走手动终发。"
    if code in (40001, 42001):
        return "token 失效或过期：检查凭据文件在不在、权限对不对。"
    return f"接口返回 errcode={code} errmsg={res.get('errmsg')}"


def main():
    ap = argparse.ArgumentParser(description="公众号 API：探针 + 建草稿")
    ap.add_argument("--action", choices=["probe", "draft-add"], required=True)
    ap.add_argument("--draft-json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    appid = os.environ.get("MP_APPID", "")
    secret = os.environ.get("MP_SECRET", "")
    if not appid or not secret:
        return fail("凭据没给：先设环境变量 MP_APPID 和 MP_SECRET（不要写进文件或命令行历史里传给别人看）")
    if args.action == "draft-add" and not args.draft_json:
        return fail("draft-add 需要 --draft-json 传 build_draft.py 生成的包")

    if args.dry_run:
        print(f"[干跑] 会先调：GET /cgi-bin/token（换 token，只打码显示 appid 前 4 位：{appid[:4]}****）")
        if args.action == "probe":
            print("[干跑] 再调：GET /cgi-bin/draft/count（读草稿数）")
        else:
            payload = json.loads(open(args.draft_json, encoding="utf-8").read())
            titles = [a.get("title", "") for a in payload.get("articles", [])]
            print(f"[干跑] 再调：POST /cgi-bin/draft/add，文章 {len(titles)} 篇：{titles}")
        print("[干跑] 没发任何请求。去掉 --dry-run 才真调。")
        return 0

    token_res = api_get("/cgi-bin/token", {
        "grant_type": "client_credential", "appid": appid, "secret": secret})
    hint = explain(token_res)
    if hint or "access_token" not in token_res:
        return fail("换 token 失败：" + (hint or str(token_res)))
    token = token_res["access_token"]
    print("token 已换到（值不打印）。")

    if args.action == "probe":
        res = api_get("/cgi-bin/draft/count", {"access_token": token})
        hint = explain(res)
        if hint:
            return fail("探针失败：" + hint)
        print(f"探针通过：草稿数 {res.get('total_count')}")
        return 0

    payload = json.loads(open(args.draft_json, encoding="utf-8").read())
    res = api_post("/cgi-bin/draft/add", {"access_token": token}, payload)
    hint = explain(res)
    if hint:
        return fail("建草稿失败：" + hint)
    print(f"草稿已建：media_id {res.get('media_id')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
