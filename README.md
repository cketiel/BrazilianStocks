# 🟢 BrazilianStocks

BrazilianStocks is a Python-based data analysis project that retrieves, processes, and stores financial information about **Brazilian stock market assets** (mainly FII and B3 stocks) using the [Alpha Vantage API](https://www.alphavantage.co/).

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

* The **free plan** of AlphaVantage allows **5 API calls per minute**. And only 25 requests per day.
  The script automatically includes delays to respect this limit.
* Keep your `api_key.py` **private** and excluded from version control.
* JSON and CSV outputs are **automatically organized** in folders.

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
