import re
from database.repo import (
    seedGenreTableQuery, 
    seedDirectorTableQuery, 
    seedActorTableQuery, 
    seedCompanyTableQuery, 
    seedCountryTableQuery, 
    seedWriterTableQuery, 
    seedLanguageTableQuery,
    getMovieTableQuery,
    insertMovieTableQuery,
    insertMovieTableQuery2,
    getCompanyQuery,
    getActorQuery,
    getCountryQuery,
    getDirectorQuery,
    getGenreQuery,
    getLanguageQuery,
    getWriterQuery,
    insertManyToMany,
    getActorQueryByActorIdMovieId,
    getGenreQueryByGenreIdMovieId,
    getDirectorQueryByDirectorIdMovieId,
    getCountryQueryByCountryIdMovieId,
    getWriterQueryByWriterIdMovieId,
    getAwardQuery,
    insertMovieAward
)
from datetime import datetime , timedelta 
from extract.helper import parseDate, awards
import random

# GENRE
def seedGenreTable(genreData):
    # In case of multiple genres, split into array
    genres = genreData.split(', ')
    for i in genres:
        seedGenreTableQuery(i)

# DIRECTOR
def seedDirectorTable(directorData):
     # In case of multiple directors, split into array
    directors = directorData.split(', ')
    for i in directors:
        seedDirectorTableQuery(i)

# ACTOR
def seedActorTable(actorData):
    # In case of multiple actors, split into array
    actors = actorData.split(', ')
    for i in actors:
        seedActorTableQuery(i)

# COMPANY
def seedCompanyTable(companyData):
    # In case of multiple companies, split into array
    # companies = companyData.split(', ')
    # for i in companies:
    seedCompanyTableQuery(companyData)

# COUNTRY
def seedCountryTable(countryData):
    # In case of multiple countries, split into array
    countries = countryData.split(', ')
    for i in countries:
        seedCountryTableQuery(i)

# LANGUAGE
def seedLanguageTable(languageData):
    # In case of multiple countries, split into array
    languages = languageData.split(', ')
    for i in languages:
        seedLanguageTableQuery(i)

# WRITER
def seedWriterTable(writerData, dataType):
    if dataType == 1:
        # In case of multiple writers, split into array
        pattern = r"[A-Z][a-zA-Z.' ]+(?= \()"
        # Extracting the names
        writers = re.findall(pattern, writerData)
        for i in writers:
            seedWriterTableQuery(i)
    else:
        writers = writerData.split(', ')
        for i in writers:
            seedWriterTableQuery(i)

# MOVIES
def seedMovieTable(data):
    companies = getCompanyQuery()
    for val in data:
        # Check if the movie already exist
        existingMovie = getMovieTableQuery(val['name'])
        if len(existingMovie) > 0:
            continue

        # Prepare and insert data
        # format release date
        parsedDate = parseDate(val['released'])
        val['released'] = parsedDate

        # determine company
        for company in companies:
            id, name = company
            if val['company'].lower() == name.lower():
                val['company_id'] = id
                insertMovieTableQuery(val) 
                break

def seedMovieTable2(data):
    for val in data:
        # Check if the movie already exist
        existingMovie = getMovieTableQuery(val['title'])
        if len(existingMovie) > 0:
            continue

        # Parse date
        # Extract year and released date
        year = val['year']
        released = val['released']
        # Parse the released date
        if released == "":
            random_month = random.randint(1, 12)  # Random month from 1 to 12
            days_in_month = (datetime(year, random_month % 12 + 1, 1) - timedelta(days=1)).day
            random_day = random.randint(1, days_in_month)  # Random day within the month

            # Create a datetime object with the random date
            random_date = datetime(year, random_month, random_day)
            val['released'] = random_date
            print(random_date)
        else:
            parsedReleased = datetime.strptime(released, '%d-%b-%y')
            # Correct the year if necessary (assume dates like 21-Apr-24 correspond to 21-Apr-1924)
            parsedReleased = parsedReleased.replace(year=year)
            # Convert to string in YYYY-MM-DD format for PostgreSQL
            releaseDateStr = parsedReleased.strftime('%Y-%m-%d')
            val['released'] = releaseDateStr
            print(releaseDateStr)

        # Parse runtime
        runtime = val['runtime']
        numericPart = runtime.split()[0]
        runtimeInMinutes = int(numericPart)
        val['runtime'] = runtimeInMinutes

        # Parse votes
        votes = str(val['imdb_votes'])
        votesWithoutCommas = votes.replace(',', '')
        intVotes = int(votesWithoutCommas)
        val['imdb_votes'] = intVotes

        # Insert Data
        print(val['title'])
        insertMovieTableQuery2(val)


def seedManyToManyTables(data):
    existingActors = getActorQuery()
    existingDirectors = getDirectorQuery()
    existingWriters = getWriterQuery()
    existingCountries = getCountryQuery()
    existingGenres = getGenreQuery()
    existingLanguages = getLanguageQuery()
    
    for val in data:
        # Get movie id
        print(val['title'])
        # movie = getMovieTableQuery(val['name'])
        movie = getMovieTableQuery(val['title'])
        print(movie)
        movID, movTitle = movie[0]

        # Actors
        actors = val['actors'].split(', ')
        actorTableName = 'movie_actor'
        for act in actors:
            match = 0
            for existingAct in existingActors:
                if match == len(actors):
                    break

                id, name = existingAct
                if act == name:
                    data = {
                        "movie_id": movID,
                        "actor_id": id
                    }

                    check = getActorQueryByActorIdMovieId(id, movID)
                    if len(check) > 0:
                        continue
                    else:
                        insertManyToMany(actorTableName, data)
                    match += 1

        # Genres
        genres = val['genre'].split(', ')
        genreTableName = 'movie_genre'
        for gen in genres:
            match = 0
            for existingGen in existingGenres:
                if match == len(genres):
                    break

                id, name = existingGen
                if gen == name:
                    data = {
                        "movie_id": movID,
                        "genre_id": id
                    }
                    check = getGenreQueryByGenreIdMovieId(id, movID)
                    if len(check) > 0:
                        continue
                    else:
                        insertManyToMany(genreTableName, data)
                    match += 1

        # Country
        countries = val['country'].split(', ')
        countryTableName = 'movie_country'
        for coun in countries:
            match = 0
            for existingCount in existingCountries:
                if match == len(countries):
                    break

                id, name = existingCount
                if coun == name:
                    data = {
                        "movie_id": movID,
                        "country_id": id
                    }
                    check = getCountryQueryByCountryIdMovieId(id, movID)
                    if len(check) > 0:
                        continue
                    else:
                        insertManyToMany(countryTableName, data)
                    match += 1

        # Director
        directors = val['director'].split(', ')
        directorTableName = 'movie_director'
        for dir in directors:
            match = 0
            for existingDir in existingDirectors:
                if match == len(directors):
                    break

                id, name = existingDir
                if dir == name:
                    data = {
                        "movie_id": movID,
                        "director_id": id
                    }
                    check = getDirectorQueryByDirectorIdMovieId(id, movID)
                    if len(check) > 0:
                        continue
                    else:
                        insertManyToMany(directorTableName, data)
                    match += 1

        # Writer
        # Data json2
        # writers = val['writer'].split(', ')
        # Data json3
        # In case of multiple writers, split into array
        pattern = r"[A-Z][a-zA-Z.' ]+(?= \()"
        # # Extracting the names
        writers = re.findall(pattern, val['writer'])
        writerTableName = 'movie_writer'
        for wri in writers:
            match = 0
            for existingWri in existingWriters:
                if match == len(writers):
                    break

                id, name = existingWri
                if wri == name:
                    data = {
                        "movie_id": movID,
                        "writer_id": id
                    }
                    check = getWriterQueryByWriterIdMovieId(id, movID)
                    if len(check) > 0:
                        continue
                    else:
                        insertManyToMany(writerTableName, data)
                    match += 1

        # Language
        languages = val['language'].split(', ')
        languageTableName = 'movie_language'
        for lang in languages:
            match = 0
            for existingLang in existingLanguages:
                if match == len(languages):
                    break

                id, name = existingLang
                if lang == name:
                    data = {
                        "movie_id": movID,
                        "language_id": id
                    }
                    insertManyToMany(languageTableName, data)
                    match += 1

def seedMovieAwardTable(resAwards):
    existingAwards = getAwardQuery()

    for aw in resAwards:
        movie = getMovieTableQuery(aw['title'])
        movID, movTitle = movie[0]
        print(aw)
        for key, value in aw.items():
            if isinstance(value, int) and value > 0:
                data = {
                    "movie_id": movID,
                    "award_id": "",
                    "count": value,
                }
                
                for existingAw in existingAwards:
                    awID, awName = existingAw
                    if key == awName.lower():
                        data['award_id'] = awID
                        print(data)
                        insertMovieAward(data)
                        break
                    
            elif isinstance(value, str):
                try:
                    int_value = int(value)
                    if int_value > 0:
                        data = {
                        "movie_id": movID,
                        "award_id": "",
                        "count": value,
                        }
                    
                        for existingAw in existingAwards:
                            awID, awName = existingAw
                            if key == awName.lower():
                                data['award_id'] = awID
                                print(data)
                                insertMovieAward(data)
                                break
                except ValueError:
                    continue
