# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Tidy Data in Python
# by [Jean-Nicholas Hould](http://www.jeannicholashould.com/)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
import pandas as pd
import datetime
from os import listdir
from os.path import isfile, join
import glob
import re
# -

# ## Column headers are values, not variable names

# ### Pew Research Center Dataset

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.read_csv("./data/pew-raw.csv")
df.head(2)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
formatted_df = pd.melt(df,["religion"], 
                       var_name="income", value_name="freq")
formatted_df = formatted_df.sort_values(by=["religion"])
formatted_df.head(2)
# -

# ### Billboard Top 100 Dataset

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.read_csv("./data/billboard.csv", encoding="mac_latin2")
df.head(2)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Melting
id_vars = ["year","artist.inverted","track","time","genre","date.entered","date.peaked"]
df = pd.melt(frame=df,id_vars=id_vars, var_name="week", value_name="rank")
df[:3]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Formatting 
df["week"] = df['week'].str.extract('(\d+)', expand=False).astype(int)

# + pycharm={"is_executing": false}
df[-3:]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Cleaning out unnecessary rows
df = df.dropna()
df["rank"] = df["rank"].astype(int)
df[-3:]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Create "date" columns
df['date'] = pd.to_datetime(df['date.entered']) + pd.to_timedelta(df['week'], unit='w') - pd.DateOffset(weeks=1)

df = df[["year", "artist.inverted", "track", "time", "genre", "week", "rank", "date"]]
df = df.sort_values(ascending=True, by=["year","artist.inverted","track","week","rank"])

# Assigning the tidy dataset to a variable for future usage
billboard = df

df.head(2)
# -

# ## Multiple types in one table

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
songs_cols = ["year", "artist.inverted", "track", "time", "genre"]
songs = billboard[songs_cols].drop_duplicates()
songs = songs.reset_index(drop=True)
songs["song_id"] = songs.index
songs.head(2)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
ranks = pd.merge(billboard, songs, on=["year","artist.inverted", "track", "time", "genre"])
ranks = ranks[["song_id", "date","rank"]]
ranks.head(2)
# -

# ## Multiple variables stored in one column

# ### Tubercolosis Example

# A few notes on the raw data set:
#
# - The columns starting with "m" or "f" contain multiple variables: 
#     - Sex ("m" or "f")
#     - Age Group ("0-14","15-24", "25-34", "45-54", "55-64", "65", "unknown")
# - Mixture of 0s and missing values("NaN"). This is due to the data collection process and the distinction is important for this dataset.

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.read_csv("./data/tb-raw.csv")
df.head(2)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.melt(df, id_vars=["country","year"], value_name="cases", var_name="sex_and_age")
df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Extract Sex, Age lower bound and Age upper bound group
tmp_df = df["sex_and_age"].str.extract("(\D)(\d+)(\d{2})", expand=False)    
tmp_df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Name columns
tmp_df.columns = ["sex", "age_lower", "age_upper"]
tmp_df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Create `age`column based on `age_lower` and `age_upper`
tmp_df["age"] = tmp_df["age_lower"] + "-" + tmp_df["age_upper"]
tmp_df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Merge 
df = pd.concat([df, tmp_df], axis=1)
df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Drop unnecessary columns and rows
df = df.drop(['sex_and_age',"age_lower","age_upper"], axis=1)
df = df.dropna()
df = df.sort_values(ascending=True,by=["country", "year", "sex", "age"])
df.head(2)
# -

# ## Variables are stored in both rows and columns

# ### Global Historical Climatology Network Dataset

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.read_csv("./data/weather-raw.csv")

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
df = pd.melt(df, id_vars=["id", "year","month","element"], var_name="day_raw")
df.head(4)

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Extracting day
df["day"] = df["day_raw"].str.extract("d(\d+)", expand=False)  
df["id"] = "MX17004"
df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# To numeric values
df[["year","month","day"]] = df[["year","month","day"]].apply(lambda x: pd.to_numeric(x, errors='ignore'))

# Creating a date from the different columns
def create_date_from_year_month_day(row):
    return datetime.datetime(year=row["year"], month=int(row["month"]), day=row["day"])

df["date"] = df.apply(lambda row: create_date_from_year_month_day(row), axis=1)
df = df.drop(['year',"month","day", "day_raw"], axis=1)
df = df.dropna()
df[:2]

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
# Unmelting column "element"
df = df.pivot_table(index=["id","date"], columns="element", values="value")
df.reset_index(drop=False, inplace=True)
df


# -

# ## One type in multiple tables

# ### Baby Names in Illinois

# + jupyter={"outputs_hidden": false} pycharm={"is_executing": false}
def extract_year(string):
    match = re.match(".+(\d{4})", string) 
    if match != None: return match.group(1)
    
path = './data'
allFiles = glob.glob(path + "/201*-baby-names-illinois.csv")
df_list= []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    df.columns = map(str.lower, df.columns)
    df["year"] = extract_year(file_)
    df_list.append(df)
    
df = pd.concat(df_list)
df.head(5)
