def read_file(pathname: str, year: int = 0) -> list:
    data = []
    file = open(pathname, mode='r', encoding='utf-8')
    file.readline()  # Skip header row
    for line in file:
        row = line.strip().split(';')
        if int(row[6]) >= year:
            data.append(row)
    file.close()
    return data

def top_n(data: list, genre: str = '', n: int = 0) -> list:
    filtered_data = []
    genres = genre.split(',') if genre else []

    # Filter by genre
    for movie in data:
        movie_genres = movie[2].split(',')
        if not genres or any(g in movie_genres for g in genres):
            filtered_data.append(movie)
    
    # Calculate Actor Rating and sort by Average Rating
    result = []
    for movie in filtered_data:
        title = movie[1]
        rating = float(movie[8])
        actors = movie[5].split(', ')
        
        # Compute actor_rating as the average of highest ratings per actor
        actor_ratings = []
        for actor in actors:
            actor_highest_rating = 0
            for m in data:
                if actor in m[5] and float(m[8]) > actor_highest_rating:
                    actor_highest_rating = float(m[8])
            actor_ratings.append(actor_highest_rating)
        actor_rating = sum(actor_ratings) / len(actor_ratings) if actor_ratings else 0

        # Compute Average Rating and add to result list
        average_rating = (rating + actor_rating) / 2
        result.append((title, average_rating))

    # Sort result by Average Rating (descending) and then Title (ascending) without lambda
    for i in range(len(result) - 1):
        for j in range(i + 1, len(result)):
            if result[i][1] < result[j][1] or (result[i][1] == result[j][1] and result[i][0] > result[j][0]):
                result[i], result[j] = result[j], result[i]
    
    # Return top n or all if n == 0
    return result[:n] if n > 0 else result

def write_file(top: list, file_name: str):
    file = open(file_name, mode='w', encoding='utf-8')
    for title, rating in top:
        file.write(f"{title}, {rating:.2f}\n")
    file.close()

def test():
    """Function for testing ai code"""
    assert read_file('films.csv', 2014)[:2] == [['1', 'Guardians of the Galaxy',
'Action,Adventure,Sci-Fi', 'A group of intergalactic criminals are forced to work together \
to stop a fanatical warrior from taking control of the universe.', 'James Gunn', 'Chris Pratt, \
Vin Diesel, Bradley Cooper, Zoe Saldana', '2014', '121', '8.1', '757074', '333.13', '76.0'],
['3', 'Split', 'Horror,Thriller', 'Three girls are kidnapped by a man with a diagnosed 23 \
distinct personalities. They must try to escape before the apparent emergence of a \
frightful new 24th.', 'M. Night Shyamalan', 'James McAvoy, Anya Taylor-Joy, Haley Lu Richardson, \
Jessica Sula', '2016', '117', '7.3', '157606', '138.12', '62.0']]
    print('Test 1: Passed')
    assert top_n(read_file('films.csv', 2014), genre='Action', n=5) == [('Dangal', 8.8),
('Bahubali: The Beginning', 8.3), ('Guardians of the Galaxy', 8.1),
('Mad Max: Fury Road', 8.1), ('Star Wars: Episode VII - The Force Awakens', 8.1)]
    print('Test 2: Passed')

test()
