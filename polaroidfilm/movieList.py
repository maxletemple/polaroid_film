import os
import json
import time
import unicodedata

class Movie:
    def __init__(self, title, year, director, format, actors, rating, duration, pic_url, date_added=None):
        self.title = title
        self.pic_url = pic_url
        self.year = year
        self.director = director
        self.format = format
        self.actors = actors
        self.rating = rating
        self.duration = duration
        self.date_added = date_added

    def __str__(self):
        return f"{self.title} ({self.year}) directed by {self.director}, added on {time.ctime(self.date_added)}"


def createMovieInteractive():
    title = input("Enter title: ")
    year = input("Enter year: ")
    director = input("Enter director: ")
    format = input("Enter format (film, series or animated film): ")
    actors = input("Enter actors: ").split(",")
    for i in range(len(actors)):
        actors[i] = actors[i].strip()
    while True:
        rating = input("Enter rating (between 0 and 5): ")
        try:
            if 0 <= float(rating) <= 5:
                rating = float(rating)
                break
        except:
            pass
    duration = input("Enter duration: ")
    pic_url = input(f"Enter picture URL: ") or f"{title.replace(' ', '_').lower()}.jpg"
    pic_url = unicodedata.normalize('NFD', pic_url)
    pic_url = ''.join(c for c in pic_url if unicodedata.category(c) != 'Mn')
    date_added = time.time()
    return Movie(title, year, director, format, actors, rating, duration, pic_url, date_added)

def modifyMovieInteractive(movie):
    title = input(f"Enter title ({movie.title}): ") or movie.title
    year = input(f"Enter year ({movie.year}): ") or movie.year 
    director = input(f"Enter director ({movie.director}): ") or movie.director
    format = input(f"Enter format ({movie.format}): ") or movie.format
    res = input(f"Enter actors ({movie.actors}): ")
    if res == "":
        actors = movie.actors
    else:
        actors = res.split(",")
        for i in range(len(actors)):
            actors[i] = actors[i].strip()
    while True:
        rating = input("Enter rating (between 0 and 5): ") or movie.rating
        try:
            if 0 <= float(rating) <= 5:
                rating = float(rating)
                break
        except:
            pass
    duration = input(f"Enter duration ({movie.duration}): ") or movie.duration
    pic_url = input(f"Enter picture URL ({movie.pic_url}): ") or movie.pic_url
    pic_url = unicodedata.normalize('NFD', pic_url)
    pic_url = ''.join(c for c in pic_url if unicodedata.category(c) != 'Mn')
    date_added = time.time()
    return Movie(title, year, director, format, actors, rating, duration, pic_url, date_added)

def getMovieList(location):
    ret = []
    if not os.path.exists(location + "movies.json"):
        return ret
    moviesFile = open(location + "movies.json", "r")
    movies = json.load(moviesFile)
    for movie in movies:
        ret.append(Movie(   movie["title"],
                            movie["year"],
                            movie["director"],
                            movie["format"],
                            movie["actors"],
                            movie["rating"],
                            movie["duration"],
                            movie["pic_url"],
                            movie["date_added"]))
    return ret

def saveMovieList(location, movieList):
    movies = []
    movieList.sort(key=lambda x: x.date_added)
    for movie in movieList:
        movies.append(  {"title": movie.title,
                         "year": movie.year,
                         "director": movie.director,
                         "format": movie.format,
                         "actors": movie.actors,
                         "rating": movie.rating,
                         "duration": movie.duration,
                         "pic_url": movie.pic_url,
                         "date_added": movie.date_added})
    moviesFile = open(location + "movies.json", "w")
    json.dump(movies, moviesFile, indent=4)
    moviesFile.close()