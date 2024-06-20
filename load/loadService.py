from load.loadRepo import (
    getCompanyOscarWinner,
    getGenreTrend,
    getGenreQuery,
    getGrossTrendByGenre,
    getMoviesByDirector,
    getMoviesByActors,
    getMoviesByWriters,
    getMoviesByRuntimeAndScore
)

def getGrossTrendByGenreSvc():
    topThreeGenre = ['Biography', 'Action', 'Crime']
    res = []
    for i in topThreeGenre:
        genre = i
        avgGross = 0
        entry = 0
        for year in range(2009, 2019):
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            resA = getGrossTrendByGenre(start_date, end_date, genre)
            for j in resA:
                title, releaseDate, gross, genres = j
                if gross == None:
                    continue
                avgGross += gross
                entry += 1
        average = float(avgGross) / float(entry)
        data = {
            "genre": genre,
            "average" : average
        }
        res.append(data)

    return res

def getGenreTrendSvc():
    resGenre = getGenreQuery()
    finalRes = []

    for year in range(2009, 2019):
        data = {
            "year": 0,
            "short": 0,
            "adventure": 0,
            "fantasy": 0,
            "action": 0,
            "crime": 0,
            "drama": 0,
            "history": 0,
            "war": 0,
            "romance": 0,
            "horror": 0,
            "mystery": 0,
            "thriller": 0,
            "documentary": 0,
            "comedy": 0,
            "family": 0,
            "western": 0,
            "animation": 0,
            "biography": 0,
            "music": 0,
            "musical": 0,
            "sci-fi": 0,
            "film-noir": 0,
            "sport": 0
        }
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        res = getGenreTrend(start_date, end_date)
        data['year'] = str(year)
        for i in res:
            title, score, release_date, genres = i
            for j in genres:
                for k in resGenre:
                    id, name = k
                    if name.lower() == j.lower():
                        data[f"{j.lower()}"] += 1
        finalRes.append(data)

    return finalRes

def getMoviesByDirectorSvc():
    res = getMoviesByDirector()
    resp = []
    response = []
    for val in res:
        dir, entry = val
        totalVal = 0
        totalEl = 0
        for ent in entry:
            totalVal += ent['score']
            totalEl += 1
        avg = totalVal / totalEl
        data = {
            "director": dir,
            "average": avg
        }
        resp.append(data)

    sorted_data = sorted(resp, key=lambda x: x['average'], reverse=True)
    for index, entry in enumerate(sorted_data[:21], start=1):
        if entry['director'] == 'Alejandro G. IÃ±Ã¡rritu':
            continue
        response.append(entry)

    return response

def getMoviesByActorSvc():
    res = getMoviesByActors()
    resp = []
    response = []
    for val in res:
        dir, entry = val
        totalVal = 0
        totalEl = 0
        for ent in entry:
            totalVal += ent['score']
            totalEl += 1
        avg = totalVal / totalEl
        data = {
            "actor": dir,
            "average": avg
        }
        resp.append(data)

    sorted_data = sorted(resp, key=lambda x: x['average'], reverse=True)
    for index, entry in enumerate(sorted_data[:21], start=1):
        response.append(entry)

    return response

def getMoviesByWriterSvc():
    res = getMoviesByWriters()
    resp = []
    response = []
    for val in res:
        dir, entry = val
        totalVal = 0
        totalEl = 0
        for ent in entry:
            totalVal += ent['score']
            totalEl += 1
        avg = totalVal / totalEl
        data = {
            "writer": dir,
            "average": avg
        }
        resp.append(data)

    sorted_data = sorted(resp, key=lambda x: x['average'], reverse=True)
    for index, entry in enumerate(sorted_data[:21], start=1):
        response.append(entry)

    return response

def getMovieByRuntimeAndScoreSvc():
    response = []
    res = getMoviesByRuntimeAndScore()

    for i in res:
        title, score, runtime = i
        if runtime == None:
            continue

        if title == 'Les vampires' or title == 'The Great Train Robbery' or title == 'Sherlock Jr.':
            continue

        response.append(i)

    return response