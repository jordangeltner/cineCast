
# Northwestern University
# Date: December 4, 2013
# Course: EECS 338 - Practicum in Intelligent Information Systems

# Project: CineCast
# Team: Joseph Diebold, Jordan Geltner, Dane Stier
# Description: The goal of CineCast is to develop a web application capable of
# providing and analyzing financial information of past, current, and upcoming 
# films. This includes projecting film revenues and explaining the major factors
# which ultimately did or will contribute to a movie's success or failure. 

# The code in this file imports and analyzes data from 2 csv files. These files 
# were exported from OpusData, the source of metadata from the-numbers.com. By 
# analyzing this data, the program returns the positive and negative factors of 
# success of each film in a format readily capable of being used for the charts
# available on CineCast's website.


# -*- coding: utf-8 -*-
import csv, utilities, os
from collections import Counter


class CineCast_Explain():
	#initialize the program by importing the information provided in the csv
	#files exported from the data source
	def __init__(self):
		self.data1 = [] #temporary placement of imported data
		self.data2 = [] #final placement of imported data

		#read data file and put data into self.data1
		loc = os.path.expanduser("~/CineCast Projection Algorithm")
		with open(loc +'/sincity.csv', 'rb') as csvfile:
			datafile = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			for row in datafile:
				if i!=0: #exclude the first row (headers) of the file
					self.data1.append(row)
				i+= 1

		with open('/Users/danestier/Desktop/CineCast/zookeeper.csv', 'rb') as csvfile:
			datafile = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			for row in datafile:
				if i!=0: #exclude the first row (headers) of the file
					self.data1.append(row)
				i+= 1

		#now that the data has been moved to an internal array, it needs to be
		#reorganized for more optimal use in this program
		self.org_data()

	#reorganize and reformat the data currently in self.data1
	def org_data(self):
		for film in self.data1:
			#all array entries are current strings, so some must be changed
			title = film[0]
			gross = int(film[1])
			budget = int(film[2])
			actor = film[3]
			billing = int(film[4]) #Order of highest billed actors. 
								   #Only <=3 are included (top three actors)
			character = film[5]
			director = film[6]
			genre = film[7]
			source = film[8] #screenplay vs book vs remake, etc.
			creative = film[9]
			method = film[10] #indicates live action vs digital animation
			sequel = int(film[11]) #binary, 1 if it is a sequel, 0 otherwise

			if film[12]:
				#date in format "year-mo-da"
				year = film[12][:4]
				month = film[12][5:7]
				day = film[12][8:]
				date = year+month+day #concatenation of the date format without
									  #the hyphens, which is useful for comparing
									  #when films were released
				release = [int(year), int(month), int(day), int(date)]

				#Most films in self.data1 have multiple entries, one for each of the top 3 actors
				#billed. If the current film being looked at is the same as the last one added
				#to self.data2, then the only thing that should be changed is the actor portion
				#of the new entry. The years of the film must also match to account for remakes.
				if self.data2 and title==self.data2[-1][0] and int(year)==self.data2[-1][4][0]:
					if billing==1: #if it is the top billed/lead actor
						self.data2[-1][2][0] = actor #put in lead actor slot
						self.data2[-1][2][2] = character #add character portrayed to main character slot
					self.data2[-1][2][1].append(actor) #actor added to list of the top actors in the film
					self.data2[-1][2][3].append(character) #character added to list of main characters
				else:
					#create a new entry for self.data2
					new_entry = [title, [gross, budget, utilities.find_range(gross)], [None, [actor], None, [character], director], [genre, source, creative, method, sequel], release]
					if billing==1: #if actor is the top billed/lead actor for that film
						new_entry[2][0] = actor #put in lead actor slot
						new_entry[2][2] = character #add character portrayed to main character slot
					self.data2.append(new_entry) #add the new entry to self.data2
		return


	#Determine the projected gross and primary factors of success/failure of a given film.
	def predict(self, title):
		#search for the film listed
		movie = self.find_film(title)

		pos_factors = [] #list of positive factors
		neg_factors = [] #list of negative factors

		final = [] #list of revenue tiers for each factors (i.e. actor trends, director trends, etc.)

		#if applicable categories
		latest = None #if an actor very recently had a successful film
		prequel = None #the prequel of the current film
		trilogy_boost = 0 #1 if the film is the end of a trilogy

		#find prequel of the film if applicable
		if movie[3][4]==1:
			#call function
			prequel = self.find_prequel(movie)
			#if a prequel is found
			if prequel:
				#if it was successful
				if prequel[0][1][0]>100000000:
					pos_factors.append(1)
					pos_factors.append("Successful Prequel")
					pos_factors.append("The success of " + movie[0] + " was boosted by the success of it's prequel, " + prequel[0][0] + ".")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
				#if it was not very successful
				if prequel[0][1][0]<50000000:
					neg_factors.append(1)
					neg_factors.append("Unsuccessful Prequel: " + prequel[0][0])
					neg_factors.append("Given the lack of success garnered by " + movie[0] + "'s prequel, " + prequel[0][0] + ", the film suffered from lowered expectations.")
					pos_factors.append(0)
					pos_factors.append("")
					pos_factors.append("")
				#if there is an indication that the current film is the end of a trilogy
				if (len(prequel[1])==2 or len(prequel[1])==5) or "III" in movie[0] or "VI" in movie[0] or "3:" in movie[0] or "6:" in movie[0] or "3"==movie[0][-1] or "6"==movie[0][-1]:
					pos_factors.append(0)
					pos_factors.append("End of Trilogy")
					pos_factors.append("As the end of a trilogy, " + movie[0] + " enjoyed higher audience anticipation, driving theater attendance.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
					trilogy_boost = 1
			
				#if it was a short duration since the release of the prequel, that's beneficial.
				if prequel[0][4][0]>movie[4][0]-3:
					pos_factors.append(1)
					pos_factors.append("Prequel Release")
					pos_factors.append("Given the short duration since the release of " + movie[0] + "'s prequel, the film could hold the attention and anticipation of its fans until its release.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
				#or if it was a long time, then it hurts the film.
				else:
					neg_factors.append(1)
					neg_factors.append("Prequel Release")
					neg_factors.append("In the long time span since the release of " + movie[0] + "'s prequel, the film lost steam and anticipation, thus having less theater attendance.")
					pos_factors.append(0)
					pos_factors.append("")
					pos_factors.append("")

		#find weekend stats by calling function
		weekend = self.weekrate(utilities.findweek(movie[4][0], movie[4][1], movie[4][2]), movie[1][1])
		if weekend: #if results were found
			final.append(weekend[0]) #add the first result to the list of revenue tiers
			if weekend[1]>=2.0: #if the average success ratio is high, it is noteworthy
				pos_factors.append(1)
				pos_factors.append("Release Timing")
				pos_factors.append("Theater attendances is usually higher during the time when this film was released, on " + str(movie[4][1]) + "-" + str(movie[4][2]) + "-" + str(movie[4][0]) + ".")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if weekend[1]<1.0: #if the average success ratio is very low, then it is also noteworthy
				neg_factors.append(1)
				neg_factors.append("Release Timing")
				neg_factors.append("Theater attendances is usually much lower during the time when this film was released, on " + str(movie[4][1]) + "-" + str(movie[4][2]) + "-" + str(movie[4][0]) + ".")
				pos_factors.append(0)
				pos_factors.append("")
				pos_factors.append("")
		
		#find actor stats by calling function
		actor = self.actor_trends(movie[2][0], movie)
		a = movie[2][0]
		if actor: #if results were found
			final.append(actor[0]) #add the first result to the list of revenue tiers
			#if the actor had a recent success in which he/she starred and it was an animated film and it was within the last 3 years, it is a boost
			if actor[2] and actor[2][2][0]>=150000000 and a==movie[2][0] and movie[3][3]!="Digital Animation" and actor[2][4][0]>=movie[4][0]-3:
				pos_factors.append(1)
				pos_factors.append("Recent Actor Success")
				pos_factors.append("This film received a boost in popularity from the recent success of " + a + " in " + actor[2][0] + ".")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")

				actor[0]+= 1 #boost the usual actor gross that was returned
			final.append(actor[0]) #add the value to the list of revenue tiers since the actor is an important factor
			if actor[1]>=2.0: #if the actor average success ratio is high, that is noteworthy
				pos_factors.append(1)
				pos_factors.append("Successful Actor Trends")
				pos_factors.append("In the recent years preceding this film, actor " + a + " had increasing popularity for a variety of successful roles, leading to higher attendance for this film.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
		 	if actor[1]<1.0 and a==movie[2][0]: #if the success ratio is low, that is also noteworthy
		 		neg_factors.append(1)
		 		neg_factors.append("Unsuccessful Actor Trends")
		 		neg_factors.append("In the recent years preceding this film, actor " + a + " had a decreasing reputation for holding numerous unsuccessful roles, leading to lower attendance for this film.")
		 		pos_factors.append(0)
				pos_factors.append("")
				pos_factors.append("")
			#check for actor partnerships
			for x in actor[3]:
				#but not for prequel/sequel films
		 		if prequel and not x[1] in prequel[1]:
					pos_factors.append(1)
					pos_factors.append("Actor Partnership")
					pos_factors.append(a + " and " + x[0] + " were popular for collaborating on numerous successful films, driving high audience expectations.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
			#same for directors
	 		for x in actor[4]:
	 			if prequel and not x[1] in prequel[1]:
	 				pos_factors.append(1)
	 				pos_factors.append("Popular Director Partnership with " + x[0])
	 				pos_factors.append(a + " has worked on numerous films with director " + x[0] + ", and the two became known for popular and successful films, leading to higher attendance for this film.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")

		#find director  by calling function
		director = self.director_trends(movie)
		if director: #if there are results
			final.append(director[0]) #the first result is added to the list of revenue tiers
			if director[1]>=3.0 or director[3]: #if the director has a very high average success ratio, it is noteworthy
				pos_factors.append(1)
				pos_factors.append("Director Quality")
				pos_factors.append("In the recent years preceding this film, " + movie[2][4] + " gained a reputation for directing high quality films, boosting attendance for " + movie[0] + ".")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if director[1]<1.0: #if the success ratio is very low, that is also noteworthy
				neg_factors.append(1)
				neg_factors.append("Director Quality")
				neg_factors.append("In the years before this films, " + movie[2][4] + " lacked a reputation for making high quality films, which discouraged audience members from attending.")
				pos_factors.append(0)
				pos_factors.append("")
				pos_factors.append("")
			#if the director's latest film was very successful but it was not the film's prequel, it is positive 
			if director[2][1][0]>=200000000 and prequel and director[2]!=prequel[0]:
				pos_factors.append(1)
				pos_factors.append("Recent Directoral Success: " + director[2][0])
				pos_factors.append(movie[0] + " received a significant boost from director " + movie[2][4] + "'s box office hit " + director[2][0])
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			latest = director[2]

		#find genre stats by calling function
		genre = self.genre_trends(movie)
		if genre: #if there are results
			final.append(genre[0]) #the first result is added to the list of revenue tiers
			if genre[1]>=3.0: #if the genre has a very high average success ratio, it is noteworthy
				pos_factors.append(1)
				pos_factors.append("Popular Genre")
				pos_factors.append("Before the release of " + movie[0] + ", " + movie[3][0] + " was a popular genre, which boosted the film's popularity.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if genre[1]<1.0: #if it has a very low average success ratio, it is also noteworthy
				neg_factors.append(1)
				neg_factors.append("Unpopular Genre: " + movie[3][0])
				neg_factors.append(movie[3][0] + " was not particularly popular in the time before " + movie[0] + "'s release, which hurt box office sales.")
				pos_factors.append(0)
				pos_factors.append("")
				pos_factors.append("")

		#find other stats by calling function. No "notes" necessary for output
		other = self.other_trends(movie)
		if other:
			final.append(other)

		#find similar movie by calling function
		similar = self.find_similar(movie)
		if similar:
			final.append(similar[1][2])

		#find competitors by calling function
		competitors = self.competition(movie)
		for film in competitors: #note all major competitors
			neg_factors.append(1)
			neg_factors.append("Competition")
			neg_factors.append("During " + movie[0] + "'s time in theaters, it suffered in ticket sales because of competition from the successful film " + film[0] + ", which was in theaters at the same time as " + movie[0] + ".")
			pos_factors.append(0)
			pos_factors.append("")
			pos_factors.append("")


		#Add other factors to positive/negative results. Some of these are less certain and added more as guesses for outcomes. It will be nice
		#to improve the accuracy of this section.
		if movie[1][0]>150000000:
			if movie[3][1]=="Based on Real Life Events":
				pos_factors.append(1)
				pos_factors.append("Real Life Event")
				pos_factors.append("Because " + movie[0] + " was based on a popular real life event, audience members were even more likely to attend.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if movie[3][1]=="Based on Fiction Book/Short Story":
				pos_factors.append(1)
				pos_factors.append("Based on Book")
				pos_factors.append("Because " + movie[0] + " was based on a popular book, avid fans helped spread anticipation and popularity of the film.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if movie[3][1]=="Based on Comic/Graphic Novel":
				if movie[3][2]=="Super Hero":
					pos_factors.append(1)
					pos_factors.append("Super Hero")
					pos_factors.append("Since " + movie[0] + " was an adapation of a popular Super Hero, fans of all ages filled the theaters.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
				else:
					pos_factors.append(1)
					pos_factors.append("Based on Novel")
					pos_factors.append("Because " + movie[0] + " was based on a popular book, avid fans helped spread anticipation and popularity of the film.")
					neg_factors.append(0)
					neg_factors.append("")
					neg_factors.append("")
			if movie[3][2]=="Kids Fiction" and movie[3][3]=="Digital Animation":
				pos_factors.append(1)
				pos_factors.append("Young Audience")
				pos_factors.append("Since " + movie[0] + " was created for a younger audience, both children and parents filled the theaters, driving ticket sales.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")
			if movie[3][3]=="Animation/Live Action":
				pos_factors.append(1)
				pos_factors.append("Animation")
				pos_factors.append("The high quality animation of " + movie[0] + " boosted attendance as people flocked to see the stunning visual effects.")
				neg_factors.append(0)
				neg_factors.append("")
				neg_factors.append("")

		
		if len(final)==0:
			prediction = 0
		else:
			#the prediction is the most common value in 'final'. If multitple integers are most common, then the highest value takes preference.
			count = Counter(final)
			prediction = count.most_common()[0][0]
			c = count.most_common()[0][1]
			for item in count.most_common():
				if item[1]==c:
					prediction = item[0]

		#if the film has a prequel and it was more successful than the current prediction, then it's gross becomes the current prediction. Most sequels do as well
		#or better than their predecers.
		if prequel and prequel[0][1][2] >= prediction:
			prediction = prequel[0][1][2]

		#if the director's latest film was more successful than the prediction, then that film's gross becomes the prediction
		if latest and latest[1][2] > prediction:
			prediction = latest[1][2]

		#add the 'trilogy_boost', which bumps the prediction up a tier if it is the end of a trilogy.
		prediction = prediction + trilogy_boost

		#return the film entry, positive factors of success, and negative factors of success. These are formatted to be used in the bar charts for the web site.
		return [movie, prediction, pos_factors, neg_factors]


	#When a film title is given, search self.data2 for the film matching that
	#title, and return the entry. If it's not found, return None.
	def find_film(self, title):
		for movie in self.data2:
			if movie[0]==title:
				return movie
		return None

	#Determine the usual film gross of a specified week of the year.
	def weekrate(self, n, b):
		gross = 0 #Running total of the domestic gross of all films released
				  #on the specified week of the year.
		budget = 0 #Running total of the budget "  "
		films = [] #List of all films released on the specified week of the year.
		nfilms = [] #Narrowed list of matching films, based on similar budgets.
		total = [] #List of revenue tiers for films released on specified week.

		for movie in self.data2:
			#find the week of the movie's release
			date = utilities.findweek(movie[4][0], movie[4][1], movie[4][2])
			if date==n: #if the release week's match
				films.append(movie) #list the movie

		#if no matches were found, return None
		if len(films)==0:
			return None

		#otherwise narrow the results to include only those with the most
		#similar budgets
		nfilms = utilities.closest_matches(films, b)

		#then go through the list
		for entry in nfilms:
			gross+= entry[1][0] #sum the revenues
			budget+= entry[1][1] #sum the budgets
			total.append(entry[1][2]) #list the revenue tiers

		#determine the average success ratio
		av_gross = float(gross)/float(budget)
		#The final value of the revenue tier projection is the most common
		#value listed. In other words, if most films fall in tier 3, then 
		#final = 3.
		count = Counter(total)
		final = count.most_common()[0][0]

		#return an array of results
		return [final, av_gross]



	#Determine the usual film gross of a certain actor based on trends in recent years.
	def actor_trends(self, actor, movie):
		date = movie[4][3]
		year = movie[4][0]
		b = movie[1][1] #budget of searched film

		gross = 0 #Running total of the domestic gross of all films released
				  #on the specified week of the year.
		budget = 0 #Running total of the budget "  "
		films = [] #List of all films released on the specified week of the year.
		nfilms = [] #Narrowed list of matching films, based on similar budgets.
		total = [] #List of revenue tiers for films released on specified week.

		apartnerships = [] #list of actor partnerships
		dpartnerships = [] #list of director partnerships
		recent = None #most recent film released

		for entry in self.data2:
			#for each film in the data, if the actor is one of the main actors
			#in the film, but the film was released before the current movie
			#and was released in the last 5 years, and is not an animated film
			if actor in entry[2][1] and entry[4][3]<date and entry[4][0]>year-5 and entry[3][3]!="Digital Animation":
				films.append(entry) #add it to the list

		#if no matches were found, return None
		if len(films)==0:
			return None

		#sort the films according to when they were released
		films.sort(key = lambda x: x[4][3])
		#the last one released becomes 'recent'
		recent = films[-1]

		for f in films:
			#if the actor has worked with another actor in the current movie before
			#and successful films were produced together, then...
			for a in f[2][1]:
				if a!=actor and movie[2][2]!=f[2][2] and a in movie[2][1] and f[1][0]>100000000:
					apartnerships.append([a, f]) #... add it to the list
			#similarly, if the actor has worked with the same director on a previous 
			#film and it was successful, then...
			if movie[2][4]==f[2][4] and f[1][0]>100000000:
				dpartnerships.append([movie[2][4], f]) #... add it to the list

		#narrow the list of matches according to most similar budgets
		nfilms = utilities.closest_matches(films, b)

		#then go through the list
		for item in nfilms:
			gross+= item[1][0] #sum the revenues
			budget+= item[1][1] #sum the budgets
			total.append(item[1][2]) #list the revenue tiers

		#determine the average success ratio
		av_gross = float(gross)/float(budget)
		#The final value of the revenue tier projection is the most common
		#value listed. In other words, if most films fall in tier 3, then 
		#final = 3.
		count = Counter(total)
		final = count.most_common()[0][0]

		#return an array of results
		return [final, av_gross, recent, apartnerships, dpartnerships]

	

	#Determine the usual film gross of a certain director based on trends in recent years.
	def director_trends(self, movie):
		#This function works very similarly to 'weekrate'. See that function for 
		#further details if necessary.

		date = movie[4][3]
		year = movie[4][0]
		b = movie[1][1] #budget
		director = movie[2][4]

		gross = 0
		budget = 0
		films = []
		nfilms = []
		total = []	
		blockbuster = None #stores recent blockbuster film made by director

		for entry in self.data2:
			#if a film in the data was directed by the given director, but was
			#released prior to the current film within the previous 15 years
			if director==entry[2][4] and entry[4][3]<date and entry[4][0]>year-15:
				films.append(entry)

		if len(films)==0:
			return None

		films.sort(key = lambda x: x[4][3])
		recent = films[-1]

		for item in films:
			#if one of the films grossed more than $300,000,000
			if item[1][0]>300000000:
				#it is the 'blockbuster'. Since the list is already sorted, if
				#there are multiple, then the most recent takes the value of
				#'blockbuster'.
				blockbuster = item

		nfilms = utilities.closest_matches(films, b)

		for item in nfilms:
			gross+= item[1][0]
			budget+= item[1][1]
			total.append(item[1][2])

		av_gross = float(gross)/float(budget)
		count = Counter(total)
		final = count.most_common()[0][0]

		return [final, av_gross, recent, blockbuster]



	#Determine the usual film gross of a certain genre based on trends in recent years.
	def genre_trends(self, movie):
		#This function works very similarly to the above functions, such as director_trends.
		#See the above functions for additional details.
		genre = movie[3][0]
		b = movie[1][1]
		date = movie[4][3]
		year = movie[4][0]

		gross = 0
		budget = 0
		films = []
		nfilms = []
		total = []	

		for entry in self.data2:
			if genre==entry[3][0] and entry[4][3]<date and entry[4][0]>year-10:
				films.append(entry)

		if len(films)==0:
			return None

		nfilms = utilities.closest_matches(films, b)
		
		for item in nfilms:
			gross+= item[1][0]
			budget+= item[1][1]
			total.append(item[1][2])

		av_gross = float(gross)/float(budget)
		count = Counter(total)
		final = count.most_common()[0][0]

		return [final, av_gross]



	#Determine the usual film gross of a various factors based on trends in recent years.
	def other_trends(self, movie):
		#This function works very similarly to the above functions, such as director_trends.
		#See the above functions for additional details.
		source = movie[3][1]
		creative = movie[3][2]
		method = movie[3][3]
		budget = movie[1][1]
		date = movie[4][3]
		year = movie[4][0]

		films = []
		nfilms = []
		total = []	

		for entry in self.data2:
			if source==entry[3][1] and creative==entry[3][2] and method==entry[3][3] and entry[4][3]<date and entry[4][0]>year-10:
				films.append(entry)

		if len(films)==0:
			return None

		nfilms = utilities.closest_matches(films, budget)
		
		for item in nfilms:
			total.append(item[1][2])

		count = Counter(total)
		final = count.most_common()[0][0]

		return final



	#Determine a film most similar to the current film given the metadata.
	def find_similar(self, movie):
		best_match = None #Closest matching film.
		similar = 0 #Degree of similarity

		#search self.data2
		for entry in self.data2:
			checker = 0 #initial degree of similarity
			#If the film is not itself, the main characters do not match (aka it is not a prequel/sequel), and the 
			#film was made before the current movie, but within 5 years of it...
			#...procede.
			if movie[0]!=entry[0] and movie[2][2]!=entry[2][2] and entry[4][3]<movie[4][3] and entry[4][0]>movie[4][0]-5:
				#if the budgets are very similar
				if entry[1][1] <= movie[1][1]+5000000 and entry[1][1] >= movie[1][1]-5000000:
					checker+= 2
				#if the budgets are similar, but less so
				if entry[1][1] <= movie[1][1]+20000000 and entry[1][1] >= movie[1][1]-20000000:
					checker+= 1

				#if the lead actors match
				if entry[2][0]==movie[2][0]:
					checker+= 3
				#if the directors match
				if entry[2][4]==movie[2][4]:
					checker+= 2
				#if the genre matches
				if entry[3][0]==movie[3][0]:
					checker+= 5
				#if the source matches
				if entry[3][1]==movie[3][1]:
					checker+= 2
				#if the creative types match
				if entry[3][2]==movie[3][2]:
					checker+= 1
				#if the methods match
				if entry[3][3]==movie[3][3]:
					checker+= 1
				#if they are both sequels
				if entry[3][4]==movie[3][4]:
					checker+= 1

			#If the degree of similarity equals the greatest similarity and there
			#is already a best_match film...
			if checker==similar and best_match:
				#if the new match was made between the best_match and the current film...
				if best_match[4][3]<entry[4][3]:
					#the new match becomes the best_match
					best_match = entry

			#If the degree of similarity is better than the greatest similarity
			#thus far...
			elif checker > similar:
				#the new match becomes the best_match
				similar = checker
				best_match = entry

		#return the best matching film
		return best_match



	#If a film lists that it has a prequel, try to find it.
	def find_prequel(self, movie):
		prequel = None #Prequel of current movie.
		all_prequels = [] #List of all prequels of current movie.

		title = movie[0]
		stitle = title.split() #Split title into array of words
		subtitle = movie[0]
		actor = movie[2][0]
		character = movie[2][2]
		date = movie[4][3]

		if ':' in title:
			index = title.index(':')
			#title up until ':' character, i.e. "Star Wars Ep. 1: The Phantom Menace"
			subtitle = title[:index]

		#Search self.data2
		for film in self.data2:
			#if the film is not the current movie and was made before it
			if film[0]!=title and film[4][3]<date:
				s = film[0].split() #Split title into array of words
				#If film title is contained within current movie's title
				#i.e. "Despicable Me" is in "Despicable Me 2"
				if film[0] in title and character==film[2][2]:
					all_prequels.append(film)
				#If film has the same characters
				elif character in film[2][3]:
					all_prequels.append(film)
				#If the title portion until the ":" matches
				elif subtitle in film[0]:
					all_prequels.append(film)
				#If the first 3 words match
				elif s[:3]==stitle[:3]:
					all_prequels.append(film)
				#Same ':' check, but in reverse
				elif ':' in film[0]:
					index = film[0].index(':')
					temp = film[0][:index]
					if temp in title:
						all_prequels.append(film)

		#if no prequels were found, return None.
		if len(all_prequels)==0:
			return None

		#sort list of prequels based on order
		all_prequels.sort(key = lambda x: x[4][3])

		#The prequel wanted is the latest created.
		prequel = all_prequels[-1]

		#Return array of results.
		return [prequel, all_prequels]



	#Determine competition from films released the same or near weekends as current movie.
	def competition(self, movie):
		date = movie[4][3]
		week = utilities.findweek(movie[4][0], movie[4][1], movie[4][2])
		year = movie[4][0]
		title = movie[0]

		competitors = [] #list of films released on nearly the same weekend as current film
		ncompetitors = [] #narrowed list based on most successful competitors

		#search data
		for entry in self.data2:
			#determine week of release
			w = utilities.findweek(entry[4][0], entry[4][1], entry[4][2])
			if title!=entry[0]: #if the film being looked at is not the current film
				if date==entry[4][3]: #if the films were released on exactly the same date
					competitors.append(entry)
				#if the films were released within 2 weeks of each other
				elif year==entry[4][3] and (week==w or (week>=w-2 and week<=w+2)):
					competitors.append(entry)
				#same search but considering films released at the beginning/end of the year
				elif week>=51 and year==entry[4][3]-1 and w<=(week+2)%53:
					competitors.append(entry)
				elif week<=2 and year==entry[4][3]+1 and w>=(week-2)%53:
					competitors.append(entry)

		#of the list of films released near the current film's date
		for c in competitors:
			#if they were or are projected to be successful
			if c[1][0]>=100000000:
				#then they are a major competitor, and are added to the final list
				ncompetitors.append(c)

		#Return the final list of major competitors
		return ncompetitors

#create class item
c = CineCast_Explain()

#example call
#c.predict("Jurassic Park")


