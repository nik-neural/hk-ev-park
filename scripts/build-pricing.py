#!/usr/bin/env python3
"""Build data/pricing.json from data.gov.hk carpark API."""

import json
import re
import ssl
import urllib.request
from pathlib import Path

API = (
    "https://api.data.gov.hk/v1/carpark-info-vacancy"
    "?data=info&vehicleTypes=privateCar&lang=zh_TW"
)
OUT = Path(__file__).resolve().parent.parent / "data" / "pricing.json"


def clean_remark(rm: str) -> str:
    if not rm:
        return ""
    t = re.sub(r"<br\s*/?>", "\n", rm, flags=re.I)
    t = t.replace("&nbsp;", " ")
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"高度限制[:：]?\s*", "", t, flags=re.I)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def parse_ev(text: str):
    if not re.search(r"kWh|kwh|度電|充電", text, re.I):
        return None, None
    prices = [float(m.group(1)) for m in re.finditer(r"([\d.]+)\s*/?\s*kWh", text, re.I)]
    detail = re.sub(r"HKD\$?", "$", text, flags=re.I).replace(",", "，").strip()
    return detail[:240], (min(prices) if prices else None)


def hourly_values(text: str):
    vals = []
    for pat in [
        r"\$\s*([\d.]+)\s*/\s*小時",
        r"\$\s*([\d.]+)\s*每小時",
        r"每小時\s*\$\s*([\d.]+)",
        r"([\d.]+)\s*港幣\s*/\s*小時",
        r"每小時\s*([\d.]+)\s*元",
        r"每小時收費港幣\s*([\d.]+)\s*元",
    ]:
        vals.extend(float(m.group(1)) for m in re.finditer(pat, text))
    return vals


def price_lines(text: str):
    lines = []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^\d+(\.\d+)?\s*米", line):
            continue
        if re.search(r"[\$港幣]|[\d.]+\s*元", line):
            lines.append(line)
    return lines


def extract_record(r: dict):
    pc = r.get("privateCar") or {}
    park_hourly = next(
        (h["price"] for h in pc.get("hourlyCharges") or [] if h.get("price") is not None),
        None,
    )
    park_detail = None
    ev_detail = ev_min = None

    for h in pc.get("hourlyCharges") or []:
        rm = (h.get("remark") or "").strip()
        if re.search(r"kWh|kwh|度電|充電", rm, re.I):
            ev_detail, ev_min = parse_ev(clean_remark(rm))
            break

    remark = clean_remark(
        "\n".join((h.get("remark") or "") for h in r.get("heightLimits") or [])
    )
    if remark:
        if not ev_detail and re.search(r"kWh|kwh|度電|充電", remark, re.I):
            ev_detail, ev_min = parse_ev(remark)

        if park_hourly is None:
            half = re.search(
                r"(?:每)?半小時\s*\$\s*([\d.]+)|\$\s*([\d.]+)\s*/\s*半小時", remark
            )
            if half:
                price = float(half.group(1) or half.group(2))
                park_detail = f"${price:g}/半小時"
            else:
                vals = hourly_values(remark)
                if len(vals) == 1:
                    park_hourly = vals[0]
                elif vals:
                    uniq = []
                    for v in vals:
                        if v not in uniq:
                            uniq.append(v)
                    if len(uniq) == 1:
                        park_hourly = uniq[0]

        if park_hourly is None and park_detail is None:
            lines = price_lines(remark)
            if lines:
                park_detail = "；".join(lines[:3])
                if len(lines) > 3:
                    park_detail += "…"

    if park_hourly is not None:
        park_detail = None

    if park_hourly is None and park_detail is None and ev_detail is None:
        return None

    out = {}
    if park_hourly is not None:
        out["h"] = park_hourly
    if park_detail:
        out["d"] = park_detail
    if ev_detail:
        out["ev"] = ev_detail
    if ev_min is not None:
        out["em"] = ev_min
    return out


def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(API, context=ctx) as resp:
        results = json.load(resp)["results"]

    lookup = {}
    for r in results:
        entry = extract_record(r)
        if entry:
            lookup[r["park_Id"]] = entry

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(lookup, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(lookup)} / {len(results)} records → {OUT}")


if __name__ == "__main__":
    main()