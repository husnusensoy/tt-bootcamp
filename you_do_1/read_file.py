from typing import Dict, List, Tuple
from collections import defaultdict
from datetime import datetime, time
import csv

class Recommendation_movie:
    def __init__(self):
        self.file_paths =["D:/indirilenler/binge/rating_1.txt","D:/indirilenler/binge/rating_2.txt","D:/indirilenler/binge/rating_3.txt","D:/indirilenler/binge/rating_4.txt"]
        self.csv_path = "D:/indirilenler/binge/movie_titles.csv"

        self.film_ratings_cache = None
        self.user_ids_cache = None

        self.film_ratings_cache, self.user_ids_cache = self.read_txt()
        self.movie_dict = self.read_csv()
        self.avg_ratings, self.total = self.calculate_avg_ratings()
        self.avg_rating_by_year = self.calculate_avg_ratings_by_year()
        self.top_movies = self.sort_by_ratings(self.avg_ratings)
        self.user_list = list(self.user_ids_cache.keys())

    # start_time = datetime.now()
    def read_txt(self):
        film_ratings: Dict[int, List[Tuple[int, str, int]]] = defaultdict(list)
        user_ids: Dict[int, List[Tuple[int,int]] ] = defaultdict(list)
        for file_path in self.file_paths:
            with open(file_path, "r") as file:

                for i ,line in enumerate(file):

                    # if i >500000:
                    #     break

                  
                    movie_id, user_id, date, rating = line.strip().split(",")
                    
                    movie_id =int(movie_id)
                    user_id= int(user_id)
                    rating= float(rating)

                    film_ratings[movie_id].append((user_id, date, rating))
                    user_ids[user_id].append((movie_id,  rating))

        return dict(film_ratings), dict(user_ids)



    def read_csv(self):
        movies = {}
        with open(self.csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file) #keep the memory
            # csv_reader = csv.DictReader(csv_file) dict olarak tutar ilk columnu belirteç olarak alır

            for line in csv_reader: 
                movie_id = int(line[0])

                published_year = line[1] if line[1] != 'NULL' else '2000'
                    
                movies[movie_id] = {
                    'published_year': line[1] , 
                    'movie_name': line[2]
                    }

            

            return movies
        # end_time = datetime.now()
    
    def calculate_avg_ratings(self) -> Dict[int,float]:

        length = {}
    #her film kaç kez oylanmış ona baktık
        for i in self.film_ratings_cache:
            values = self.film_ratings_cache[i]
            ratings = [entry[2] for entry in values]
            avg_rate = sum(ratings)/ len(ratings)

            length[i] = {"avg_rate": avg_rate, "izlenme":len(values)}

        weighted_scores = {}

        for movie_id, data in length.items():
            avg_rate = data["avg_rate"]
            vote_count = data["izlenme"]

     
            weighted_score = avg_rate * vote_count  

            weighted_scores[movie_id] = {
                "weighted_score": weighted_score,
                "avg_rate": avg_rate,
                "izlenme": vote_count
            }

        total_weighted_sum = sum([score["weighted_score"] for score in weighted_scores.values()])
        total_votes = sum([score["izlenme"] for score in weighted_scores.values()])

        final_weighted_average = total_weighted_sum / total_votes if total_votes > 0 else 0

        return weighted_scores, final_weighted_average

    def calculate_avg_ratings_by_year(self) -> Dict[str, List[Dict]]:
        movie_rate_by_year = {}

        for movie_id, movie_info in self.movie_dict.items():
            year = movie_info['published_year']
            movie_name = movie_info['movie_name']
            
            if movie_id in self.film_ratings_cache:
                movie_ratings = self.film_ratings_cache[movie_id]
                ratings_list = [rating for (_, _, rating) in movie_ratings]
                avg_rate = sum(ratings_list) / len(ratings_list)

            
                if year not in movie_rate_by_year:
                    movie_rate_by_year[year] = []
                movie_rate_by_year[year].append({
                    "movie_name": movie_name,
                    "rate": avg_rate,
                    "movie_id": movie_id
                })

        return movie_rate_by_year  

    def sort_by_ratings(self, weighted_scores) -> List[Tuple[int,float]]:
        return sorted(weighted_scores.items(), key=lambda item: item[1]['weighted_score'], reverse=True)

    def cold_start(self, user_id):
        if user_id not in self.user_list:
            print(f"Welcome {user_id}! Here are the top 5 movies for your fresh start:")

            top_5_movies = self.top_movies[:5]

            for i, (movie_id, data) in enumerate(top_5_movies):
                movie_name = self.movie_dict[movie_id]["movie_name"]
                rating = data['weighted_score']  # Veya weighted_score kullanabilirsiniz.
                print(f"{i+1}-) {movie_name}, Rate: {rating:.2f}")
        else:
            print(f"User {user_id} is already registered. No cold start recommendations needed.")


    def our_customer(self, user_id):
        rated_movies = {}
        published_years = []
   
        if user_id in self.user_ids_cache:
            print(f"hey you are.. it is good to see you again. what do you want to watch? these your movies that watched and rated. you can chose like them")
            for movie_id, rating in self.user_ids_cache[user_id]:
                movie_name = self.movie_dict[movie_id]["movie_name"]
                published_year = self.movie_dict[movie_id]["published_year"]
                movie_info = self.movie_dict[movie_id]

                rated_movies[movie_id] = { "name": movie_name, "rating": rating, "published_year": published_year}
                # rated_movies.append((movie_name, rating))
                if str(published_year).isdigit():  
                    published_years.append(int(published_year))

            top_rated_movies = sorted(
                rated_movies.items(), 
                key=lambda x: x[1]["rating"], 
                reverse=True
            )[:5]

            print("\nYour top rated movies:")
            for movie_id, info in top_rated_movies:
                print(f"- {info['name']} ({info['published_year']}) - Your rating: {info['rating']}")

            
            recommendations = []
            for year in published_years:
                if str(year) in self.avg_rating_by_year:  # Yıl string olarak tutuluyor
                    for movie in self.avg_rating_by_year[str(year)]:
                        recommendations.append(movie["movie_name"])

            print(f"\nHere are your recommendations: {recommendations[:5]}")

            
    def compare_movies(self,movie_id, movie_id2):
        now = datetime.now().year

        movie_1 = self.movie_dict[movie_id]
        movie_2 = self.movie_dict[movie_id2]
        print(f"Compare {movie_1} and {movie_2} ")

        if(self.avg_ratings[movie_id]["weighted_score"] < self.avg_ratings[movie_id2]["weighted_score"]):
            print(f"{movie_1["movie_name"]} rate is less than {movie_2["movie_name"]}")
        else:
            print(f"{self.movie_dict[movie_id2]["movie_name"]} rate is less than {self.movie_dict[movie_id]["movie_name"]}")

        age1 = now - int(movie_1["published_year"])
        age2 = now - int(movie_2["published_year"])

        print(f"lets look the age of movies. \n{movie_1["movie_name"]}: {age1} \n{movie_2["movie_name"]} is published: {age2}")


recommender = Recommendation_movie()

# avg = recommender.calculate_avg_ratings()
# print(avg)

recommendations = recommender.cold_start(2)

compare = recommender.compare_movies(1,2)

our_customer = recommender.our_customer(387418)
