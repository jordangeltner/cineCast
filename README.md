Northwestern University
Date: December 4, 2013
Course: EECS 338 - Practicum in Intelligent Information Systems

Project: CineCast
Team: Joseph Diebold, Jordan Geltner, Dane Stier
Description: The goal of CineCast is to develop a web application capable of providing and analyzing financial information of past, current, and upcoming films. This includes projecting film revenues and explaining the major factors which ultimately did or will contribute to a movie's success or failure. 

cineCast.zip:
  -all the html files for the website
  -all the javascript
  -all the css
  -contains some earlier iterations of the site
  
downloadedMovieData.zip:
  -contains .csv files for many different types of queries harvested from opusData
  -contains "selectedOpusDataFields.rtf" which states the fields we considered important
  
queries.txt:
  -a query into the OpusData Explorer that gets many important features for prediction from movies
  -budget is positive and box office is positive and the top 3 actors
  
newqueries.txt:
  -an updated version of queries.txt with a few different features selected
  
cineCast.mp4:
  -a screen cast for the lazy of you who don't want to have to click links yourself
  

Both files were written using Python 2.7 for its flexibility in easily parsing data and creating nested arrays. It was written for Mac but should be accessible from any machine type. 

The "utilities.py" file is a module for "CineCastFinal.py", which is the primary code; it includes a few commonly needed functions that do not need to be stored within a Class structure. 

Alternatively, all of the code in "CineCastFinal.py" is written around a Class structure, which is done to ensure quick access to the data continuously without sending thousands of entries of data into every function needed; instead everything is locally accessible. 

The Class "CineCast_Explain" initializes by importing data from 2 csv files: "sincity.csv" and "zookeeper.csv" (named after the last films included in each file). These files were exported from OpusData, which is the source of the data provided by the-numbers.com. The initialization process first stores each row in the csv files in a temporary array, and then calls another function to organize the data from there. This process is more thoroughly detailed within the code itself.

The main function of "CineCast_Explain" is "predict", which takes a film title as argument. From this title, the program goes through all of the other functions as needed, first finding the film entry in the data, and then composing 3 important lists as it calls each function: positive factors, negative factors, and revenue tiers. The last mostly corresponds to the tiers (1 - 11) of film success for each category, such as actor trends, director trends, etc. After all are added, the most common value becomes the predicted value of success. (So if most of the aspects of a particular film tend to gross in the 4th tier, $150,000,000 - $200,000,000, then the input film is also projected to earn that value.) 

The positive factors and negative factors arrays are appended as the function goes based on a variety of criteria, all described in further detail within the code. The information added is formatted so as to accommodate bar graphs used in the CineCast web application. The return value of the "predict" function is an array of the following: the movie entry, the projected revenue tier, the positive factors array, and the negative factors array.
