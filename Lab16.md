Lab 16.md

#On the day you would have traded, what did this data actually say — and how much of what you see now came later?
| Ticker | Knowable index | Monthly change |
|---|---:|---:|
| AAA | 103.0 | +1.98% |
| BBB | 97.0 | −1.02% |
| CCC | 111.0 | +0.91% |

Three rows came later: AAA’s March index of 109, BBB’s March index of 92, and CCC’s revised February index of 112.

Using those later publications produces the naive signals: +5.83%, −5.15%, and +1.82%, respectively. None of those signals was knowable on March 31.

#Ask your AI to quiz you on the line you understand least; answer before it explains.
#if key not in latest or row["published"] > latest[key]["published"]:

What are the two conditions being checked, and why should either one cause the code to save this row?

Answer: finding the latest publication date for each ticker

#What is look-ahead bias? 2. How does it work — event time, publication time, revision? 
Look-ahead bias happens when a backtest uses information that wasn’t available on the historical decision date. It gives the strategy hindsight.

- Event time: the period the number measures—for example, March spending.
- Publication time: when that number became available—for example, April 10.
- Revision date: when an updated value for an earlier period was published.



