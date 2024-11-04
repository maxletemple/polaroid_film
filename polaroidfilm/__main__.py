from movieList import *
from polaroid import *

movies_location = "work/"

def main():
    print("Welcome to the movie database!")
    movieList = getMovieList(movies_location)
    while True:
        print("1. Add movie")
        print("2. List movies")
        print("3. Modify movie")
        print("4. Delete movie")
        print("5. Export movie list to polaroid template")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            movie = createMovieInteractive()
            movie.date_added = time.time()
            movieList.append(movie)
            print("Movie added successfully!")
        elif choice == "2":
            for movie in movieList:
                print(movie)
        elif choice == "3":
            for i in range(len(movieList)):
                print(f"{i+1}. {movieList[i]}")
            choice = int(input("Enter movie number to modify: "))
            movieList[choice-1] = modifyMovieInteractive(movieList[choice-1])
        elif choice == "4":
            for i in range(len(movieList)):
                print(f"{i+1}. {movieList[i]}")
            choice = int(input("Enter movie number to delete: "))
            del movieList[choice-1]
        elif choice == "5":
            print("Exporting movie list to polaroid template...")
            exportMovieList(template_standard, movies_location, movieList)
        elif choice == "6":
            break
        else:
            print("Invalid choice")
        saveMovieList(movies_location, movieList)
    
    print("Goodbye!")

if __name__ == "__main__":
    main()