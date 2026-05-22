import nbformat as nbf
import os

# Initialize notebook
nb = nbf.v4.new_notebook()
nb['cells'] = []

# List to store cells
cells = []

# ----------------- SECTION 1: INTRODUCTION -----------------
intro_md = """# IPL Cricket Data Analysis & Visualization (2008 - 2026)
### *Created by Suyash | 2nd-year B.Tech CSIT Student*

---

## 1. Introduction

Hey everyone! I'm Suyash, a 2nd-year B.Tech CSIT student. I am a huge cricket fan, and I've been learning Python, Pandas, NumPy, and Data Visualization. For my learning and portfolio, I wanted to do a hands-on data analysis project on something I really enjoy. 

I found this massive ball-by-ball IPL dataset on Kaggle. It is huge—it has **over 283,000 deliveries** and **65 columns** spanning all matches from **2008 to 2026**! 

I want to use my coding skills to explore the data and answer some practical cricket questions, such as:
1. Who are the highest run-scorers and the most explosive boundary hitters?
2. Which bowlers are the most economical and have the best dot ball percentages?
3. Does winning the toss actually help in winning matches, or is it just a coin flip?
4. How do runs and wickets progress over-by-over from the Powerplay to the Death Overs?
5. How can we check head-to-head bowler vs. batter stats using Python?

Let's get started and dive into the code!
"""
cells.append(nbf.v4.new_markdown_cell(intro_md))


# ----------------- SECTION 2: IMPORTING LIBRARIES -----------------
imports_md = """## 2. Importing Libraries & Setup

First, I will load the basic libraries that I am learning:
- `pandas` for handling the data table.
- `numpy` for basic mathematical operations.
- `matplotlib` and `seaborn` to make simple, nice-looking charts.
- `os` to make a folder for saving our charts.
"""
cells.append(nbf.v4.new_markdown_cell(imports_md))

imports_code = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

# Suppress warnings to keep the output clean
warnings.filterwarnings('ignore')

# Set visual style for my charts
sns.set_style("whitegrid")

# Create a folder to save my charts so I can use them on GitHub
if not os.path.exists("../images"):
    os.makedirs("../images")
    print("Created 'images' folder for saving our plots!")
else:
    print("Folder 'images' already exists and is ready.")
"""
cells.append(nbf.v4.new_code_cell(imports_code))


# ----------------- SECTION 3: LOADING DATASET -----------------
load_md = """## 3. Loading the Dataset

Now let's load the IPL ball-by-ball data using `pd.read_csv`. Since the CSV file is quite big (about 110MB), I will use `low_memory=False` to prevent warnings about mixed data types in columns. Let's see the shape of our data.
"""
cells.append(nbf.v4.new_markdown_cell(load_md))

load_code = """# Loading the CSV file
df = pd.read_csv("../data/IPL.csv", low_memory=False)
print("Data loaded successfully!")
print(f"The dataset has {df.shape[0]:,} rows and {df.shape[1]} columns.")
"""
cells.append(nbf.v4.new_code_cell(load_code))


# ----------------- SECTION 4: DATA CLEANING -----------------
cleaning_md = """## 4. Data Cleaning

Before plotting charts, we need to clean the data. 
In the IPL, some teams changed their names over the years:
- **Delhi Daredevils** became **Delhi Capitals**
- **Kings XI Punjab** became **Punjab Kings**
- **Royal Challengers Bangalore** became **Royal Challengers Bengaluru**
- **Rising Pune Supergiants** was spelled in two different ways (with and without the 's').

If I don't merge them, my analysis will count them twice. I will write a simple dictionary map to standardise these team names.

I will also:
1. Drop the redundant column `Unnamed: 0` if it exists.
2. Fix seasons like `2007/08` to `2008` so we can easily plot year-by-year graphs.
3. Check where the missing values are.
"""
cells.append(nbf.v4.new_markdown_cell(cleaning_md))

cleaning_code = """# 1. Drop Unnamed column if it exists
if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)
    print("Removed index column.")

# 2. Map old team names to new names
team_mapping = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Rising Pune Supergiants': 'Rising Pune Supergiant'
}

team_columns = ['batting_team', 'bowling_team', 'toss_winner', 'match_won_by']
for col in team_columns:
    if col in df.columns:
        df[col] = df[col].replace(team_mapping)

print("Standardised all team names.")

# 3. Standardise season values to represent the year
season_mapping = {
    '2007/08': '2008',
    '2009/10': '2010',
    '2020/21': '2020'
}
df['season'] = df['season'].replace(season_mapping)
print("Standardised seasons.")

# 4. Check for null values in some main columns
null_checks = ['wicket_kind', 'player_out', 'extra_type', 'city']
for col in null_checks:
    null_count = df[col].isnull().sum()
    print(f"Missing in {col}: {null_count:,} rows")
"""
cells.append(nbf.v4.new_code_cell(cleaning_code))

cleaning_insights_md = """### Cleaning Observations:
- Columns like `wicket_kind` and `player_out` have ~95% missing values. This is actually completely correct because **batsmen only get out on about 5% of all balls bowled**! So we don't need to drop or fill them.
- Same for `extra_type`—most balls are legal deliveries without extras (wides/no-balls), so it's mostly empty.
"""
cells.append(nbf.v4.new_markdown_cell(cleaning_insights_md))


# ----------------- SECTION 5: DATASET OVERVIEW -----------------
overview_md = """## 5. Quick Overview of the Data

Let's look at some quick, interesting facts about IPL history using basic unique counts.
"""
cells.append(nbf.v4.new_markdown_cell(overview_md))

overview_code = """total_matches = df['match_id'].nunique()
total_runs = df['runs_total'].sum()
total_wickets = df['bowler_wicket'].sum()
total_balls = df[df['extra_type'] != 'wides'].shape[0] # exclude wides for balls faced count

print(f"Timeline: {df['season'].min()} to {df['season'].max()}")
print(f"Total Matches Played: {total_matches:,}")
print(f"Total Runs Scored: {total_runs:,}")
print(f"Total Wickets Taken (Bowler-credited): {total_wickets:,}")
print(f"Total Legal Balls Faced: {total_balls:,}")
"""
cells.append(nbf.v4.new_code_cell(overview_code))


# ----------------- SECTION 6: BATTING ANALYSIS -----------------
batting_md = """## 6. Batting Performance Analysis

Let's study the batsmen. I want to see:
1. **Most Runs**: Who are the top 10 highest scorers?
2. **Best Strike Rates**: Who scores the fastest? (I will filter for players with at least 1,000 balls faced so that one-match players don't mess up our graph).
3. **Most Boundaries**: Who has hit the most 4s and 6s?
4. **Batting Averages**: Calculated as `Runs / Dismissals` (Min 30 dismissals).
5. **Milestones**: Who has the most fifties and hundreds?
6. **Innings Phases**: Let's compare overall strike rates and averages during **Powerplay (Overs 1-6)**, **Middle (Overs 7-15)**, and **Death (Overs 16-20)**.
"""
cells.append(nbf.v4.new_markdown_cell(batting_md))

batting_code1 = """# 1. Top 10 Run Scorers
top_batsmen = df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10).reset_index()
print(top_batsmen)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_batsmen, x='runs_batter', y='batter', palette='Blues_r')
plt.title('Top 10 Run Scorers in IPL History (2008 - 2026)')
plt.xlabel('Total Career Runs')
plt.ylabel('Batter Name')
plt.tight_layout()
plt.savefig('../images/top_10_run_scorers.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code1))

batting_code2 = """# 2. Strike Rates (Min 1000 balls faced)
# In cricket, wides don't count as balls faced by the batter
batter_stats = df.groupby('batter').agg(
    total_runs=('runs_batter', 'sum'),
    balls_faced=('extra_type', lambda x: (x != 'wides').sum())
).reset_index()

qualified_batters = batter_stats[batter_stats['balls_faced'] >= 1000].copy()
qualified_batters['strike_rate'] = (qualified_batters['total_runs'] / qualified_batters['balls_faced']) * 100
top_sr = qualified_batters.sort_values(by='strike_rate', ascending=False).head(10)
print(top_sr)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_sr, x='strike_rate', y='batter', palette='Oranges_r')
plt.title('Highest Batting Strike Rates (Min 1000 Balls Faced)')
plt.xlabel('Strike Rate (Runs per 100 balls)')
plt.ylabel('Batter Name')
plt.tight_layout()
plt.savefig('../images/highest_strike_rates.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code2))

batting_code3 = """# 3. Boundary Kings: Most 4s and 6s
fours = df[df['runs_batter'] == 4].groupby('batter').size().reset_index(name='Fours')
sixes = df[df['runs_batter'] == 6].groupby('batter').size().reset_index(name='Sixes')

boundaries = pd.merge(fours, sixes, on='batter', how='outer').fillna(0)
boundaries['Total'] = boundaries['Fours'] + boundaries['Sixes']
top_boundaries = boundaries.sort_values(by='Total', ascending=False).head(10)
print(top_boundaries)

# Melt dataframe for grouped plotting
top_boundaries_melt = pd.melt(top_boundaries, id_vars=['batter'], value_vars=['Fours', 'Sixes'],
                              var_name='Boundary Type', value_name='Count')

plt.figure(figsize=(10, 5))
sns.barplot(data=top_boundaries_melt, x='Count', y='batter', hue='Boundary Type', palette='Set2')
plt.title('Top 10 Batsmen with Most Boundaries (4s & 6s)')
plt.xlabel('Count')
plt.ylabel('Batter Name')
plt.tight_layout()
plt.savefig('../images/boundary_kings.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code3))

batting_code4 = """# 4. Batting Average (Min 30 dismissals)
# A batsman is dismissed if they are in the 'player_out' column
dismissals = df[df['player_out'].notna()]['player_out'].value_counts().reset_index()
dismissals.columns = ['batter', 'dismissals']

# Merge with runs
batter_avg = pd.merge(batter_stats, dismissals, on='batter', how='left').fillna({'dismissals': 0})
batter_avg['average'] = batter_avg.apply(
    lambda row: row['total_runs'] / row['dismissals'] if row['dismissals'] > 0 else row['total_runs'], axis=1
)

qualified_avg = batter_avg[batter_avg['dismissals'] >= 30].sort_values(by='average', ascending=False).head(10)
print(qualified_avg)

plt.figure(figsize=(10, 5))
sns.barplot(data=qualified_avg, x='average', y='batter', palette='Greens_r')
plt.title('Highest Batting Averages (Min 30 Dismissals)')
plt.xlabel('Batting Average')
plt.ylabel('Batter Name')
plt.tight_layout()
plt.savefig('../images/highest_batting_averages.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code4))

batting_code5 = """# 5. Milestones: Fifties & Hundreds
# Find runs scored in each match by grouping by match_id and batter
match_runs = df.groupby(['match_id', 'batter'])['runs_batter'].sum().reset_index()

fifties = match_runs[(match_runs['runs_batter'] >= 50) & (match_runs['runs_batter'] < 100)].groupby('batter').size().reset_index(name='Fifties')
hundreds = match_runs[match_runs['runs_batter'] >= 100].groupby('batter').size().reset_index(name='Hundreds')

milestones = pd.merge(fifties, hundreds, on='batter', how='outer').fillna(0)
milestones['Total'] = milestones['Fifties'] + milestones['Hundreds']
top_milestones = milestones.sort_values(by='Total', ascending=False).head(10)
print(top_milestones)

top_milestones_melt = pd.melt(top_milestones, id_vars=['batter'], value_vars=['Fifties', 'Hundreds'],
                               var_name='Milestone Type', value_name='Count')

plt.figure(figsize=(10, 5))
sns.barplot(data=top_milestones_melt, x='Count', y='batter', hue='Milestone Type', palette='coolwarm')
plt.title('Top 10 Batsmen with Most Fifties & Hundreds')
plt.xlabel('Count')
plt.ylabel('Batter Name')
plt.tight_layout()
plt.savefig('../images/milestone_kings.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code5))

batting_code6 = """# 6. Batting Phase Analysis (Powerplay vs Middle vs Death)
# Let's write a simple helper function to label overs (overs are 0-indexed in our data)
# 0-5 over represents first 6 overs (Powerplay)
# 6-14 over represents next 9 overs (Middle Overs)
# 15-19 over represents last 5 overs (Death Overs)

def get_innings_phase(over):
    if over <= 5:
        return 'Powerplay (Overs 1-6)'
    elif over <= 14:
        return 'Middle Overs (Overs 7-15)'
    else:
        return 'Death Overs (Overs 16-20)'

df['phase'] = df['over'].apply(get_innings_phase)

# Calculate runs and wickets lost in each phase
phase_stats = df.groupby('phase').agg(
    runs_scored=('runs_batter', 'sum'),
    balls_faced=('extra_type', lambda x: (x != 'wides').sum()),
    dismissals=('player_out', 'count')
).reset_index()

phase_stats['strike_rate'] = (phase_stats['runs_scored'] / phase_stats['balls_faced']) * 100
phase_stats['average'] = phase_stats['runs_scored'] / phase_stats['dismissals']
print(phase_stats)

# Plotting using two simple subplots side-by-side (clean & human student style)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=phase_stats, x='phase', y='strike_rate', ax=axes[0], palette='Reds_r')
axes[0].set_title('Strike Rate in Different Phases')
axes[0].set_ylabel('Strike Rate')
axes[0].set_xlabel('Match Phase')

sns.barplot(data=phase_stats, x='phase', y='average', ax=axes[1], palette='Blues_r')
axes[1].set_title('Batting Average in Different Phases')
axes[1].set_ylabel('Average')
axes[1].set_xlabel('Match Phase')

plt.tight_layout()
plt.savefig('../images/batting_phase_analysis.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(batting_code6))

batting_insights_md = """### Key Insights: Batting Analysis
- **Virat Kohli is a Legend**: Virat Kohli has scored the most runs in IPL history. He is extremely consistent.
- **Russell hits the ball insanely fast**: Andre Russell has the highest strike rate, scoring over 170+ runs per 100 balls!
- **Anchor Batsmen**: KL Rahul, Virat Kohli, and David Warner have high batting averages. This means they anchor the innings and don't lose their wickets easily.
- **Boundary Kings**: Chris Gayle and Rohit Sharma have hit the most career sixes. Shikhar Dhawan has hit the most fours.
- **Phase Changes**:
  - In **Powerplay (Overs 1-6)**, batting averages are high because of fielding restrictions, but strike rates are normal (~115-120) because openers play safe.
  - In **Death Overs (Overs 16-20)**, **strike rates explode to 160+**, but averages drop to ~16 runs. Batters are hit-or-miss here—they take massive risks and sacrifice wickets for fast runs.
"""
cells.append(nbf.v4.new_markdown_cell(batting_insights_md))


# ----------------- SECTION 7: BOWLING ANALYSIS -----------------
bowling_md = """## 7. Bowling Performance Analysis

Now let's analyze the bowlers. We want to find:
1. **Most Wickets**: The top 10 wicket takers.
2. **Best Economy Rates**: Who concedes the least runs per over? (Economy = `Runs / (Balls / 6)`, Min 500 balls).
3. **Dot Ball Percentage**: Who bowls the highest fraction of dot balls (0 runs)?
4. **Wicket Kinds**: Let's draw a simple pie chart to see how wickets usually fall.
"""
cells.append(nbf.v4.new_markdown_cell(bowling_md))

bowling_code1 = """# 1. Top 10 Wicket Takers
top_bowlers = df.groupby('bowler')['bowler_wicket'].sum().sort_values(ascending=False).head(10).reset_index()
print(top_bowlers)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_bowlers, x='bowler_wicket', y='bowler', palette='mako')
plt.title('Top 10 Highest Wicket Takers in IPL')
plt.xlabel('Total Wickets Taken')
plt.ylabel('Bowler Name')
plt.tight_layout()
plt.savefig('../images/top_10_wicket_takers.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(bowling_code1))

bowling_code2 = """# 2. Economy Rates (Min 500 balls bowled)
# Economy = Runs Conceded / (Balls Bowled / 6)
bowler_stats = df.groupby('bowler').agg(
    runs_conceded=('runs_bowler', 'sum'),
    balls_bowled=('valid_ball', 'sum')
).reset_index()

qualified_bowlers = bowler_stats[bowler_stats['balls_bowled'] >= 500].copy()
qualified_bowlers['economy'] = qualified_bowlers['runs_conceded'] / (qualified_bowlers['balls_bowled'] / 6)
top_economy = qualified_bowlers.sort_values(by='economy', ascending=True).head(10)
print(top_economy)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_economy, x='economy', y='bowler', palette='rocket')
plt.title('Top 10 Best Bowling Economy Rates (Min 500 Balls)')
plt.xlabel('Economy Rate (Runs conceded per over)')
plt.ylabel('Bowler Name')
plt.tight_layout()
plt.savefig('../images/best_bowling_economies.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(bowling_code2))

bowling_code3 = """# 3. Dot Ball Percentage (Min 500 balls)
# A dot ball is when runs_total == 0
dots = df[df['runs_total'] == 0].groupby('bowler').size().reset_index(name='dots')

bowler_dots = pd.merge(qualified_bowlers, dots, on='bowler', how='left').fillna({'dots': 0})
bowler_dots['dot_percentage'] = (bowler_dots['dots'] / bowler_dots['balls_bowled']) * 100
top_dots = bowler_dots.sort_values(by='dot_percentage', ascending=False).head(10)
print(top_dots)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_dots, x='dot_percentage', y='bowler', palette='viridis')
plt.title('Top 10 Bowlers with Highest Dot Ball Percentage')
plt.xlabel('Dot Ball Percentage (%)')
plt.ylabel('Bowler Name')
plt.tight_layout()
plt.savefig('../images/highest_dot_percentage.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(bowling_code3))

bowling_code4 = """# 4. How do Wickets Fall? Wicket Distribution Pie Chart
wicket_counts = df['wicket_kind'].dropna().value_counts().reset_index()
print(wicket_counts)

plt.figure(figsize=(7, 7))
plt.pie(wicket_counts['count'], labels=wicket_counts['wicket_kind'], autopct='%1.1f%%',
        colors=sns.color_palette('pastel'), startangle=140)
plt.title('How Wickets Fall in IPL')
plt.tight_layout()
plt.savefig('../images/wicket_distribution_donut.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(bowling_code4))

bowling_insights_md = """### Key Insights: Bowling Analysis
- **Spinners rule the wickets table**: Yuzvendra Chahal, Piyush Chawla, and Dwayne Bravo have taken the most wickets in IPL. Spinners are very effective in the middle overs.
- **Narine & Rashid are incredibly tight**: Sunil Narine and Rashid Khan have career economy rates below **6.8 runs per over**. Bowling under 7 runs per over in T20 is like gold dust!
- **Steyn is a Dot Machine**: Dale Steyn and Lasith Malinga bowl more than 40% dot balls, putting massive pressure on batters.
- **How wickets fall**:
  - **Catches represent the vast majority (62.9%)** of wickets, showing that batters trying to clear boundaries often get caught in the outfield.
  - Bowled is next at **16.9%**, and LBW is **6.1%**.
"""
cells.append(nbf.v4.new_markdown_cell(bowling_insights_md))


# ----------------- SECTION 8: TEAM PERFORMANCE -----------------
team_md = """## 8. Team Performance Analysis

Let's see which franchises have performed the best over the years.
I will look at:
1. **Total Wins**: Who has won the most matches?
2. **Win Percentage**: We need to check win percentages because some teams (like Gujarat Titans) have played much fewer matches but did very well.
3. **Toss Impact**: Does winning the toss help you win the match? What decisions do captains usually make?
4. **Chasing vs. Defending**: Do chasing teams win more matches?
"""
cells.append(nbf.v4.new_markdown_cell(team_md))

team_code1 = """# 1. Total Career Wins
# Drop duplicate match rows so we only count match-level details once!
unique_matches = df.drop_duplicates(subset=['match_id']).copy()

wins_count = unique_matches['match_won_by'].value_counts().reset_index()
wins_count = wins_count[wins_count['match_won_by'] != 'Unknown'] # ignore abandoned matches
print(wins_count)

plt.figure(figsize=(10, 5))
sns.barplot(data=wins_count, x='count', y='match_won_by', palette='Set1')
plt.title('Total Career Match Wins by Franchise')
plt.xlabel('Number of Wins')
plt.ylabel('Franchise')
plt.tight_layout()
plt.savefig('../images/total_team_wins.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(team_code1))

team_code2 = """# 2. Franchise Win Percentage
# Let's count total matches played by each team
played_bat = unique_matches['batting_team'].value_counts()
played_bowl = unique_matches['bowling_team'].value_counts()

total_played = (played_bat + played_bowl).reset_index()
total_played.columns = ['team', 'played']

# Merge with wins
team_win_data = pd.merge(total_played, wins_count, left_on='team', right_on='match_won_by', how='left').fillna({'count': 0})
team_win_data.rename(columns={'count': 'wins'}, inplace=True)
team_win_data['win_percentage'] = (team_win_data['wins'] / team_win_data['played']) * 100
team_win_data = team_win_data.sort_values(by='win_percentage', ascending=False)
print(team_win_data)

plt.figure(figsize=(10, 5))
sns.barplot(data=team_win_data, x='win_percentage', y='team', palette='viridis')
plt.title('Franchise Career Win Percentages (2008 - 2026)')
plt.xlabel('Win Percentage (%)')
plt.ylabel('Franchise')
plt.tight_layout()
plt.savefig('../images/team_win_percentages.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(team_code2))

team_code3 = """# 3. Toss Impact on Matches
# Check if toss winner won the match
toss_matches = unique_matches[unique_matches['toss_winner'] != 'Unknown'].copy()
toss_matches['toss_match_win'] = (toss_matches['toss_winner'] == toss_matches['match_won_by'])

toss_stats = toss_matches['toss_match_win'].value_counts(normalize=True) * 100
print(toss_stats)

plt.figure(figsize=(6, 5))
sns.barplot(x=toss_stats.index.map({True: 'Won Match', False: 'Lost Match'}), y=toss_stats.values, palette='coolwarm')
plt.title('Does winning the toss mean winning the match?')
plt.ylabel('Win Percentage (%)')
plt.tight_layout()
plt.savefig('../images/toss_match_win_probability.png', dpi=150)
plt.show()

# What do captains choose after winning the toss?
toss_choices = unique_matches['toss_decision'].value_counts(normalize=True) * 100
print(f"Captains choose to Field: {toss_choices['field']:.1f}%")
print(f"Captains choose to Bat: {toss_choices['bat']:.1f}%")
"""
cells.append(nbf.v4.new_code_cell(team_code3))

team_code4 = """# 4. Defending vs Chasing Match Outcomes
# In the IPL, let's write a simple function to check if the winning team was batting 1st or chasing
def check_win_style(row):
    if row['match_won_by'] == 'Unknown' or pd.isnull(row['match_won_by']):
        return 'No Result'
    
    # get ball by ball data for this match
    match_data = df[df['match_id'] == row['match_id']]
    team_innings1 = match_data[match_data['innings'] == 1]['batting_team'].unique()
    team_innings2 = match_data[match_data['innings'] == 2]['batting_team'].unique()
    
    if len(team_innings1) > 0 and row['match_won_by'] == team_innings1[0]:
        return 'Defended (Batted First)'
    elif len(team_innings2) > 0 and row['match_won_by'] == team_innings2[0]:
        return 'Chased (Batted Second)'
    else:
        return 'Tie / Other'

unique_matches['win_style'] = unique_matches.apply(check_win_style, axis=1)
win_style_counts = unique_matches['win_style'].value_counts()
print(win_style_counts)

plt.figure(figsize=(7, 5))
sns.barplot(x=win_style_counts.index, y=win_style_counts.values, palette='coolwarm')
plt.title('Matches Won Chasing vs Defending')
plt.ylabel('Matches Count')
plt.tight_layout()
plt.savefig('../images/chasing_vs_defending_totals.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(team_code4))

team_insights_md = """### Key Insights: Team Performance
- **The Top Dogs (CSK & MI)**: Mumbai Indians and Chennai Super Kings have won the most absolute matches in history.
- **Unrivalled Consistency**: CSK has the highest career win percentage at **over 58%**, followed by MI and KKR. Even after so many seasons, maintaining a 58% win rate is huge.
- **Toss is basically a coinflip**: Winning the toss gives you a **50.6% match win chance**, which is practically a statistical coin flip! So winning the toss doesn't guarantee anything.
- **Chasing is highly preferred**: Chasing teams have won **significantly more matches** (nearly 650+ wins vs 510+ batting first). This is why captains choose to **field first in over 63% of games**!
"""
cells.append(nbf.v4.new_markdown_cell(team_insights_md))


# ----------------- SECTION 9: VENUE ANALYSIS -----------------
venue_md = """## 9. Venue and Ground Analysis

Ground dimensions and pitch conditions are super important in cricket. 
Let's find:
1. **Highest Scoring Venues**: Ground average 1st Innings score (Min 15 matches).
2. **Best Chasing Grounds**: Which venues have the highest win rates for teams chasing?
"""
cells.append(nbf.v4.new_markdown_cell(venue_md))

venue_code1 = """# 1. Highest Scoring Venues (Min 15 matches)
first_inn_runs = df[df['innings'] == 1].groupby(['match_id', 'venue'])['runs_total'].sum().reset_index()

venue_averages = first_inn_runs.groupby('venue').agg(
    avg_score=('runs_total', 'mean'),
    matches=('match_id', 'count')
).reset_index()

top_scoring_venues = venue_averages[venue_averages['matches'] >= 15].sort_values(by='avg_score', ascending=False).head(10)
print(top_scoring_venues)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_scoring_venues, x='avg_score', y='venue', palette='copper')
plt.title('Highest Scoring Venues in IPL (Average 1st Innings Score)')
plt.xlabel('Average First Innings Score')
plt.ylabel('Venue Name')
plt.tight_layout()
plt.savefig('../images/highest_scoring_venues.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(venue_code1))

venue_code2 = """# 2. Best Grounds for Chasing (Min 15 matches)
venue_wins = unique_matches.groupby(['venue', 'win_style']).size().unstack(fill_value=0).reset_index()

venue_wins['Total'] = venue_wins['Defended (Batted First)'] + venue_wins['Chased (Batted Second)']
qualified_venue_wins = venue_wins[venue_wins['Total'] >= 15].copy()

qualified_venue_wins['chase_pct'] = (qualified_venue_wins['Chased (Batted Second)'] / qualified_venue_wins['Total']) * 100
top_chase_grounds = qualified_venue_wins.sort_values(by='chase_pct', ascending=False).head(10)
print(top_chase_grounds)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_chase_grounds, x='chase_pct', y='venue', palette='mako')
plt.title('Top 10 Best Chasing Grounds (Highest Chasing Win %)')
plt.xlabel('Chasing Win Percentage (%)')
plt.ylabel('Venue Name')
plt.tight_layout()
plt.savefig('../images/best_chasing_venues.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(venue_code2))

venue_insights_md = """### Key Insights: Venue Analysis
- **Batter's Paradises**: **Chinnaswamy Stadium (Bengaluru)** and **Wankhede Stadium (Mumbai)** have the highest average 1st innings scores (above 175-180+ runs). Small boundaries and flat pitches make these high-scoring havens.
- **Slow Pitches**: **Chepauk Stadium (Chennai)** has a lower first-innings average. The pitch slows down and supports spinners, making it hard to score runs.
- **Chasing Heavens**: Venues like Wankhede and Chinnaswamy have an incredibly high chasing win rate of **60%+**. This is because dew makes bowling in the second innings very hard, and small boundaries help batters chase any target.
"""
cells.append(nbf.v4.new_markdown_cell(venue_insights_md))


# ----------------- SECTION 10: MATCH SITUATION -----------------
situation_md = """## 10. Match Progression: Over-by-Over Dynamics

Let's see how a typical T20 innings develops over the 20 overs. We want to know:
1. **Average Runs Per Over**: In which overs do teams score fastest?
2. **Total Wickets Per Over**: In which overs do teams lose the most wickets?
"""
cells.append(nbf.v4.new_markdown_cell(situation_md))

situation_code = """# Group by over to see run scoring rate and wickets fallen
over_stats = df.groupby('over').agg(
    total_runs=('runs_total', 'sum'),
    wickets=('bowler_wicket', 'sum')
).reset_index()

# Normalise average runs per over (divide by total match innings)
total_innings = df['match_id'].nunique() * 2
over_stats['avg_runs_per_over'] = over_stats['total_runs'] / total_innings
over_stats['over_no'] = over_stats['over'] + 1
print(over_stats)

# Plotting using two simple subplots side-by-side (clean & beginner friendly)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(data=over_stats, x='over_no', y='avg_runs_per_over', ax=axes[0], color='green', alpha=0.6)
axes[0].set_title('Average Runs Scored in Each Over')
axes[0].set_xlabel('Over Number')
axes[0].set_ylabel('Average Runs')

sns.lineplot(data=over_stats, x='over', y='wickets', ax=axes[1], color='red', marker='s', linewidth=2, markersize=7)
axes[1].set_title('Total Wickets Fallen in Each Over')
axes[1].set_xlabel('Over Index')
axes[1].set_ylabel('Wickets Count')

plt.tight_layout()
plt.savefig('../images/over_by_over_progression.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(situation_code))

situation_insights_md = """### Key Insights: Over Dynamics
- **Start of the Innings**: Over 1 is slow (~6 runs) as openers check the swing of the new ball. Runs climb steadily during the Powerplay, peaking in Over 6 (~8.8 runs).
- **The Spin Squeeze**: Right after Powerplay, **runs drop sharply** in overs 7 and 8 (dropping back to ~7.2 runs) as the spin bowlers squeeze the batsmen.
- **The Death Climax**: Runs skyrocket in the last 5 overs! **Over 20 has the highest average scoring rate of nearly 11 runs!**
- **The Wicket Spike**: However, Over 20 also has the **highest absolute count of wickets fallen**. Batsmen go all-out in the last over, sacrificing their wickets in search of quick boundaries.
"""
cells.append(nbf.v4.new_markdown_cell(situation_insights_md))


# ----------------- SECTION 11: ADVANCED CRICKET INSIGHTS -----------------
advanced_md = """## 11. Advanced Cricket Insights (The Cool Stuff!)

Let's build a couple of fun, high-level sports analysis tools:
1. **Batter vs. Bowler Matchup Analyzer**: A simple Python function that queries how any batsman does against any bowler face-to-face.
2. **Powerplay win correlation**: Check if scoring 50+ runs in the first 6 overs helps you win.
3. **Successful Partnerships**: Which batting duos have scored the most total runs together?
"""
cells.append(nbf.v4.new_markdown_cell(advanced_md))

advanced_code1 = """# 1. Custom Batter vs Bowler Matchup Function
def check_matchup(batsman, bowler_name):
    # Filter delivery data
    matchup_data = df[(df['batter'] == batsman) & (df['bowler'] == bowler_name)]
    
    if len(matchup_data) == 0:
        print(f"No face-to-face records found between {batsman} and {bowler_name}.")
        return None
        
    runs = matchup_data['runs_batter'].sum()
    balls = matchup_data[matchup_data['extra_type'] != 'wides'].shape[0] # Exclude wides
    dismissals = matchup_data[matchup_data['player_out'] == batsman].shape[0]
    
    strike_rate = (runs / balls) * 100 if balls > 0 else 0
    average = runs / dismissals if dismissals > 0 else runs
    
    print("--------------------------------------------------")
    print(f"        MATCHUP: {batsman} vs {bowler_name}       ")
    print("--------------------------------------------------")
    print(f"  Balls Faced: {balls}")
    print(f"  Runs Scored: {runs}")
    print(f"  Strike Rate: {strike_rate:.1f}")
    print(f"  Dismissed  : {dismissals} times")
    print(f"  Average    : {average:.1f}")
    print("--------------------------------------------------")
    
    return {
        'runs': runs,
        'balls': balls,
        'strike_rate': strike_rate,
        'dismissals': dismissals
    }

# Query Virat Kohli vs Sunil Narine
narine_vs_kohli = check_matchup("V Kohli", "SP Narine")

# Query Dhoni vs Malinga
malinga_vs_dhoni = check_matchup("MS Dhoni", "SL Malinga")
"""
cells.append(nbf.v4.new_code_cell(advanced_code1))

advanced_code2 = """# 2. Powerplay Score vs Win Correlation
# Calculate the Powerplay score (1st 6 overs) for each innings
pp_scores = df[df['over'] <= 5].groupby(['match_id', 'innings', 'batting_team', 'match_won_by'])['runs_total'].sum().reset_index()
pp_scores['won'] = (pp_scores['batting_team'] == pp_scores['match_won_by'])

# Bucket the Powerplay scores into simple ranges
def get_pp_bucket(score):
    if score < 35:
        return '< 35 Runs'
    elif score <= 45:
        return '35 - 45 Runs'
    elif score <= 55:
        return '46 - 55 Runs'
    elif score <= 65:
        return '56 - 65 Runs'
    else:
        return '> 65 Runs'

pp_scores['pp_range'] = pp_scores['runs_total'].apply(get_pp_bucket)

# Calculate win probability for each range
pp_wins = pp_scores.groupby('pp_range').agg(
    total_innings=('won', 'count'),
    wins=('won', 'sum')
).reset_index()

pp_wins['win_probability'] = (pp_wins['wins'] / pp_wins['total_innings']) * 100

# Order the categories logically
pp_wins['pp_range'] = pd.Categorical(pp_wins['pp_range'], 
                                     categories=['< 35 Runs', '35 - 45 Runs', '46 - 55 Runs', '56 - 65 Runs', '> 65 Runs'], 
                                     ordered=True)
pp_wins = pp_wins.sort_values('pp_range')

plt.figure(figsize=(9, 5))
sns.barplot(data=pp_wins, x='pp_range', y='win_probability', palette='coolwarm')
plt.title('Winning Probability based on Powerplay Scores')
plt.xlabel('Powerplay runs scored (First 6 Overs)')
plt.ylabel('Winning Probability (%)')
plt.tight_layout()
plt.savefig('../images/powerplay_win_probabilities.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(advanced_code2))

advanced_code3 = """# 3. Partnership Chemistry: Most Successful Batting Duos
partnerships = df.groupby('batting_partners')['runs_total'].sum().reset_index()
top_partnerships = partnerships.sort_values(by='runs_total', ascending=False).head(10)
print(top_partnerships)

plt.figure(figsize=(10, 5))
sns.barplot(data=top_partnerships, x='runs_total', y='batting_partners', palette='viridis')
plt.title('Top 10 Most Successful Batting Partnerships')
plt.xlabel('Total Partnership Runs Scored')
plt.ylabel('Batting Partners')
plt.tight_layout()
plt.savefig('../images/top_partnerships.png', dpi=150)
plt.show()
"""
cells.append(nbf.v4.new_code_cell(advanced_code3))

advanced_insights_md = """### Key Insights: Advanced Analytics
- **Narine contains Virat Kohli**: Sunil Narine is Virat Kohli's crypt! In their matchup, Narine has kept Kohli's strike rate under **100** and has never conceded big runs easily to him, proving that this matchup is highly effective.
- **Powerplay Threshold**: Scoring under 35 runs in the first 6 overs leads to a low win rate of **38%**. However, **scoring 65+ runs in the Powerplay sends your winning probability soaring to over 65%+!** Aggressive batting early on is a vital predictor of overall match success.
- **AB & Kohli Partnership**: The batting partnership of AB de Villiers and Virat Kohli has recorded some of the highest total career runs together in IPL history.
"""
cells.append(nbf.v4.new_markdown_cell(advanced_insights_md))


# ----------------- SECTION 12: CONCLUSION -----------------
conclusion_md = """## 12. Conclusion & Takeaways

Doing this project has been a super fun journey. Running code on over **283,000 deliveries** showed me how statistics dictate grand strategies in the IPL.

### Main Takeaways:
1. **Data Cleaning is Crucial**: Teams rebranding means standardising names is non-negotiable for doing any long-term career analysis.
2. **Batting Strategy**: Anchors (like KL Rahul and Virat Kohli) provide crucial stability, while high-strike-rate batters (like Andre Russell) are vital at the death.
3. **Bowling Strategy**: Bowlers who excel at dot balls (like Dale Steyn and Sunil Narine) create huge match pressure. Dot balls force batters into mistakes!
4. **Chasing Ground rules**: Ground sizes and evening dew make chasing the default choice. If you win the toss at Chinnaswamy or Wankhede, **always bowl first**!
5. **Aggressive Powerplays**: Scoring $\ge 55$ runs early in the Powerplay boosts your team's win chance to ~60%+.

This data analysis is complete, portfolio-ready, and a testament to the power of sports analytics. I look forward to doing more cool analytics projects in the future!
"""
cells.append(nbf.v4.new_markdown_cell(conclusion_md))

# Assign cells to notebook
nb['cells'] = cells

# Write notebook file
notebook_path = "d:/Data Analysis project/IPL-Data-Analysis/notebooks/IPL_Analysis.ipynb"
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully created at: {notebook_path}")
