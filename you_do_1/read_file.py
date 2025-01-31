from typing import Dict, List, Tuple
import csv
from datetime import datetime


file_path = "D:/indirilenler/binge/rating_1.txt"


def read_txt():
    film_ratings: Dict[int, List[Tuple[int, str, int]]] = {}
    user_ids: Dict[int, List[Tuple[int,int]] ] = {}
    with open(file_path, "r") as file:

        for i, line in enumerate(file):
            if i>5000:
                break
          
            c = line.strip().split(",")
            
            movie_id =int(c[0])
            user_id= int(c[1])
            date= c[2]
            rating= float(c[3])

            if movie_id not in film_ratings:
                film_ratings[movie_id] = []

            if user_id not in user_ids:
                user_ids[user_id] = []

            film_ratings[movie_id].append((user_id, date, rating))
            user_ids[user_id].append((movie_id,  rating))

        return film_ratings, user_ids

csv_path = "D:/indirilenler/binge/movie_titles.csv"

def read_csv():
    movies = {}
    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file) #keep the memory
        # csv_reader = csv.DictReader(csv_file) dict olarak tutar ilk columnu belirteç olarak alır


        for line in csv_reader: 
            movie_id = int(line[0])
            movies[movie_id] = {
                'published_year': line[1] , 
                'movie_name': line[2]
                }

        return movies

                    
ratings, user_ids = read_txt()
# print(user_ids)
 
film_ratings_cache = None
user_ids_cache = None

def read_txt_cached():
    global film_ratings_cache, user_ids_cache
    if film_ratings_cache is None or user_ids_cache is None:
        film_ratings_cache, user_ids_cache = read_txt()
    return film_ratings_cache, user_ids_cache

# İlk çağrıda dosyadan okuyacak, sonrasında bellekte tutacak
ratings, user_ids = read_txt_cached()


def avg_rating(ratings: Dict[int, List[Tuple[int, str, float]]]) -> Dict[int,float]:
    movie_avg_Rate= {}

    for movie_id, movie_ratings in ratings.items():

        ratings_list = [rating for (_,_,rating) in movie_ratings]
        avg_rate = sum(ratings_list) / len(ratings_list)
        movie_avg_Rate[movie_id] = avg_rate

    return movie_avg_Rate

avg= avg_rating(ratings)
sorteds =sorted(avg.items(), key=lambda item: item[1], reverse=True)
# print(sorteds[0][0])

user_id_list = [1,2,3]
top_5_movies = sorteds[:5]
#user id listesi oluştur
def cold_start(user_id):
    movie_dict = read_csv()
    if user_id not in user_id_list:
        print(f"Welcome {user_id}! Here are the top 5 movies for your fresh start:")
        for i,(movie_id, rating) in enumerate(top_5_movies):
            movie_name = movie_dict[movie_id]["movie_name"]
            print(f"{i+1}-) {movie_name},  Rate: {rating:.2f}")
    else:
        print(f"User {user_id} is already registered. No cold start recommendations needed.")

# cold_startt = cold_start(2)


def our_customer(user_id):
    rated_movies = []
    movie_dict = read_csv()
    
    # Kullanıcıya ait tüm verileri al
    if user_id in user_ids:
        print(f"hey you are.. it is good to see you again. what do you want to watch? these your movies that watched and rated. you can chose like them")
        for movie_id, rating in user_ids[user_id]:
            movie_name = movie_dict[movie_id]["movie_name"]

            rated_movies.append((movie_name, rating))
    
    return rated_movies
       

customer = our_customer(387418)
print(customer)

# def compare_movies(movie_id, movie_id2):

# def count_rated_movies(user_ids):
#     # Kullanıcılar ve puanladıkları film sayısını tutacak bir liste
#     user_ratings_count = {}

#     for user_id, ratings in user_ids.items():
#         # Kullanıcının puanladığı film sayısı
#         rated_movies_count = len(ratings)
#         user_ratings_count[user_id] = rated_movies_count

#     # Kullanıcıları, puanladıkları film sayısına göre azalan sırayla sıralama
#     sorted_user_ratings = sorted(user_ratings_count.items(), key=lambda x: x[1])

#     return sorted_user_ratings

# # Kullanıcıların puanladığı film sayısını alıp sıralama
# sorted_user_ratings = count_rated_movies(user_ids)

# # Sonuçları yazdırma
# for user_id, count in sorted_user_ratings:
#     print(f"Kullanıcı ID: {user_id}, Puanladığı Film Sayısı: {count}")

    

# print(avg)
# ratings = film_ratings[1][1][2]
# print(len(film_ratings))
    # print(type(content))  #list
    # print(len(content))



#oku ve movie idye göre dicte kaydet
#movie idye göre avarage rate skoru döndür her biri için ve bunları ayrı bir yerde tut ve büyüükten küçüğe sırala


