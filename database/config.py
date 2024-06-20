import psycopg2

dbCredential = "dbname=mdik user=postgres password=12345 port=5433 host=localhost"
createTableQuery = """
CREATE TABLE actor (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE genre (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE director (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE writer (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE company (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE country (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE award (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE language (
    id bigserial NOT NULL,
    name varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE movie (
    id bigserial NOT NULL,
    title varchar(100),
    score float,
    votes float,
    company_id int,
    budget float,
    gross float,
    rating varchar(15),
    runtime float,
    release_date date,
    PRIMARY KEY (id),
    FOREIGN KEY(company_id) references company(id)
);

CREATE TABLE movie_award (
    id bigserial NOT NULL,
    movie_id int,
    award_id int,
    count int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (award_id) references award(id)
);

CREATE TABLE movie_genre (
    id bigserial NOT NULL,
    movie_id int,
    genre_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (genre_id) references genre(id)
);

CREATE TABLE movie_actor (
    id bigserial NOT NULL,
    movie_id int,
    actor_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (actor_id) references actor(id)
);

CREATE TABLE movie_director (
    id bigserial NOT NULL,
    movie_id int,
    director_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (director_id) references director(id)
);

CREATE TABLE movie_writer (
    id bigserial NOT NULL,
    movie_id int,
    writer_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (writer_id) references writer(id)
);

CREATE TABLE movie_country (
    id bigserial NOT NULL,
    movie_id int,
    country_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (country_id) references country(id)
);

CREATE TABLE movie_language (
    id bigserial NOT NULL,
    movie_id int,
    language_id int,
    PRIMARY KEY(id),
    FOREIGN KEY (movie_id) references movie(id),
    FOREIGN KEY (language_id) references language(id)
);
"""

seedAwardTableQuery = """
    INSERT INTO award (name) VALUES('OSCAR WINNER');
    INSERT INTO award (name) VALUES('FESTIVAL WINNER');
    INSERT INTO award (name) VALUES('OSCAR NOMINATION');
    INSERT INTO award (name) VALUES('FESTIVAL NOMINATION');
"""

dropTableQuery = """
    DROP TABLE movie_award, movie, actor, director, writer, company, genre, country, award;
"""

def dropTables():
    with psycopg2.connect(dbCredential) as conn:
      with conn.cursor() as cur:
          cur.execute(dropTableQuery)
          conn.commit()
        

def createTables():
    with psycopg2.connect(dbCredential) as conn:
      with conn.cursor() as cur:
          cur.execute(createTableQuery)
          conn.commit()

def seedAwardTable():
    with psycopg2.connect(dbCredential) as conn:
      with conn.cursor() as cur:
          cur.execute(seedAwardTableQuery)
          conn.commit()