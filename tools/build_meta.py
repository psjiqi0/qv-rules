#!/usr/bin/env python3
"""扫 countries/*.json 生成仓库根目录 meta.json。

用法: python3 tools/build_meta.py
新增/更新国家包后跑一次本脚本，再连同 meta.json 一起提交。
meta.version 为时间戳整数（YYYYMMDDHHMM，UTC），单调递增即可，App 以它判新旧。
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"


def count_domains(pack: dict) -> int:
    n = len(pack.get("direct_domains", [])) + len(pack.get("direct_cidrs", []))
    for g in pack.get("groups", {}).values():
        n += len(g.get("direct", [])) + len(g.get("proxy", []))
    return n


def main() -> None:
    countries = {}
    for path in sorted(COUNTRIES_DIR.glob("*.json")):
        raw = path.read_bytes()
        pack = json.loads(raw.decode("utf-8"))
        cc = pack.get("country") or path.stem
        countries[cc] = {
            "file": f"countries/{path.name}",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "domains": count_domains(pack),
        }
    now = datetime.now(timezone.utc)
    meta = {
        "version": int(now.strftime("%Y%m%d%H%M")),
        "updated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "countries": countries,
    }
    out = ROOT / "meta.json"
    out.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"meta.json written: version={meta['version']} countries={list(countries)}")


if __name__ == "__main__":
    main()
