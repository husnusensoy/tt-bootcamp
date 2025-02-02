from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict


@dataclass
class Movies:
    published_year: int
    movie_name: str

@dataclass
class Ratings:
    user_id: int
    movie_id: int
    created_date: int
    rate: int

def read_txt(file_name: List[str], delimiter: str = ","):
    ratings_dict: Dict[int, ratings]

    

def read_file(file_name: str | Path,header:bool, delimiter: str = ","):
    movie_dict: Dict[int, Movies] = {}

        
    with Path(file_name).open() as rf:
        if header:
            for i,line in enumerate(rf):
                print(line)
                if i == 0:
                    headers = [h.lower() for h in line.strip().split(delimiter)]
                else:
                    movie_id,published_year, *movie_name = line.strip().split(delimiter)

                    movie_name = ",".join(movie_name)

                    movie = Movies(
                        published_year=published_year,
                        movie_name=str(movie_name)
                    )

                    movie_dict[int(movie_id)] = movie
        else:
            for i, line in enumerate(rf):
                movie_id, published_year, *movie_name = line.strip().split(delimiter)
                movie_name = ",".join(movie_name)  # *name de liste olarka geldi biz de bunun ,le birleştierek strgine çeviridk.
                            
                movie = Movies(
                    # movie_id = int(movie_id),
                    published_year=published_year,
                    movie_name=movie_name
                )

                movie_dict[int(movie_id)] = movie



    return movie_dict
file_paths =["D:/indirilenler/binge/rating_1.txt","D:/indirilenler/binge/rating_2.txt","D:/indirilenler/binge/rating_3.txt","D:/indirilenler/binge/rating_4.txt"]

def read_txt():
        film_ratings: Dict[int, List[Tuple[int, str, int]]] = defaultdict(list)
        user_ids: Dict[int, List[Tuple[int,int]] ] = defaultdict(list)
        for file_path in file_paths:
            with open(file_path, "r") as file:

                for i ,line in enumerate(file):

                    if i>20000:
                        break
            
                    movie_id, user_id, date, rating = line.strip().split(",")
                    
                    movie_id =int(movie_id)
                    user_id= int(user_id)
                    rating= float(rating)

                    film_ratings[movie_id].append((user_id, date, rating))
                    user_ids[user_id].append((movie_id,  rating))

        return dict(film_ratings), dict(user_ids)

def calculate_avg_ratings(ratings):
        movie_avg_Rate= {}
        watcher_count = {}
        for movie_id, movie_ratings in ratings.items():

            ratings_list = [rating for (_,_,rating) in movie_ratings]
            avg_rate = sum(ratings_list) / len(ratings_list)
            movie_avg_Rate[movie_id] = avg_rate

            watcher_count[movie_id] = {"izlenme": len(ratings_list), "rate": avg_rate}

        return watcher_count

if __name__=="__main__":

    movies = read_file("movie_titles.csv", header=False)
    txts, a = read_txt()
    a = calculate_avg_ratings(txts)
    print(type(txts))
    print(a)

   
    # print(movies[17764].movie_name)