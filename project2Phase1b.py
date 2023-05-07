#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:51:59 2023

@author: zackmulholland
"""

import matplotlib.pyplot as plt

# Function that reads in the info of the users
def createUserList():
    f = open("ml-100k/u.user","r")
    userList = []
    for line in f:
        # Split the line up into the individual data points
        newLine = line.split("|")
        userList.append({"age": int(newLine[1]), "gender": newLine[2], "occupation": newLine[3], "zip": newLine[4][:len(newLine[4])-1]})
    return userList

# Function that reads in the info of the movies
def createMovieList():
    f = open("ml-100k/u.item", "r", encoding="windows-1252")
    movieList = []
    for line in f:
        # Split the line up in to the individual data points
        newLine = line.split("|")
        # Create a the list of the genre ratings
        newLine[23] = newLine[23][0]
        i = 5
        genreList = []
        while i < 24:
            genreList.append(int(newLine[i]))
            i = i + 1
        
        # Put the info into movieList
        movieList.append({"title": newLine[1], "release date": newLine[2], "video release date": newLine[3], "IMDB url": newLine[4], "genre": genreList})
    return movieList

# Function that stores all ratings as a list of tuples
def readRatings():
    f = open("ml-100k/u.data", "r")
    ratingTuples = []
    for line in f:
        # Split the line up
        line = line.split()
        ratingTuples.append((int(line[0]), int(line[1]), int(line[2])))
    return ratingTuples

# Function that creates two lists of dicts, one for the user ratings and one for the movie ratings
def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    # Initializing the lists of tuples
    rLu = []
    rLm = []
    for i in range(numUsers):
        rLu.append({})
    for i in range(numItems):
        rLm.append({})
    # Put all the ratings into a users tuple and a movies tuple
    for (user, item, rating) in ratingTuples:
        rLu[user - 1][item] = rating
        rLm[item - 1][user] = rating
    return [rLu, rLm]

# Function that generates a list of the genres
def createGenreList():
    f = open("ml-100k/u.genre", "r")
    genres = []
    for line in f:
        line = line.split("|")
        genres.append(line[0])
    # Remove the endline character
    genres = genres[:len(genres)-1]
    return genres


def demGenreRatingFractions(userList, movieList, rLu, gender, ageRange, ratingRange):
    numerators = [0] * 19
    denominator = 0
    # Find the users that fit the demographics
    validUserIndices = []
    i = 0
    while i < len(userList):
        if (userList[i]["gender"] == gender or gender == "A") and (ageRange[0] <= userList[i]["age"] and userList[i]["age"] < ageRange[1]):
            validUserIndices.append(i)
        i = i + 1
    
    # Find the ratings of the valid users
    for user in validUserIndices:
        # Update the denominator
        denominator = denominator + len(rLu[user])
        # Walk down the rating of each user- if the rating is in the range, add the respective genres to the numerator
        for i in range(len(movieList)):
            # If the user's rating of a movie is in the range
            if (i+1 in rLu[user]) and (ratingRange[0]<= rLu[user][i+1] and rLu[user][i+1] <= ratingRange[1]):
                numerators = updateNumerators(numerators, movieList[i])
    
    # If the denominator is zero, return all None
    if denominator == 0:
        return [None] * 19
    else:
        return [numerator/denominator for numerator in numerators]
            
# Function that updates the numerator 
def updateNumerators(numerators, movieDict):
    for i in range(19):
        numerators[i] = numerators[i] + movieDict["genre"][i]
    return numerators   


def add_to_all_elements_in_list(list1, val):
    return [elem+val for elem in list1]



def createPlot(data, label_tuple, title, ylabel):
    x = [val for val in range(len(label_tuple))] # the label locations
    width = 1/(len(data)+1) # the width of the bars
    multiplier = 0
    fig, ax = plt.subplots()
    
    for attribute, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(add_to_all_elements_in_list(x, offset), measurement, width,
                       label=attribute)
        multiplier += 1
        # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(add_to_all_elements_in_list(x, width), label_tuple)
    # ax.legend(loc='upper left', ncols=3)
    ax.legend(loc='best')
    # ax.set_ylim(0, 250)
    y_max = max([max(v) for k,v in data.items()])
    ax.set_ylim(0, y_max*1.2)

    
    # plt.show()
    pass
    


userList = createUserList()
movieList = createMovieList()
ratingTuples = readRatings()
numUsers = len(userList)
numItems = len(movieList)
genres = createGenreList()
[rLu, rLm] = createRatingsDataStructure(numUsers, numItems, ratingTuples)

label_tuple = ("Action", "Comedy", "Drama", "Horror", "Romance")
indices = [i for i in range(len(genres)) if genres[i] in label_tuple]
m4to5 = demGenreRatingFractions(userList, movieList, rLu, "M", [0, 125], [4, 5])
w4to5 = demGenreRatingFractions(userList, movieList, rLu, "F", [0, 125], [4, 5])
data = {
        "Men": [m4to5[i] for i in indices],
        "Women": [w4to5[i] for i in indices]
        }
title='High Ratings from Men and Women'
ylabel='Fraction of Ratings'
createPlot(data, label_tuple, title, ylabel)


m1to2 = demGenreRatingFractions(userList, movieList, rLu, "M", [0, 125], [1, 2])
w1to2 = demGenreRatingFractions(userList, movieList, rLu, "F", [0, 125], [1, 2])
data = {
        "Men": [m1to2[i] for i in indices],
        "Women": [w1to2[i] for i in indices]
        }
title='Low Ratings from Men and Women'
ylabel='Fraction of Ratings'
createPlot(data, label_tuple, title, ylabel)


y4to5 = demGenreRatingFractions(userList, movieList, rLu, "A", [20, 30], [4, 5])
o4to5 = demGenreRatingFractions(userList, movieList, rLu, "A", [50, 60], [4, 5])
data = {
        "Younger Adults (20-29)": [y4to5[i] for i in indices],
        "Older Adults (50-59)": [o4to5[i] for i in indices]
        }
title='High Ratings from Younger and Older Adults'
ylabel='Fraction of Ratings'
createPlot(data, label_tuple, title, ylabel)


y1to2 = demGenreRatingFractions(userList, movieList, rLu, "A", [20, 30], [1, 2])
o1to2 = demGenreRatingFractions(userList, movieList, rLu, "A", [50, 60], [1, 2])
data = {
        "Younger Adults (20-29)": [y1to2[i] for i in indices],
        "Older Adults (50-59)": [o1to2[i] for i in indices]
        }
title='Low Ratings from Younger and Older Adults'
ylabel='Fraction of Ratings'
createPlot(data, label_tuple, title, ylabel)