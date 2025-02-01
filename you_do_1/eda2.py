import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CSV dosyasını yükleme
file_path = '/Users/2na/Documents/tt-bootcamp/you_do_1/organized_data/customer_avg_ratings.csv'
df = pd.read_csv(file_path)

# Grafiklerin kaydedileceği klasörü oluşturma
output_dir = 'plots2'
os.makedirs(output_dir, exist_ok=True)

# Grafikler için genel ayar
sns.set(style="whitegrid")

# Avg_Rating için Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Avg_Rating'], bins=30, kde=True)
plt.title('Distribution of Average Ratings')
plt.xlabel('Average Rating')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'avg_rating_distribution.png'))
plt.close()

# Watch_Count için Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Watch_Count'], bins=30, kde=True)
plt.title('Distribution of Watch Count')
plt.xlabel('Watch Count')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'watch_count_distribution.png'))
plt.close()

# Date_Diff için Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Date_Diff'], bins=30, kde=True)
plt.title('Distribution of Date Difference')
plt.xlabel('Date Difference (days)')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'date_diff_distribution.png'))
plt.close()

# Month bazlı Bar Plot
plt.figure(figsize=(14, 6))
df['Month'] = pd.to_datetime(df['Min_Date']).dt.to_period('M')
sns.countplot(x='Month', data=df, order=df['Month'].sort_values().unique())
plt.title('Count of Customers per Month')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, 'customers_per_month.png'))
plt.close()

# Min_Date ve Max_Date için Çizgi Grafiği
plt.figure(figsize=(14, 7))
df['Min_Date'] = pd.to_datetime(df['Min_Date'])
df['Max_Date'] = pd.to_datetime(df['Max_Date'])

plt.plot(df['Min_Date'], df['Avg_Rating'], label='Min Date Avg Rating', marker='o')
plt.plot(df['Max_Date'], df['Avg_Rating'], label='Max Date Avg Rating', marker='x')

plt.title('Average Ratings over Min and Max Dates')
plt.xlabel('Date')
plt.ylabel('Average Rating')
plt.legend()
plt.savefig(os.path.join(output_dir, 'avg_ratings_min_max_dates.png'))
plt.close()

# Min_Date için Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Min_Date'], bins=30, kde=True)
plt.title('Distribution of Min Date')
plt.xlabel('Min Date')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'min_date_distribution.png'))
plt.close()

# Max_Date için Histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['Max_Date'], bins=30, kde=True)
plt.title('Distribution of Max Date')
plt.xlabel('Max Date')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_dir, 'max_date_distribution.png'))
plt.close()