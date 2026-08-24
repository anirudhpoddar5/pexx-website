#!/usr/bin/env python3
"""Read PEXX Meta ad performance from the Marketing API.

Setup once:  put a Meta access token in pexx-shopify/.meta-token
Usage:       python3 scripts/meta_ads.py [days]   (default 7)

Read-only. Nothing here creates, edits, pauses or spends.
"""
import datetime, json, sys, urllib.request, urllib.parse, pathlib

ACT = "act_1350379969884972"         # PEXX ad account (the one the system user sees + billing runs through)
API = "https://graph.facebook.com/v21.0"
TOKEN = (pathlib.Path(__file__).parent.parent / ".meta-token").read_text().strip()


def get(path, **params):
    params["access_token"] = TOKEN
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get("error", {})
        sys.exit(f"Meta API error: {err.get('message', e)}")


def insights(level, days):
    fields = "campaign_name,adset_name,ad_name,spend,impressions,clicks,ctr,cpc,actions,action_values"
    # ponytail: explicit time_range, not date_preset — last_Nd excludes today and hid a live purchase
    today = datetime.date.today()
    since = today - datetime.timedelta(days=int(days) - 1)
    rows = get(f"{ACT}/insights", level=level, fields=fields, limit=200,
               time_range=json.dumps({"since": str(since), "until": str(today)})).get("data", [])
    return rows


def purchases(row):
    n = v = 0
    for a in row.get("actions", []):
        if a["action_type"] in ("purchase", "omni_purchase"):
            n = max(n, int(float(a["value"])))
    for a in row.get("action_values", []):
        if a["action_type"] in ("purchase", "omni_purchase"):
            v = max(v, float(a["value"]))
    return n, v


def main():
    days = sys.argv[1] if len(sys.argv) > 1 else "7"

    acct = get(ACT, fields="name,account_status,balance,amount_spent,currency")
    status = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_REVIEW",
              9: "IN_GRACE_PERIOD", 101: "CLOSED"}.get(acct["account_status"], acct["account_status"])
    print(f"{acct['name']} ({ACT}) — {status} — lifetime spend "
          f"{int(acct['amount_spent'])/100:,.0f} {acct['currency']}\n")

    camps = get(f"{ACT}/campaigns", fields="name,status,effective_status,daily_budget,objective",
                limit=200).get("data", [])
    live = [c for c in camps if c["effective_status"] not in ("ARCHIVED", "PAUSED", "DELETED")]
    print(f"Campaigns: {len(camps)} total, {len(live)} not paused/archived")
    for c in live:
        budget = int(c.get("daily_budget", 0)) / 100
        print(f"  [{c['effective_status']:<18}] {c['name'][:48]:<48} "
              f"{c.get('objective','-'):<22} ₹{budget:,.0f}/day")

    print(f"\nLast {days} days, by ad:")
    rows = insights("ad", days)
    if not rows:
        print("  no delivery in this window")
        return
    print(f"  {'ad':<40} {'spend':>8} {'impr':>7} {'clicks':>7} {'CTR':>6} "
          f"{'CPC':>7} {'buys':>5} {'revenue':>9} {'ROAS':>6}")
    for r in sorted(rows, key=lambda x: float(x.get("spend", 0)), reverse=True):
        spend = float(r.get("spend", 0))
        n, val = purchases(r)
        roas = val / spend if spend else 0
        print(f"  {r.get('ad_name','-')[:40]:<40} {spend:>8,.0f} {int(r.get('impressions',0)):>7,} "
              f"{int(r.get('clicks',0)):>7,} {float(r.get('ctr',0)):>5.2f}% "
              f"{float(r.get('cpc',0)):>7,.1f} {n:>5} {val:>9,.0f} {roas:>5.2f}x")

    tot_spend = sum(float(r.get("spend", 0)) for r in rows)
    tot_buys = sum(purchases(r)[0] for r in rows)
    tot_rev = sum(purchases(r)[1] for r in rows)
    print(f"\n  TOTAL  spend ₹{tot_spend:,.0f} · {tot_buys} purchases · revenue ₹{tot_rev:,.0f} · "
          f"ROAS {(tot_rev/tot_spend if tot_spend else 0):.2f}x · "
          f"CAC ₹{(tot_spend/tot_buys if tot_buys else 0):,.0f}")


if __name__ == "__main__":
    main()
