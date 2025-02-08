import pandas as pd

# Read the CSV files into DataFrames
test_df = pd.read_csv("data/test.csv")
val_df = pd.read_csv("data/val.csv")

# Concatenate the DataFrames vertically (row-wise)
combined_df = pd.concat([test_df, val_df], axis=0, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv("new_test.csv", index=False)