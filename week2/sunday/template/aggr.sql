select {{ ','.join(key_column) }}
    {% for metric in metrics -%}
      , {{ metric }}(averageRating) as rating_{{ metric }}
    {% endfor -%}
from title_ratings join title_basics using (tconst) 
group by {{ ','.join(key_column) }}
order by 2 desc
limit 5