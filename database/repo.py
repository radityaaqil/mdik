import psycopg2
from database.config import dbCredential

# GENRE TABLE
def seedGenreTableQuery(genre):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query genre table
                cur.execute("SELECT name FROM genre where LOWER(name) = LOWER(%s)", (genre,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO genre (name) VALUES(%s)", (genre,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# DIRECTOR TABLE
def seedDirectorTableQuery(director):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query director table
                cur.execute("SELECT name FROM director where LOWER(name) = LOWER(%s)", (director,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO director (name) VALUES(%s)", (director,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# COUNTRY TABLE
def seedCountryTableQuery(country):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query country table
                cur.execute("SELECT name FROM country where LOWER(name) = LOWER(%s)", (country,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO country (name) VALUES(%s)", (country,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# COMPANY TABLE
def seedCompanyTableQuery(company):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query company table
                cur.execute("SELECT name FROM company where LOWER(name) = LOWER(%s)", (company,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO company (name) VALUES(%s)", (company,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# WRITER TABLE
def seedWriterTableQuery(writer):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query writer table
                cur.execute("SELECT name FROM writer where LOWER(name) = LOWER(%s)", (writer,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO writer (name) VALUES(%s)", (writer,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# ACTOR TABLE
def seedActorTableQuery(actor):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query actor table
                cur.execute("SELECT name FROM actor where LOWER(name) = LOWER(%s)", (actor,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO actor (name) VALUES(%s)", (actor,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# LANGUAGE TABLE
def seedLanguageTableQuery(language):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query language table
                cur.execute("SELECT name FROM language where LOWER(name) = LOWER(%s)", (language,))
                rows = cur.fetchall()
            
                if len(rows) == 0:
                   cur.execute("INSERT INTO language (name) VALUES(%s)", (language,))

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# MOVIE TABLE
def getMovieTableQuery(title):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie table
                cur.execute("SELECT id, title FROM movie where LOWER(title) = LOWER(%s)", (str(title),))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def insertMovieTableQuery(data):
    # Check empty data
    for key in data:
        if data[key] == '':
            data[key] = None
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie table
                cur.execute("""
                    INSERT INTO movie(
                            title,
                            score,
                            votes,
                            company_id,
                            budget,
                            gross,
                            release_date,
                            rating,
                            runtime
                    ) VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                    )
                """,(
                        data['name'],
                        data['score'],
                        data['votes'],
                        data['company_id'],
                        data['budget'],
                        data['gross'],
                        data['released'],
                        data['rating'],
                        data['runtime']
                    )
                )
               
                conn.commit()
    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

def insertMovieTableQuery2(data):
    # Check empty data
    for key in data:
        if data[key] == '':
            data[key] = None
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie table
                cur.execute("""
                    INSERT INTO movie(
                            title,
                            score,
                            votes,
                            rating,
                            runtime,
                            release_date
                    ) VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                    )
                """,(
                        data['title'],
                        data['imdb_rating'],
                        data['imdb_votes'],
                        data['rated'],
                        data['runtime'],
                        data['released']
                    )
                )
               
                 # data['title'],
                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

# GET COMPANIES
def getCompanyQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie table
                cur.execute("SELECT id, name FROM company")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET ACTORS
def getActorQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query actor table
                cur.execute("SELECT id, name FROM actor")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# Get Actor by name
def getActorQueryByActorIdMovieId(actorId, movieId):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query actor table
                cur.execute("SELECT id FROM movie_actor where actor_id = %s AND movie_id = %s", (actorId, movieId))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET Country
def getCountryQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query country table
                cur.execute("SELECT id, name FROM country")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getCountryQueryByCountryIdMovieId(countryId, movieId):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query country table
                cur.execute("SELECT id FROM movie_country where country_id = %s AND movie_id = %s", (countryId, movieId))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET GENRE
def getGenreQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query genre table
                cur.execute("SELECT id, name FROM genre")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getGenreQueryByGenreIdMovieId(genreId, movieId):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query genre table
                cur.execute("SELECT id FROM movie_genre where genre_id = %s AND movie_id = %s", (genreId, movieId))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET WRITER
def getWriterQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query writer table
                cur.execute("SELECT id, name FROM writer")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getWriterQueryByWriterIdMovieId(writerId, movieId):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query writer table
                cur.execute("SELECT id FROM movie_writer where writer_id = %s AND movie_id = %s", (writerId, movieId))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET LANGUAGE
def getLanguageQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query language table
                cur.execute("SELECT id, name FROM language")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
# GET DIRECTOR
def getDirectorQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query director table
                cur.execute("SELECT id, name FROM director")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows

def getDirectorQueryByDirectorIdMovieId(directorId, movieId):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query director table
                cur.execute("SELECT id FROM movie_director where director_id = %s AND movie_id = %s", (directorId, movieId))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    

def insertManyToMany(tableName, data):
    colName = tableName.split('_')[1]
    preparedQuery = f"INSERT INTO {tableName}(movie_id, {colName}_id) VALUES (%s, %s)"
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie table
                cur.execute(preparedQuery, (data['movie_id'], data[f"{colName}_id"]))
               
                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

def insertMovieAward(data):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query movie_award table
                cur.execute("""
                   INSERT INTO movie_award(
                        movie_id,
                        award_id,
                        count
                   ) VALUES (
                        %s,
                        %s,
                        %s 
                   )
                """, (
                    data['movie_id'],
                    data['award_id'],
                    data['count']
                ))
               
                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()

def getAwardQuery():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Execute the command to get the award table
                cur.execute("SELECT id, name FROM award")
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows