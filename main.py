def read_file(pathname: str, year: int=0) -> list:
    """
    Reads file and returns all items with specified year in file as a list
    Args:
        pathname (str): path to the file with movies
        year (int, optional): starting with the particular year. Defaults to 0.

    Returns:
        list: information about movies

    >>> read_file('films.csv', 2014)[:2]
    [['1', 'Guardians of the Galaxy', \
'Action,Adventure,Sci-Fi', 'A group of intergalactic criminals are forced to work together \
to stop a fanatical warrior from taking control of the universe.', 'James Gunn', 'Chris Pratt, \
Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1', '757074', '333.13', '76.0'], \
['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a diagnosed 23 \
distinct personalities. They must try to escape before the apparent emergence of a \
frightful new 24th.', 'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, \
Jessica Sula', '2016', '117', '7.3', '157606', '138.12', '62.0']]
    """
    with open(pathname, 'r', encoding='utf-8') as my_file:
        content = my_file.readlines()
        movies = []
        for line in content[1:]:
            data = line.strip().split(';')
            movie_year = int(data[6])
            if movie_year >= year: 
                movies.append(data)
    return movies


def top_n(data: list, genre: str='', n:int=0) ->list[tuple]:
    """
    For each movie in data, with genre given by genre, this function calculates a new rating,
    actor_rating, as follows: for each actor appearing in the movie, finds the highest rating
    of any movie (regardless of genre) in which the actor appears; then it finds the new
    actor_rating as the arithmetic mean (average) of all these ratings for all actors in
    the movie. The function then generates a list of tuples containing three fields:
    (Title, Rating, Actors_Rating), sorts the list of tuples in descending order based on
    the average of Rating and Actors_Rating (tuples with the same averaged rating should be
    ordered lexicographically), and returns the n first movies with the highest value as tuples
    (Title, Average_rating). If n = 0, the entire list of available movies is displayed.
    If genre = '', all movies are selected regardless of genre. The genre parameter can also
    contain several genres listed separated by commas (for example, "Sci-Fi,Adventure").
    In this case, the search is performed within any of the specified genres (i.e., interpret
    the comma as an 'or' operator).
    Args:
        data (list): a list of movie lists (as an output of the read_file function)
        genre (str, optional):  a movie genre. Defaults to ''.
        n (int, optional): number of elements to return. Defaults to 0.

    Returns:
        list[tuple]: n first movies with the highest value as tuples
    >>> top_n(read_file('films.csv', 2014), genre='Action', n=5)
    [('Dangal', 8.8), ('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1), \
('Mad Max: Fury Road', 8.1), ('Star Wars: Episode VII - The Force Awakens', 8.1)]
    """
    outcome = []
    for el in data:
        if genre in el[2]:
            actors = el[5].split(', ')
            result = {}
            for actor in actors:
                result[actor] = max(float(el[8]) for el in data if actor in el[5])
            avg_rating = sum(list(result.values()))/len(list(result.values()))
            avg_rating = float(f'{avg_rating:.1f}')
            outcome.append((el[1], float(el[8]), avg_rating))
    def some_func(outcome):
        return (outcome[2] + outcome[1])/2
    outcome = sorted(outcome)
    outcome = sorted(outcome, key=some_func, reverse=True)
    result = [(el[0], el[2]) for el in outcome]
    return result[:n]

def write_file(top: list, file_name: str):
    """
    Function writes movies into file. The function should write each tuple (Title, rating) 
    on a separate line. For example: Intern, 8.5
    Args:
        top (list): the list top generated by the previous function
        file_name (str):  the name of the file file_name to write this information to
    """
    with open(file_name, 'w+', encoding='utf-8') as file:
        for tup in top:
            tup = [str(el) for el in tup]
            file.write(', '.join(tup) + '\n')


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())