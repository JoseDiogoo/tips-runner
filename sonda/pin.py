import json, urllib.request
B = "https://guest.api.arcadia.pinnacle.com/0.1"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(B + p, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}), timeout=30))
want = ("premier league", "la liga", "serie a", "bundesliga", "ligue 1", "champions league", "europa league", "conference league", "primeira", "liga portugal", "eredivisie", "championship", "nba")
for sid in (29, 4):
    ls = get(f"/sports/{sid}/leagues")
    print("LIGAS", sid, [(x["id"], x["group"] + " | " + x["name"], x["matchupCount"]) for x in ls if any(w in x["name"].lower() for w in want) and x["matchupCount"]])
def first(sid, key):
    for x in get(f"/sports/{sid}/leagues"):
        if key in x["name"].lower() and x["matchupCount"]: return x["id"]
for sid, key in ((29, "premier league"), (29, "champions league"), (4, "nba")):
    lid = first(sid, key)
    if not lid: print("sem", key); continue
    ms = get(f"/leagues/{lid}/matchups"); ks = get(f"/leagues/{lid}/markets/straight")
    print("\n#### LIGA", lid, key, "matchups", len(ms), "markets", len(ks))
    print("tipos de matchup:", sorted({(m.get("type"), bool(m.get("parentId"))) for m in ms}))
    main = [m for m in ms if m.get("type") == "matchup" and not m.get("parentId")][:2]
    for m in main:
        print("MATCHUP", json.dumps({k: m.get(k) for k in ("id", "type", "isLive", "startTime", "status")} | {"participants": [{k: p.get(k) for k in ("id", "alignment", "name")} for p in m["participants"]], "periods": [(p.get("period"), p.get("description"), p.get("cutoffAt"), p.get("status")) for p in m.get("periods", [])][:3]}, ensure_ascii=False))
        mine = [k for k in ks if k["matchupId"] == m["id"]]
        print(" tipos/periodos:", sorted({(k["type"], k["period"], k.get("isAlternate", False)) for k in mine})[:14])
        for k in mine:
            if k["period"] == 0 and k["type"] in ("moneyline", "total") and not k.get("isAlternate"):
                print(" MKT", json.dumps({x: k.get(x) for x in ("type", "key", "status", "prices")}, ensure_ascii=False)[:420])
