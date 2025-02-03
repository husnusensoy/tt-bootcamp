from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict

from pprint import pprint


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
                    if i>500000:
                        break
            
                    movie_id, user_id, date, rating = line.strip().split(",")
                    
                    movie_id =int(movie_id)
                    user_id= int(user_id)
                    rating= float(rating)

                    film_ratings[movie_id].append((user_id, date, rating))
                    user_ids[user_id].append((movie_id,  rating))

        return dict(film_ratings), dict(user_ids)

def calculate(txt):
    length = {}
    #her film kaç kez oylanmış ona baktık
    for i in txt:
       values = txt[i]
       ratings = [entry[2] for entry in values]
       avg_rate = sum(ratings)/ len(ratings)

       length[i] = {"avg_rate": avg_rate, "izlenme":len(values)}

    weighted_scores = {}

    for movie_id, data in length.items():
        avg_rate = data["avg_rate"]
        vote_count = data["izlenme"]

        # Ağırlıklı Ortalama Hesaplama
        weighted_score = avg_rate * vote_count  # Puan * Oylama sayısı

        weighted_scores[movie_id] = {
            "weighted_score": weighted_score,
            "avg_rate": avg_rate,
            "izlenme": vote_count
        }

    # Ağırlıklı ortalamayı toplam oylama sayısına böleriz
    total_weighted_sum = sum([score["weighted_score"] for score in weighted_scores.values()])
    total_votes = sum([score["izlenme"] for score in weighted_scores.values()])

    final_weighted_average = total_weighted_sum / total_votes if total_votes > 0 else 0

    return final_weighted_average, weighted_scores

    # sorted_length = dict(sorted(length.items(), key=lambda item: item[1]['avg_rate'], reverse=True))
    # return(sorted_length)

def sort_by_ratings(weighted_scores):
    # "weighted_scores" sözlüğünü "weighted_score" değerine göre azalan sırayla sıralar
    return sorted(weighted_scores.items(), key=lambda item: item[1]['weighted_score'], reverse=True)

# Örnek kullanım

if __name__=="__main__":

    movies = read_file("movie_titles.csv", header=False)
    txts, b = read_txt()
    a,b = calculate(txts)
    # first_10 = dict(list(txts.items())[:1])
    # length = {}
    
    # for i in txts:
    #    values = txts[i]
    #    ratings = [entry[2] for entry in values]
    #    avg_rate = sum(ratings)/ len(ratings)

    #    length[i] = {"avg_rate": avg_rate, "izlenme":len(values)}

    #    if length[i]["avg_rate"]

# sorted_length = dict(sorted(length.items(), key=lambda item: item[1]['avg_rate'], reverse=True))

sorteds = sort_by_ratings(b)
print(b[13433]["weighted_score"])




   
    # print(movies[17764].movie_name)