import glob 
import pandas as pd

all_files = glob.glob("capstone.*.jsonl")
df_list = []
for f in all_files:
    df_temp = pd.read_json(f, lines=True)
    df_list.append(df_temp)
    print(f"f:{f}, df_temp.shape:{df_temp.shape}")

df = pd.concat(df_list, ignore_index=True)

df.to_csv("data/capstone.csv", index=False)