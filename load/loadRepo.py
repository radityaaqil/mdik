import psycopg2
from database.config import dbCredential

def getCompanyOscarWinner():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT c.name AS company_name, SUM(ma.count) AS total_awards
                    FROM movie m
                    JOIN company c ON c.id = m.company_id
                    JOIN movie_award ma ON ma.movie_id = m.id
                    JOIN award a ON a.id = ma.award_id
                    WHERE a.name = 'OSCAR_WINNER'
                    GROUP BY c.name
                    ORDER BY total_awards DESC
                    LIMIT 10;
                """)
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getGenreTrend(startDate, endDate):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        m.title, 
                        m.score, 
                        m.release_date, 
                        ARRAY_AGG(g.name) AS genres
                    FROM 
                        movie m
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    WHERE 
                        m.release_date between %s and %s
                    GROUP BY 
                        m.title, m.score, m.release_date
                    ORDER BY 
                        m.score desc;
                """, (startDate, endDate))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getGenreQuery():
    try:
        # Establish the database connection using a context manager
        with psycopg2.connect(dbCredential) as conn:
            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                # Execute the command to seed the genre table
                cur.execute("SELECT id, name FROM genre")
                rows = cur.fetchall()

                # Commit the changes to the database
                conn.commit()

    except psycopg2.Error as error:
        # Rollback the transaction in case of error
        conn.rollback()
        print("Error occurred:", error)

    finally:
        # Close the database connection
        conn.close()
        return rows
    
def getGrossTrendByGenre(startDate, endDate, genre):
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        m.title,  
                        m.release_date, 
                        m.gross,
                        ARRAY_AGG(g.name) AS genres
                    FROM 
                        movie m
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    WHERE 
                        m.release_date between %s and %s and g.name in (%s)
                    GROUP BY 
                        m.title, m.release_date, m.gross
                    ORDER BY 
                        m.gross desc;
                """, (startDate, endDate, genre))
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getMoviesByDirector():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        d.name AS director,
                        ARRAY_AGG(
                            JSON_BUILD_OBJECT(
                                'title', m.title,
                                'release_date', m.release_date,
                                'score', m.score,
                                'genre', g.name
                            )
                        ) AS movies
                    FROM 
                        movie m
                    JOIN 
                        movie_director md ON md.movie_id = m.id 
                    JOIN 
                        director d ON d.id = md.director_id
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    WHERE 
                        g.name = 'Action'
                        AND m.release_date BETWEEN '2009-01-01' AND '2019-12-31'
                    GROUP BY 
                        d.name
                    ORDER BY 
                        AVG(m.score) DESC;
                """)
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getMoviesByActors():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        a.name AS actor,
                        ARRAY_AGG(
                            JSON_BUILD_OBJECT(
                                'title', m.title,
                                'release_date', m.release_date,
                                'score', m.score,
                                'genre', g.name
                            )
                        ) AS movies
                    FROM 
                        movie m
                    JOIN 
                        movie_actor ma ON ma.movie_id = m.id 
                    JOIN 
                        actor a ON a.id = ma.actor_id
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    WHERE 
                        g.name = 'Action'
                        AND m.release_date BETWEEN '2009-01-01' AND '2019-12-31'
                    GROUP BY 
                        a.name
                    ORDER BY 
                        AVG(m.score) DESC;
                """)
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getMoviesByWriters():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        w.name AS writer,
                        ARRAY_AGG(
                            JSON_BUILD_OBJECT(
                                'title', m.title,
                                'release_date', m.release_date,
                                'score', m.score,
                                'genre', g.name
                            )
                        ) AS movies
                    FROM 
                        movie m
                    JOIN 
                        movie_writer mw ON mw.movie_id = m.id 
                    JOIN 
                        writer w ON w.id = mw.writer_id
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    WHERE 
                        g.name = 'Action'
                        AND m.release_date BETWEEN '2009-01-01' AND '2019-12-31'
                    GROUP BY 
                        w.name
                    ORDER BY 
                        AVG(m.score) DESC
                """)
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows
    
def getMoviesByRuntimeAndScore():
    try:
        with psycopg2.connect(dbCredential) as conn:
            with conn.cursor() as cur:
                # Query
                cur.execute("""
                    SELECT 
                        m.title, 
                        m.score,
                        m.runtime
                    FROM 
                        movie m
                    JOIN 
                        movie_genre mg ON mg.movie_id = m.id 
                    JOIN 
                        genre g ON g.id = mg.genre_id
                    where 
                        g.name in ('Action')
                    GROUP BY 
                        m.title, m.score, m.runtime
                    ORDER BY 
                        m.score desc
                    offset 1;
                """)
                rows = cur.fetchall()

                conn.commit()

    except psycopg2.Error as error:
        conn.rollback()
        print("Error occurred:", error)

    finally:
        conn.close()
        return rows