## TASK 1



## Scoring Algorithm

The scoring algorithm is composed of two main parts: the calculation of a **weighted average rating** and the computation of the **final score**. This method ensures that ratings with more votes have a greater impact on the score. On the other hand, it try to get rid of the outliers.

### 1. Weighted Average Rating

Instead of using a simple arithmetic mean, the algorithm calculates a weighted average to emphasize ratings with more votes. This helps mitigate the impact of outliers. The formula is:

\[
\text{weighted\_average} = \frac{\text{rate} \times (\text{rate\_count})^2}{\text{total\_rate\_squared\_count}}
\]

- **rate**: The average rating value for an item.
- **rate_count**: The number of votes associated with that rating.
- **total_rate_squared_count**: The sum of the squares of the vote counts for all items or ratings considered.

### 2. Final Score Calculation

In addition to the quality of the rating, the vote count is also an important factor. The final score is computed as follows:

\[
\text{score} = \left( \text{weighted\_average} \times 0.78 \right) + \left( \frac{\text{count} \times 0.22}{\text{total\_count}} \right)
\]

- **weighted_average**: The weighted average computed from the previous formula.
- **count**: The number of votes for the particular item.
- **total_count**: The total number of votes across all items.

#### Rationale Behind the Weights

- **0.78 (Weighted Average Contribution)**: Emphasizes that the quality of the rating is the primary factor.
- **0.22 (Vote Count Contribution)**: Ensures that the total number of votes plays a significant, yet secondary, role in the final score.

This combination is intended to balance cases where a moderately high rating with a high vote count (e.g., 4.5 with 1,000 votes) is preferred over a near-perfect rating with very few votes (e.g., 5.0 with 10 votes), while still giving some credit to highly rated items even with fewer votes.

## Usage

Below is an example of how to implement the scoring algorithm in Python:

```python
def calculate_weighted_average(rate, rate_count, total_rate_squared_count):
    return (rate * (rate_count ** 2)) / total_rate_squared_count

def calculate_final_score(weighted_average, count, total_count):
    return (weighted_average * 0.78) + ((count * 0.22) / total_count)
```

## TASK 2

In this task, we build an efficient pipeline for finding similar movies. The process is designed to handle large datasets without running into memory issues while ensuring fast lookup times. The pipeline includes the following key steps:

1. **Convert Data into a Sparse Matrix**  
   To avoid memory errors when working with large datasets, the data is converted into a sparse matrix format. This format stores only non-zero elements, drastically reducing memory usage while retaining essential information for further analysis.

2. **Dimensionality Reduction**  
   After creating the sparse matrix, I apply Dimensionality Reduction with TruncatedSVD method to speed up the process.

3. **Create Annoy Index**  
   To enable fast and efficient similarity searches, I build an Annoy index from the reduced dataset. Annoy is optimized for quick lookup. Therefore, I used it to speed up the process.

4. **Recommendation for User**
    Make the recommendation


## TASK 3

I calculate their cosine similarity score and set threshold then look they are similar or different. 


# Dependicies:


```python

numpy scipy pandas annoy scikit-learn loguru

```

# Each Task can be runned by tasks/task{task_id}.py


# Deficiencies and areas for improvement

1. **I used pandas for this dataset, which is fine for now, but if the dataset were larger, I should store the data in a database and execute SQL queries to dramatically speed up the process.**
2. **In Task 2, while reducing dimensionality to improve speed, I lose some information.**
3. **I don’t fully understand the third question. I interpreted it as determining whether two movies are similar or not.**
