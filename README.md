# 🟢 BrazilianStocks

BrazilianStocks is a Python-based data analysis project that retrieves, processes, and stores financial information about **Brazilian stock market assets** (mainly FII and B3 stocks) using the [Alpha Vantage API](https://www.alphavantage.co/). [https://www.alphavantage.co/documentation/]

The project can:

* Download **daily** and **weekly** stock price histories.
* Generate **CSV** and **JSON** data files for multiple stock groups.
* Manage requests efficiently with **rate-limiting** and **error retrying**.
* Produce a **master dataset** combining all stocks for further analysis.

---

## 🚀 Features

* ✅ Bulk download of Brazilian stock data (`.SAO` symbols)
* ✅ Automated generation of group-based CSV files
* ✅ Smart delay handling to comply with AlphaVantage’s free API limits (5 requests/minute)
* ✅ JSON export for historical data
* ✅ Modular structure for easy expansion and automation

---

## 🧠 Project Structure

```
BrazilianStocks/
│
├── api_key.py             # Contains your private API key (excluded from Git)
├── history_to_json.py     # Downloads historical data (daily or weekly)
├── main.py                # Downloads current prices for multiple groups
├── csv/                   # Generated CSV files are saved here
├── json/                  # JSON output directory for historical data
├── ticket_group/          # Contains .txt files listing stock groups
├── .gitignore             # Excludes sensitive or unnecessary files
└── README.md              # You’re reading it :)
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cketiel/BrazilianStocks.git
cd BrazilianStocks
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv env1
env1\Scripts\activate    # On Windows
```

### 3️⃣ Install required dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, create one manually with:

```bash
pip install requests pandas
pip freeze > requirements.txt
```

### 4️⃣ Add your API key

Create a file called `api_key.py` (this file should **not** be uploaded to GitHub) and add:

```python
key = "your_alphavantage_api_key_here"
```

---

## ▶️ Usage

### Example 1: Generate JSON data (daily or weekly)

```bash
python history_to_json.py --t NCRA11 --f d
```

This creates a file like `json/NCRA11_d.json`.

### Example 2: Generate CSVs for multiple stock groups

* Add `.txt` files inside the `ticket_group/` folder (e.g., `1_3.txt`, `2_4.txt`, `random.txt`).
* Each `.txt` file should list one symbol per line.
* Run the script:

```bash
python list_ticket_group.py
```

The output CSVs will be saved in the `csv/` folder as:

```
list_1_3.csv
list_2_4.csv
list_random.csv
master_list.csv
```
### Example 3: Generate Ticket List
### Example 4: Generate historical analysis
### Example 5: Generate dividend analysis (monthly earnings) (dividend = dividend_amount * cant)
### Example 6: Generate trading balance (trading = ganancia - total_dividend)
### Example 7: Generate historical total balance (ganancia = saldo_final - initial_balance)
  
---

## 📊 Example Output

**Example of `list_1_3.csv`:**

| symbol    | open  | high  | low   | price | volume  | latestDay  | previousClose | change | changePercent |
| --------- | ----- | ----- | ----- | ----- | ------- | ---------- | ------------- | ------ | ------------- |
| ABEV3.SAO | 13.45 | 13.58 | 13.21 | 13.40 | 4567800 | 2025-10-23 | 13.50         | -0.10  | -0.74%        |
| BBAS3.SAO | 49.20 | 49.85 | 48.95 | 49.40 | 2789400 | 2025-10-23 | 49.10         | +0.30  | +0.61%        |

---

## ⚠️ Notes
* The API has a free plan and a paid plan.
* The **free plan** of AlphaVantage allows **5 API calls per minute**. And only 25 requests per day, and you can't use features labeled "Premium"
  The script automatically includes delays to respect this limit.
* Keep your `api_key.py` **private** and excluded from version control.
* JSON and CSV outputs are **automatically organized** in folders.

---
## 🧠 Idea Genial

In the Brazilian stock market, there are several *fundos imobiliários* and stocks that pay **monthly dividends (proventos)**. This regular income stream encourages investors to hold such assets, as each company or fund distributes its dividends on different dates during the month.

However, to qualify for these payments, investors must meet the **minimum holding period**, usually around **8 days** before the ex-dividend date. This means you must own the shares for at least that period to receive the monthly payout.

### 💡 The Core Idea

The “brilliant idea” behind this strategy is to **use timing between different dividend-paying assets** to double the potential monthly return using the *same capital*.

For instance, if one stock pays dividends early in the month and another pays later (with a gap of at least 10 days), an investor could:

1. Hold **Stock A** until its payout date, receive its dividend, and then sell it.
2. Immediately reinvest the proceeds into **Stock B**, which has not yet reached its payout date.

Since both pay in different parts of the month, the same amount of capital generates **two dividend incomes** in the same period.
In other words, your effective return becomes the **sum of both proventos**, while still working within the time restrictions of each asset.

On average, monthly proventos yield around **1%** of the stock’s price. With this strategy, that return could be **doubled** — achieving roughly **2% monthly** — by smartly rotating between two or more assets.

---

### ⚙️ Supporting Definitions & Formulas

Let’s define key variables used in this logic:

| Symbol    | Description                        |
| :-------- | :--------------------------------- |
| **pc**    | Purchase price                     |
| **pv**    | Selling price                      |
| **g**     | Profit per share                   |
| **cant**  | Number of shares                   |
| **net**   | Net profit = (g × cant)            |
| **total** | Total value after sale = cant × pv |

The fundamental condition to maintain profitability is:

[
p_1 + p_2 > d_1 + a_2 + c_1 + c_2
]

Where:

* **p₁** = dividend (provento) from Stock 1
* **p₂** = dividend (provento) from Stock 2
* **d₁** = price drop after Stock 1 payout
* **a₂** = price increase before buying Stock 2
* **c₁, c₂** = transaction costs (sell and buy commissions)

**Simplified conditions:**

* ( d₁ = pc₁ - pv₁ ), but if ( pv₁ > pc₁ ) then ( d₁ = 0 )
* ( a₂ = pv₂ - pc₂ ), but initially ( a₂ = 0 ) since Stock 2 hasn’t been sold yet

---

### 💰 Commissions and Optimization

Investigate **whether c₁ and c₂ are fixed or variable**, depending on the broker or trading platform.
Some brokers charge differently for limit orders versus market orders. Choosing the right broker can optimize profitability.

It’s advisable to **rebalance weekly** using smart trading automation (such as a *grid trading bot* or strategies similar to **Aladdin by BlackRock**) to manage buy/sell timing intelligently.

---

### 📈 Portfolio Strategy Overview

To sustain continuous reinvestment, the assets are divided into **four groups** based on their dividend payment dates:

| Group  | Payment Window | Investment Goal        |
| :----- | :------------- | :--------------------- |
| **S1** | Around day 30  | Can buy until the 30th |
| **S2** | Around day 7   | Can buy until the 7th  |
| **S3** | Around day 12  | Can buy until the 12th |
| **S4** | Around day 17  | Can buy until the 17th |

This structure allows receiving **weekly proventos**, enabling consistent reinvestment and compounding returns.
Ideally, allocate **at least 1,000 BRL** per group to maintain balance.

**Key rule:**

> Always re-buy “good” stocks when their price drops below your average cost — that’s when they’re “in the red”.

---

### 🧩 Example Trading Plan

**S1 (End of month)**

* Sell: `LIFE11`, `RURA`, `CACR11`
* Buy: `VGIA11`, `VGIR11`, `NAVT11`, `DCRA11`

**S2 (Early month)**

* Sell: `DCRA11`, `AGRX11`, `RZAG11`, `XPCA11`
* Buy: `NCRA11`

**S3 (Mid-month)**

* Sell: `VGIA11`, `VGIR11`, `NAVT11`
* Buy: `CACR11`

**S4 (Third week)**

* Sell: `NCRA11`
* Buy: `AGRX11`, `RZAG11`, `XPCA11`, `LIFE11`, `RURA`

---

### 📊 Practical Benefits

* Weekly dividend inflows and reinvestment.
* Dual provento earnings with the same capital.
* Portfolio diversification by timing rather than by sector.
* Smart rebalancing using data-driven signals.

This approach transforms passive income investing into a **dynamic rotation strategy**, aiming for **consistent monthly compounding** with minimal idle capital.

## 🧭 Plan General

The **general plan** of this strategy is to maintain an active yet structured investment cycle that allows continuous income, reinvestment, and growth — all based on the timing of dividend payments from different asset groups.

The portfolio is strategically divided into **four groups (S1, S2, S3, S4)** according to their *dividend payment dates*.
This ensures that every week of the month there is at least one group generating proventos, creating a **weekly income flow**.

---

### 🔁 Core Principles

1. **Weekly Rebalancing**
   Every week, the portfolio is reviewed to decide which assets to sell and which to buy based on:

   * Dividend payment schedules.
   * Price movements and market conditions.
   * Profit-taking or re-entry opportunities.

2. **Reinvesting Smartly**
   Dividends and sale proceeds are immediately reinvested into the next eligible group (e.g., selling from S1 → buying in S2).
   This keeps capital working continuously without idle periods.

3. **Re-buying Good Stocks**
   Always re-purchase **high-quality assets** when their price drops below the average purchase cost (when they are “in the red”).
   This increases position size at a discount, lowering the average cost and improving long-term yield potential.

4. **Automated Rebalancing**
   Whenever possible, use **automation tools** such as a *grid trading bot* or intelligent allocation algorithms inspired by **Aladdin by BlackRock**.
   These tools help optimize buy/sell timing and rebalance the portfolio with data-driven precision.

---

### 🧮 Investment Logic

Each group has a **specific reinvestment window**, defined by the date before its dividend payment.

| Group  | Latest Buy Date | Dividend Frequency | Main Objective         |
| :----- | :-------------- | :----------------- | :--------------------- |
| **S1** | Day 30          | End of month       | Prepare for next cycle |
| **S2** | Day 7           | Early month        | Capture early payers   |
| **S3** | Day 12          | Mid-month          | Mid-cycle accumulation |
| **S4** | Day 17          | Third week         | Complete the cycle     |

To ensure consistent returns, keep **a minimum of 1,000 BRL per group**.
This balance allows steady reinvestment and sufficient liquidity to take advantage of short-term opportunities.

---

### 📊 Trading and Execution Strategy

* Maintain three main **rotation sets**:

  * Group **(1-2-4)**: Focused on assets with overlapping payment gaps of ~10 days.
  * Group **(1-3)**: Balances monthly cycles with alternating weeks.
  * Group **(2-4)**: Provides mid-month reinforcement for compound growth.

* **Example flow:**

  * Week 1 → Sell S1, Buy S2
  * Week 2 → Sell S2, Buy S3
  * Week 3 → Sell S3, Buy S4
  * Week 4 → Sell S4, Buy S1

This rotation ensures that capital is constantly moving toward the next profitable window.

---

### 🤖 Automation and Risk Control

* Implement a **grid trading bot** or rule-based script that automates:

  * Sell signals when dividends are paid.
  * Buy signals based on price thresholds and group timing.
  * Weekly rebalancing decisions using live market data.

* Introduce **smart safeguards** such as:

  * Minimum holding days (≥8 days).
  * Stop-loss rules for excessive price drops.
  * Profit-locking triggers to preserve gains.

---

### 🎯 Strategic Goals

* Achieve **weekly dividend income** using time-based diversification.
* Double monthly returns by compounding multiple proventos with the same capital.
* Maintain low idle cash and high reinvestment efficiency.
* Build a semi-automated, intelligent trading system inspired by professional asset management frameworks.

---

This plan sets the foundation for a **sustainable dividend rotation model**, where capital efficiency and timing precision replace speculation.
It’s not about chasing price movements — it’s about **orchestrating consistent cash flow** through disciplined rebalancing.

## 🔗 Combinaciones Estratégicas

While each group (S1, S2, S3, S4) is designed to operate independently based on its dividend schedule, the true optimization of this system emerges when **strategic combinations** between groups are executed.
These combinations allow for **smoother capital rotation**, **continuous reinvestment**, and **optimized yield compounding** throughout the month.

---

### ⚖️ Combination 1 — **S1–S3**

* **Objective:** Balance end-of-month and mid-month payers to maintain cash flow stability.
* **Mechanism:**

  * Sell assets from **S1** right after their dividend payout (around day 30).
  * Immediately reinvest into **S3**, which typically pays mid-month (around day 12).
* **Benefit:** Capital is reused twice per month — once at the end, once mid-month — ensuring nearly no idle periods.
* **Ideal for:** Medium-risk investors seeking stable, recurring reinvestment cycles.

---

### 🔁 Combination 2 — **S2–S4**

* **Objective:** Create a reinvestment bridge between early-month and third-week payers.
* **Mechanism:**

  * Sell **S2** holdings after early-month payouts (around day 7).
  * Use those proceeds to buy **S4**, which typically pays around day 17.
* **Benefit:** Captures proventos twice per month, roughly every 10 days apart — aligning perfectly with the 8-day minimum holding requirement.
* **Ideal for:** Aggressive dividend rotators aiming for biweekly yield acceleration.

---

### 🧠 Combination 3 — **S1–S2–S4**

* **Objective:** Execute a **three-stage reinvestment cycle** to maintain near-continuous capital flow.
* **Mechanism:**

  1. **Start with S1:** Receive dividends and sell around day 30.
  2. **Reinvest into S2:** Hold and collect around day 7.
  3. **Reinvest again into S4:** Capture third-week payments around day 17.
* **Benefit:** This is the most efficient rotation, achieving **three dividend payouts within one month** using the same capital.
  It effectively creates a “dividend grid” where every week capital is active and compounding.
* **Ideal for:** Advanced investors or automated trading bots applying **grid trading logic** for maximum yield optimization.

---

### ⚙️ Strategic Integration

These combinations can be **manually managed** or **automated** through scripts or bots that:

* Track each group’s expected payment dates.
* Trigger sell/buy operations according to the defined calendar.
* Optimize transaction timing and reduce commission overlap.

The **grid-based approach** also allows adaptive scaling — if one group underperforms, its capital can be reallocated dynamically to another combination that maintains positive yield momentum.

---

### 📈 Outcome

| Combination  | Avg. Monthly Rotations | Expected Yield Gain     | Risk Level  |
| :----------- | :--------------------- | :---------------------- | :---------- |
| **S1–S3**    | 2x                     | +80–100% of base yield  | Low         |
| **S2–S4**    | 2x                     | +100–120% of base yield | Medium      |
| **S1–S2–S4** | 3x                     | +150–180% of base yield | Medium–High |

The ultimate goal is to **synchronize dividend cycles** to extract maximum efficiency from the same capital, transforming temporal diversification into a source of **compound growth and stable income**.

---

By mastering these combinations, investors can operate a **continuous dividend loop**, where money never rests — it flows, earns, and reinvests, just like a professional portfolio managed by an intelligent algorithm.

---

## 🧩 Future Enhancements

* Add database persistence (SQLite or PostgreSQL)
* Integrate scheduling with `cron` or `Task Scheduler`
* Create visualization dashboards with `Plotly` or `Matplotlib`
* Add command-line flags to export Excel or Parquet files
* Add Bots for data visualization, notification and alert agents
* Add Customized applications (desktop, web and/or app for Android/IO mobiles) to obtain maximum profits, making use of these analyzes and applying group strategies

---

## 📜 License

No license has been defined yet.
You can add one later by creating a file named `LICENSE` (MIT, Apache 2.0, etc.).

---

## 👨‍💻 Author

**Roger Rodriguez Navarro**
GitHub: [@cketiel](https://github.com/cketiel)
Project: [BrazilianStocks](https://github.com/cketiel/BrazilianStocks)
