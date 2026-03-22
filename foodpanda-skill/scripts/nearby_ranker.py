#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nearby restaurant ranker.
Input: JSON string
Output: ranked candidates with weighted score
"""

import json
import math
import sys


def norm(value, min_v, max_v):
    if max_v <= min_v:
        return 1.0
    return (value - min_v) / (max_v - min_v)


def score_candidates(candidates):
    ratings = [c.get("rating", 0) for c in candidates]
    reviews = [c.get("reviews", 0) for c in candidates]
    dists = [c.get("distance_km", 99) for c in candidates]

    r_min, r_max = min(ratings), max(ratings)
    v_min, v_max = min(reviews), max(reviews)
    d_min, d_max = min(dists), max(dists)

    out = []
    for c in candidates:
        r = norm(c.get("rating", 0), r_min, r_max)
        v = norm(math.log1p(c.get("reviews", 0)), math.log1p(v_min), math.log1p(v_max))
        d = 1 - norm(c.get("distance_km", 99), d_min, d_max)  # closer is better
        o = 1.0 if c.get("open", False) else 0.0

        total = r * 0.40 + v * 0.30 + d * 0.20 + o * 0.10

        # Normalize output schema so the UI/assistant can always show key fields
        row = {
            "name": c.get("name", "未命名店家"),
            "rating": c.get("rating", 0),
            "reviews": c.get("reviews", 0),
            "distance_km": c.get("distance_km"),
            "open": bool(c.get("open", False)),
            "eta_min": c.get("eta_min"),
            "price_level": c.get("price_level", "未知"),
            "signature_dishes": c.get("signature_dishes", []),
            "estimated_per_person": c.get("estimated_per_person") if c.get("estimated_per_person") is not None else "未知", 
            "reservation_phone": c.get("reservation_phone") or c.get("phone") or "未提供",
            "foodpanda_delivery": c.get("foodpanda_delivery", "未知"),
            "restaurant_url": c.get("restaurant_url") or c.get("website") or "未提供",
            "maps_url": c.get("maps_url") or "未提供",
            "address": c.get("address") or "未提供",
            "nearby_parking": c.get("nearby_parking", []),
            "platform": c.get("platform", "unknown"),
        }
        # keep any extra fields from caller
        for k, val in c.items():
            if k not in row:
                row[k] = val

        row["score"] = round(total, 4)
        out.append(row)

    out.sort(key=lambda x: x["score"], reverse=True)
    return out


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "missing JSON input"}, ensure_ascii=False))
        sys.exit(1)

    payload = json.loads(sys.argv[1])
    candidates = payload.get("candidates", [])
    if not candidates:
        print(json.dumps({"error": "no candidates"}, ensure_ascii=False))
        sys.exit(1)

    ranked = score_candidates(candidates)
    result = {
        "location": payload.get("location"),
        "cuisine": payload.get("cuisine"),
        "budget_per_person": payload.get("budget_per_person"),
        "people": payload.get("people", 1),
        "ranked": ranked,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
