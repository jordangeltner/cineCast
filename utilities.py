import datetime

#This function returns an integer between 0 and 53 indicating 
#the week of the year of the given date
def findweek(year, month, day):
	return datetime.date(year, month, day).isocalendar()[1]

#This function receives an array of films with metadata. The list results
#from one of the class functions, such as actor_trends or genre_trends. It then
#reduces the array to 5 or less entries by eliminating the entries with the most 
#dissimilar budgets until 5 or less films are listed. Having a similar budget
#helps with maintaining accuracy.
def closest_matches(array, budget):
	while len(array)>5:
		array.remove(array[max(range(len(array)), key=lambda x: abs(array[x][1][1]-budget))])
	return array

#This film classifies movies based on the degree of their success.
def find_range(num):
	if num < 50000000:
		return 1
	elif num < 100000000:
		return 2
	elif num < 150000000:
		return 3
	elif num < 200000000:
		return 4
	elif num < 250000000:
		return 5
	elif num < 300000000:
		return 6
	elif num < 350000000:
		return 7
	elif num < 400000000:
		return 8
	elif num < 450000000:
		return 9
	elif num < 500000000:
		return 10
	else:
		return 11