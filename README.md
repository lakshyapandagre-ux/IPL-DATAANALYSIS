# IPL Data Analysis & Visualization 🏏

This project is a complete Exploratory Data Analysis (EDA) and Visualization project based on IPL (Indian Premier League) ball-by-ball data.

As a 2nd-year B.Tech CSIT student learning Data Science, I built this project to improve my skills in:
*   **Python Programming**
*   **Pandas & NumPy** for data cleaning and manipulation
*   **Data Visualization** (Matplotlib & Seaborn)
*   **Exploratory Data Analysis (EDA) & Statistics**

The project focuses on understanding IPL trends, player performances, team statistics, venue analysis, and match insights using real IPL data from **2008 to 2026**!

---

## 📌 Project Objectives

The main goals of this project were:
*   Practice real-world data analysis on a large dataset
*   Work with large datasets (over 283,000 deliveries!)
*   Improve visualization skills to build neat, readable charts
*   Learn the basics of cricket analytics
*   Build a strong portfolio project for GitHub and summer internship applications

---

## 📂 Dataset Information

The dataset contains:
*   Ball-by-ball IPL data
*   Match details (season, city, venue, toss)
*   Batter and bowler statistics
*   Dismissal types and wickets
*   Team performance data
*   Match results

### Dataset Size
*   **Rows**: ~283,000+
*   **Columns**: 65

---

## 🛠 Technologies Used

*   **Python**
*   **Pandas** & **NumPy**
*   **Matplotlib** & **Seaborn**
*   **Plotly** (for interactive matchups)
*   **Jupyter Notebook**

---

## 📁 Project Structure

```bash
IPL-Data-Analysis/
│
├── data/
│   └── IPL.csv                      # Main ball-by-ball CSV data (110MB)
│
├── notebooks/
│   └── IPL_Analysis.ipynb           # Main exploratory Jupyter Notebook
│
├── images/                          # Exported high-resolution charts
│   ├── top_10_run_scorers.png
│   ├── highest_strike_rates.png
│   ├── batting_phase_analysis.png
│   └── ... (19 charts in total)
│
├── src/                             # Automated python utility scripts
│   ├── generate_notebook.py
│   └── execute_notebook.py
│
├── README.md                        # Documentation
├── requirements.txt                 # Dependencies
└── .gitignore
```

---

## 📊 Analysis Performed

### 🔹 Data Cleaning
*   Removed unnecessary columns (like index columns)
*   Checked and accounted for missing values in sparse columns (like `player_out` and `wicket_kind`)
*   Checked and removed duplicate rows
*   Standardised historical team names (Delhi Daredevils $\rightarrow$ Capitals, Kings XI Punjab $\rightarrow$ Punjab Kings, RCB $\rightarrow$ Bengaluru) so career stats stay contiguous
*   Cleaned up season formats (like `2007/08` $\rightarrow$ `2008`) for chronological plotting

### 🔹 Batting Analysis
*   Top 10 run-scorers in IPL history (Virat Kohli is leading!)
*   Best career batting strike rates (Min 1,000 balls faced, Andre Russell leads with 170+)
*   Most boundaries hit (Fours vs. Sixes)
*   Highest batting averages (calculated based on actual dismissals, led by KL Rahul & Kohli)
*   Most milestones (Fifties and Hundreds)
*   Batting performance across innings phases: **Powerplay** vs. **Middle** vs. **Death Overs**

### 🔹 Bowling Analysis
*   Top 10 highest wicket-takers (Spinners lead the middle overs!)
*   Best career bowling economy rates (Min 500 balls, Sunil Narine & Rashid Khan lead)
*   Dot ball percentage for bowlers (Dale Steyn & Malinga lead with over 40% dots)
*   Wicket distribution analysis (caught is the most common dismissal at 62.9%)

### 🔹 Team Analysis
*   Most successful teams in history (Mumbai Indians & Chennai Super Kings lead in wins)
*   Win percentage of teams (CSK leads with over 58%)
*   Toss win impact (winning the toss is a 50.6% coin flip; doesn't guarantee a win)
*   Chasing vs. defending outcomes (chasing teams win 54.5% of matches)

### 🔹 Venue Analysis
*   Highest scoring venues by average 1st innings score (Chinnaswamy & Wankhede average 175+)
*   Best chasing venues (highest chasing win percentages are over 60%)

### 🔹 Advanced Insights & Match Progression
*   Over-by-over scoring runs vs. wicket fall progression
*   Powerplay score ranges win probability correlation (scoring 65+ runs boosts win chance to 65%+)
*   Batter vs. Bowler face-to-face head-to-head matchup analyzer function

---

## 📈 Sample Visualizations

The Jupyter Notebook generates and exports **19 clean charts** into the `images/` directory:
*   **Bar Charts**: Career runs, strike rates, win percentages, boundaries
*   **Subplots**: Runs & wickets over-by-over, batting phases strike rate & average side-by-side
*   **Pie Charts**: Distribution of wicket kinds in IPL history
*   **Line Charts**: Wicket progression over the 20 overs

---

## 🎯 Key Learnings

Through building this project, I learned:
1.  **Working with Large Datasets**: How to efficiently read, group, and aggregate a 110MB dataset with Pandas.
2.  **Real-World Data Cleaning**: The absolute necessity of combining renamed teams and fixing season formats so our numbers are contiguous.
3.  **Cricket Analytics Concepts**: Calculating domain-correct cricket stats (e.g. strike rates excluding wides, averages off dismissals instead of matches).
4.  **Exploratory Data Analysis**: How to ask questions from raw data and answer them step-by-step using Python.

---

## 🚀 Future Improvements

In the future, I plan to:
*   Build an interactive IPL dashboard using Streamlit
*   Add Machine Learning models to predict matches in real-time
*   Create player rating systems based on recent seasons

---

## ▶️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/suyash-codez/IPL-Data-Analysis.git
cd IPL-Data-Analysis
```

### 2. Install Libraries
```bash
pip install -r requirements.txt
```

### 3. Run the Notebook
Open `notebooks/IPL_Analysis.ipynb` using Jupyter Notebook or VS Code. 

*(Note: The notebook is completely executed, so all data tables, printed matchup outputs, and Seaborn charts are already fully populated and visible right away!)*

---

## 👨‍💻 About Me

Hi! I am **Suyash**, a 2nd-year B.Tech CSIT student currently learning Data Science, Python programming, and basic Machine Learning. I am highly interested in exploring data stories and sports analytics!

This project is part of my learning journey in:
*   Data Analysis & Exploration
*   Visualization & Data Storytelling
*   Python Programming

---

## 📬 Connect With Me

*   **LinkedIn**: [suyash-codez](https://www.linkedin.com/in/suyash-codez)
*   **GitHub**: [suyash-codez](https://github.com/suyash-codez)
*   **Email**: suyashverma0023@gmail.com

⭐ *If you liked this project, feel free to give it a star!*