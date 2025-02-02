create table if not exists rating as
select *
from read_csv(
        'rating_*.txt',
        columns = { 'MovieId': 'int',
        'UserId': 'int',
        'Date': 'date',
        'Rate' :'int' }
    );

CREATE TABLE IF NOT EXISTS titles AS
SELECT * 
FROM read_csv(
        'movie_titles_new.csv',
        columns = {
            "index": "int",
            'MovieId': 'int',
            'Year': 'varchar',
            "Title" : 'text'
        },
        delim = ',',
        quote = '"',
        null_padding = TRUE,
        header = TRUE
    );


CREATE TABLE IF NOT EXISTS normalized_rates AS(
    SELECT MovieId, UserId, Date, NormalizedRate
    FROM (
        WITH user_info AS (
            SELECT UserId, AVG(Rate) as RateAVG, NULLIF(STDDEV(Rate),0) as RateSTD
            FROM rating
            GROUP BY UserId
        )
        SELECT  a.MovieId, a.UserId, a.Date, a.Rate AS OldRate, (a.Rate - b.RateAVG)/b.RateSTD AS NormalizedRate
        FROM rating a
        LEFT JOIN user_info b
        USING(UserId)
    )
);

-- cold start recommendation:
-- izlenme sayısı düşük olan filmleri henüz eleyemedim ancak ilerlememi paylaşmak istedim.
-- Bu sorunu çözdükten sonra diğer 2 maddedeki talepler için geliştirmeye devam edeceğim.
SELECT a.Title, a.MovieId, MEDIAN(b.NormalizedRate) as NormalizedRateMEDIAN, COUNT(UserId) AS WatchCount
FROM titles a 
LEFT JOIN normalized_rates b
USING(MovieId)
GROUP BY a.Title, a.MovieId
ORDER BY NormalizedRateMEDIAN DESC;





