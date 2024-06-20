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
  # LOAD DATA
  # dataSet3 = open('./datasource/masterListMovies.json')
  # dataSet2 = open('./datasource/movies.json')
  # dataJson3 = json.load(dataSet3)
  # dataJson2 = json.load(dataSet2)


  # DATASET 1
  # for val in dataJson3:
  #   seedGenreTable(val['genre'])
  #   seedDirectorTable(val['director'])
  #   seedActorTable(val['actors'])
  #   seedCountryTable(val['country'])
  #   seedWriterTable(val['writer'], 1)
  #   seedLanguageTable(val['language'])
  # print(seedMovieTable2(dataJson3))
   
  # seedMovieTable2(dataJson3)
  # seedManyToManyTables(dataJson3)
  # res = awards(dataJson3)
  # seedMovieAwardTable(res)

  # DATASET 2
  # for val in dataJson2:
    # seedGenreTable(val['genre'])
    # seedDirectorTable(val['director'])
    # seedActorTable(val['star'])
    # seedCountryTable(val['country'])
    # seedWriterTable(val['writer'], 2)
    # seedCompanyTable(val['company'])

  # seedMovieTable(dataJson2)
  # seedManyToManyTables(dataJson2)
 
  # =========================================================
  # PLOT GENRES
  res = getGenreTrendSvc()

  # Extract years
  years = [int(d['year']) for d in res]

  # Extract genres
  genres = list(res[0].keys())[1:]

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
  # plt.show()

  # =========================================================
  # GROSS TREND 3 GENRES (Biography, Action, Crime)
  res1 = getGrossTrendByGenreSvc()

  # Extracting data for plotting
  genres = [entry['genre'] for entry in res1]
  averages_millions = [entry['average'] / 1000000 for entry in res1]  # Scaling to millions of dollars

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
  # plt.show()

  # =========================================================
  # PLOT DIRECTOR
  res3 = getMoviesByDirectorSvc()

  directors = [entry['director'] for entry in res3]
  averages = [entry['average'] for entry in res3]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(directors, averages, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Directors')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # =========================================================
  res4 = getMoviesByActorSvc()

  actors = [entry['actor'] for entry in res4]
  averageVal = [entry['average'] for entry in res4]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(actors, averageVal, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Actors')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # ========================================================
  res5 = getMoviesByWriterSvc()
  # print(res5)

  writers = [entry['writer'] for entry in res5]
  averageVal1 = [entry['average'] for entry in res5]

  # Plotting
  plt.figure(figsize=(12, 8))  # Optional: adjust figure size
  plt.barh(writers, averageVal1, color='skyblue')
  plt.xlabel('Average Score')
  plt.title('Average Scores of Writers')
  plt.gca().invert_yaxis()  # Invert y-axis to have highest score at the top
  plt.tight_layout()  # Optional: adjust layout
  # plt.show()

  # =========================================================
  res6 = getMovieByRuntimeAndScoreSvc()

  ratings = [entry[1] for entry in res6]
  durations = [entry[2] for entry in res6]

  # # Plotting the scatter plot
  # plt.figure(figsize=(10, 6))  # Optional: set the figure size

  # plt.scatter(ratings, durations, marker='o', c='blue', edgecolors='black', s=100)

  # # Adding labels and title
  # plt.title('IMDb Ratings vs Durations of Movies')
  # plt.xlabel('IMDb Ratings')
  # plt.ylabel('Duration (minutes)')

  # # Adding movie names as annotations
  # for i, movie in enumerate(movies):
  #     plt.annotate(movie, (ratings[i], durations[i]), textcoords="offset points", xytext=(0,10), ha='center')

  # # Display the plot
  # plt.grid(True)
  # plt.tight_layout()
  # plt.show()
  # Plotting the scatter plot
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
