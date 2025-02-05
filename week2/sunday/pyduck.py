import duckdb
import pandas as pd
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


def generate_report(conn, sql, **kwargs) -> pd.DataFrame:
    rendered_sql = sql.render(**kwargs)
    print(rendered_sql)
    
    return conn.execute(rendered_sql).fetchdf()

if __name__ == "__main__":
    conn = duckdb.connect(database="../imdb.duck")
    
    envi = Environment(loader=FileSystemLoader("template/"))
    
    sql = envi.get_template("aggr.sql")
    
    # print(conn.execute("select * from title_ratings limit 10").fetchdf())
    
    # df = pd.DataFrame({"id":[1,2,3], "name": ["Alice","Bob","Charlie"],"age":[30,35,28]})
    
    # result = duckdb.query("select * from df where age > 30")
    
    result = generate_report(conn, sql, key_column=["titleType"], metrics=["avg"])
    
    print(result)
    
    result = generate_report(conn, sql, key_column=["isAdult"], metrics=["avg"])
    
    print(result)
    
    result = generate_report(conn, sql, key_column=["startYear","isAdult"], metrics=["avg","max","min","median","sum","count","stddev","geomean"])
    
    print(result)