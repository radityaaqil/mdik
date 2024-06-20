import json
from extract.service import (
  seedGenreTable, 
  seedDirectorTable, 
  seedActorTable, 
  seedCompanyTable, 
  seedCountryTable, 
  seedWriterTable, 
  seedLanguageTable,
  seedMovieTable,
  seedManyToManyTables,
  seedMovieTable2,
  seedMovieAwardTable,
)
from database.config import createTables, seedAwardTable   
from extract.helper import awards
from datetime import datetime  
import re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from load.loadService import (
    getGenreTrendSvc,
    getGrossTrendByGenreSvc,
    getMoviesByDirectorSvc,
    getMoviesByActorSvc,
    getMoviesByWriterSvc,
    getMovieByRuntimeAndScoreSvc
)

def main():
  # EXTRACT AND TRANSFORM
  dataSet3 = open('./datasource/masterListMovies.json')
  dataSet2 = open('./datasource/movies.json')
  dataJson3 = json.load(dataSet3)
  dataJson2 = json.load(dataSet2)

  # DATASET 1
  for val in dataJson3:
    seedGenreTable(val['genre'])
    seedDirectorTable(val['director'])
    seedActorTable(val['actors'])
    seedCountryTable(val['country'])
    seedWriterTable(val['writer'], 1)
    seedLanguageTable(val['language'])
   
  seedMovieTable2(dataJson3)
  seedManyToManyTables(dataJson3)
  res = awards(dataJson3)
  seedMovieAwardTable(res)

  # DATASET 2
  for val in dataJson2:
    seedGenreTable(val['genre'])
    seedDirectorTable(val['director'])
    seedActorTable(val['star'])
    seedCountryTable(val['country'])
    seedWriterTable(val['writer'], 2)
    seedCompanyTable(val['company'])

  seedMovieTable(dataJson2)
  seedManyToManyTables(dataJson2)
 
  # ==================================================================================================================
  # LOAD

  # PLOT GENRES
  genreTrend = getGenreTrendSvc()

  # Extract years
  years = [int(d['year']) for d in genreTrend]

  # Extract genres
  genres = list(genreTrend[0].keys())[1:]

  # Prepare data for plotting
  genre_data = {genre: [] for genre in genres}
  for d in res:
      for genre in genres:
          genre_data[genre].append(d[genre])

  # Plot the data
  plt.figure(figsize=(14, 10))

  # Adding different line styles and markers
  line_styles = ['-', '--', '-.', ':']
  markers = ['o', 's', '^', 'D']

  for i, (genre, counts) in enumerate(genre_data.items()):
      plt.plot(years, counts, label=genre, linestyle=line_styles[i % len(line_styles)], marker=markers[i % len(markers)])

  plt.xlabel('Year', fontsize=14)
  plt.ylabel('Count', fontsize=14)
  plt.title('Genres per Year', fontsize=16)
  plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
  plt.grid(True)
  plt.tight_layout()

  # ==================================================================================================================
  # GROSS TREND 3 GENRES (Biography, Action, Crime)
  grossTrend = getGrossTrendByGenreSvc()

  # Extracting data for plotting
  genres = [entry['genre'] for entry in grossTrend]
  averages_millions = [entry['average'] / 1000000 for entry in grossTrend]  # Scaling to millions of dollars

  # Plotting the bar graph
  plt.figure(figsize=(10, 6))
  bars = plt.bar(genres, averages_millions, color=['skyblue', 'orange', 'green'])

  # Adding labels and title
  plt.xlabel('Genre')
  plt.ylabel('Average Box Office (Millions of $)')
  plt.title('Average Box Office by Genre')

  # Adding data labels on top of each bar
  for bar, avg in zip(bars, averages_millions):
      plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{avg:.1f}', ha='center', va='bottom', fontsize=10)

  # Display the plot
  plt.tight_layout()

  # ==================================================================================================================
  # PLOT DIRECTOR
  moviesByDirector = getMoviesByDirectorSvc()

  directors = [entry['director'] for entry in moviesByDirector]
  averages = [entry['average'] for entry in moviesByDirector]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(directors, averages, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Directors')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # ==================================================================================================================
  moviesByActors = getMoviesByActorSvc()

  actors = [entry['actor'] for entry in moviesByActors]
  averageVal = [entry['average'] for entry in moviesByActors]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(actors, averageVal, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Actors')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # ========================================================
  moviesByWriter = getMoviesByWriterSvc()

  writers = [entry['writer'] for entry in moviesByWriter]
  averageVal1 = [entry['average'] for entry in moviesByWriter]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(writers, averageVal1, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Writers')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # ==================================================================================================================
  movireByRuntimeAndScore = getMovieByRuntimeAndScoreSvc()

  ratings = [entry[1] for entry in movireByRuntimeAndScore]
  durations = [entry[2] for entry in movireByRuntimeAndScore]

  plt.figure(figsize=(10, 6))  # Optional: set the figure size
  plt.scatter(durations, ratings, marker='o', c='blue', edgecolors='black', s=100)

  # Adding labels and title
  plt.title('IMDb Ratings vs Durations of Movies')
  plt.xlabel('Duration (minutes)')
  plt.ylabel('IMDb Ratings')

  # Display the plot without legend and movie titles
  plt.grid(True)
  plt.tight_layout()
  plt.show()

main()
