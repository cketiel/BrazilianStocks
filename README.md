# 🟢 BrazilianStocks

**BrazilianStocks** is a Python-based data analysis project designed to retrieve, process, and store financial information about **Brazilian stock market assets** — mainly *Fundos Imobiliários (FII)* and *B3-listed stocks* — using the [Alpha Vantage API](https://www.alphavantage.co/documentation/).

---

## 🚀 Features

* ✅ Bulk download of Brazilian stock data (`.SAO` symbols)
* ✅ Automated generation of group-based CSV files
* ✅ Smart delay handling to comply with AlphaVantage’s free API limits (5 requests/minute)
* ✅ JSON export for historical data
* ✅ Modular and extensible code structure

---

## 🧠 Project Structure

```
BrazilianStocks/
│
├── api_key.py             # Contains your private API key (excluded from Git)
├── history_to_json.py     # Downloads historical data (daily or weekly)
├── list_ticket_group.py   # Generates CSVs from .txt group files
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

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, create one manually:

```bash
pip install requests pandas
pip freeze > requirements.txt
```

### 4️⃣ Add your API key

Create a file named `api_key.py` (excluded from Git) and include:

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

---

### Additional Analysis Examples

* **Example 3:** Generate a unified ticket list
* **Example 4:** Generate historical analysis
* **Example 5:** Calculate monthly dividend analysis (`dividend = dividend_amount * cant`)
* **Example 6:** Compute trading balance (`trading = profit - total_dividend`)
* **Example 7:** Track historical total balance (`profit = final_balance - initial_balance`)

---

## 📊 Example Output

**Example of `list_1_3.csv`:**

| symbol    | open  | high  | low   | price | volume  | latestDay  | previousClose | change | changePercent |
| --------- | ----- | ----- | ----- | ----- | ------- | ---------- | ------------- | ------ | ------------- |
| ABEV3.SAO | 13.45 | 13.58 | 13.21 | 13.40 | 4567800 | 2025-10-23 | 13.50         | -0.10  | -0.74%        |
| BBAS3.SAO | 49.20 | 49.85 | 48.95 | 49.40 | 2789400 | 2025-10-23 | 49.10         | +0.30  | +0.61%        |

---

## ⚠️ Notes

* The API’s **free plan** allows 5 API calls per minute and 25 per day.
  The script includes automatic delays to respect this limit.
* Keep your `api_key.py` **private**.
* JSON and CSV outputs are **automatically organized** into folders.

---

## 💼 Estrategia y Uso Práctico

### 🧠 Idea Genial

In the Brazilian market, many **Fundos Imobiliários (FIIs)** and **stocks** pay **monthly dividends (proventos)**. Each asset distributes on a different date, and to receive the dividend, you must hold the asset for at least **8 days** before its *ex-dividend date*.

The **brilliant idea** behind this system is to **rotate capital** between assets with different payment dates — effectively earning **two or more dividends with the same capital** in one month.

**Example workflow:**

1. Hold **Stock A** until it pays its dividend, receive payment, and sell it.
2. Immediately reinvest into **Stock B**, which pays later in the same month.

If the difference between their payment dates is at least 10 days, the investor earns **two sets of proventos** with the same money.

Average dividend yields in Brazil hover around **1% per month**. Using this rotation logic, monthly returns can **double** to approximately **2%**, without adding new capital.

---

#### 🔢 Key Formulas

| Symbol    | Description             |
| :-------- | :---------------------- |
| **pc**    | Purchase price          |
| **pv**    | Selling price           |
| **g**     | Profit per share        |
| **cant**  | Number of shares        |
| **net**   | Net profit = g × cant   |
| **total** | Total value = cant × pv |

The **profit condition** is:

```
p₁ + p₂ > d₁ + a₂ + c₁ + c₂
```

Where:

* **p₁**, **p₂** = dividends from stocks 1 and 2
* **d₁** = drop after Stock 1 payment (if pv₁ < pc₁)
* **a₂** = price increase before buying Stock 2
* **c₁**, **c₂** = commissions for selling and buying

---

### 💰 Commissions and Optimization

Analyze whether commissions (**c₁**, **c₂**) are fixed or vary by broker.
Using **limit orders** instead of market orders can lower costs.
Weekly **rebalancing** via automation (e.g., *grid trading bots* or **Aladdin by BlackRock-inspired algorithms**) ensures disciplined execution.

---

### 📈 Portfolio Strategy Overview

Divide assets into **four groups** based on payment timing:

| Group  | Approx. Date | Description         |
| :----- | :----------- | :------------------ |
| **S1** | Day 30       | End-of-month payers |
| **S2** | Day 7        | Early-month payers  |
| **S3** | Day 12       | Mid-month payers    |
| **S4** | Day 17       | Third-week payers   |

💡 **Tip:** Always re-buy quality stocks when they drop below your average cost.

---

### 🧭 Plan General

The **general plan** maintains a weekly reinvestment cycle ensuring continuous income and growth.
Each week, one group generates proventos while another is purchased for the next payout window.

#### 🔁 Core Principles

1. **Weekly Rebalancing** — Review which assets to sell and buy weekly.
2. **Continuous Reinvestment** — Reinvest dividends into the next group immediately.
3. **Buy the Dip** — Re-acquire good assets below average cost.
4. **Automate When Possible** — Use bots or scripts for data-driven rotation.

#### 🧮 Reinvestment Windows

| Group  | Last Buy Date | Dividend Period | Objective          |
| :----- | :------------ | :-------------- | :----------------- |
| **S1** | Day 30        | End of month    | Start of rotation  |
| **S2** | Day 7         | Early month     | Early reinvestment |
| **S3** | Day 12        | Mid-month       | Growth phase       |
| **S4** | Day 17        | Third week      | Cycle completion   |

**Minimum capital per group:** 1,000 BRL.

---

### 🔗 Combinaciones Estratégicas

While each group operates independently, combining them creates **optimized capital flow** and **continuous reinvestment**.

#### ⚖️ Combination 1 — S1–S3

Balances end-of-month and mid-month cycles.
🟢 Stable income, 2x capital use per month.
🔹 Best for moderate-risk investors.

#### 🔁 Combination 2 — S2–S4

Bridges early-month and third-week payers.
🟢 Earn twice monthly, ~10-day gap between cycles.
🔹 Best for active dividend rotators.

#### 🧠 Combination 3 — S1–S2–S4

Three-stage reinvestment cycle (Day 30 → Day 7 → Day 17).
🟢 Near-continuous compounding with 3 payouts per month.
🔹 Best for advanced or automated strategies.

#### 📊 Comparative Overview

| Combination  | Avg. Monthly Rotations | Expected Yield Gain | Risk        |
| :----------- | :--------------------- | :------------------ | :---------- |
| **S1–S3**    | 2x                     | +80–100%            | Low         |
| **S2–S4**    | 2x                     | +100–120%           | Medium      |
| **S1–S2–S4** | 3x                     | +150–180%           | Medium–High |

---

## 🧩 Future Enhancements

* Add database persistence (SQLite or PostgreSQL)
* Integrate task scheduling (`cron`, Task Scheduler)
* Build dashboards (Plotly, Matplotlib)
* Add CLI export options (Excel, Parquet)
* Implement bot-based alerts and analytics
* Create desktop/web/mobile apps using the analytical core

---

## 📜 License

No license has been defined yet.
You can add one later by creating a `LICENSE` file (MIT, Apache 2.0, etc.).

---

## 👨‍💻 Author

**Roger Rodriguez Navarro**
GitHub: [@cketiel](https://github.com/cketiel)
Project: [BrazilianStocks](https://github.com/cketiel/BrazilianStocks)
