"""Lab 16: fictional training data; standard library only."""

import csv
from datetime import date
from io import StringIO

# Editable inputs. Row numbers identify source rows, not data fields for deduping.
DECISION_DATE = "2026-04-15"
TABLE = """row,ticker,month,published,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def read_rows(table):
    rows = []
    for record in csv.DictReader(StringIO(table)):
        rows.append(dict(row=int(record["row"]), ticker=record["ticker"].strip(),
                         month=date.fromisoformat(record["month"] + "-01"),
                         published=date.fromisoformat(record["published"]),
                         index=float(record["index"])))
    return rows


def latest_vintages(rows):
    """Rule 4: caller supplies only publications eligible for its panel."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published"] > latest[key]["published"]:
            latest[key] = row
    kept = sorted(latest.values(), key=lambda row: row["row"])
    kept_ids = {row["row"] for row in kept}
    removed = [row for row in rows if row["row"] not in kept_ids]
    return kept, removed


def filter_rows(rows, decision_date):
    funnel = []
    valid = [row for row in rows if row["ticker"]]
    funnel.append(("Quarantined: no ticker", [r for r in rows if not r["ticker"]]))

    seen = set()
    clean, duplicates = [], []
    for row in valid:
        key = (row["ticker"], row["month"], row["published"], row["index"])
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)
            clean.append(row)
    funnel.append(("Exact duplicate", duplicates))

    eligible = [r for r in clean if r["published"] <= decision_date]
    funnel.append(("Published after decision date",
                   [r for r in clean if r["published"] > decision_date]))
    panel, replaced = latest_vintages(eligible)
    funnel.append(("Older vintage replaced by a revision", replaced))
    naive, _ = latest_vintages(clean)
    return panel, naive, funnel


def signals(panel):
    result = {}
    for ticker in sorted({row["ticker"] for row in panel}):
        history = sorted((r for r in panel if r["ticker"] == ticker),
                         key=lambda r: r["month"])
        latest = history[-1]
        # Require the immediately preceding calendar month, not a stale observation.
        previous_month = (latest["month"].replace(year=latest["month"].year - 1, month=12)
                          if latest["month"].month == 1 else
                          latest["month"].replace(month=latest["month"].month - 1))
        previous = next((r for r in history if r["month"] == previous_month), None)
        change = None if previous is None or previous["index"] == 0 else (
            latest["index"] / previous["index"] - 1) * 100
        result[ticker] = (latest["month"], change)
    return result


def main():
    decision = date.fromisoformat(DECISION_DATE)
    panel, naive, funnel = filter_rows(read_rows(TABLE), decision)
    print(f"Decision date: {decision}\n\nRow funnel")
    for label, removed in funnel:
        numbers = ", ".join(str(r["row"]) for r in removed) or "none"
        print(f"{label}: {len(removed)} removed; rows {numbers}")
    print(f"As-of panel: {len(panel)} rows\n")
    print("Row  Ticker  Month    Published   Index")
    for r in panel:
        print(f'{r["row"]:>3}  {r["ticker"]:<6}  {r["month"]:%Y-%m}  '
              f'{r["published"]}  {r["index"]:.1f}')
    for label, data in (("As-of", panel), ("Naive (ignores publication cutoff)", naive)):
        print(f"\n{label} signals")
        for ticker, (month, change) in signals(data).items():
            value = "unavailable (missing previous month or zero base)" if change is None else f"{change:+.2f}%"
            print(f"{ticker}: {value} ({month:%B %Y})")


if __name__ == "__main__":
    main()
