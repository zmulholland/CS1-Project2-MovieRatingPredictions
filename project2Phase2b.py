#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:51:59 2023

@author: zackmulholland
"""

import matplotlib.pyplot as plt
import random
import time

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
    

# Functions that attempt to guess the rating from a user who has not rated a movie
# Random integer
def randomPrediction(u, m):
    return random.randint(1,5)

# The mean of all the user's ratings
def meanUserRatingPrediction(u, m, rLu):
    sumOfRatings = 0
    amountOfRatings = len(rLu[u - 1])
    for i in rLu[u - 1]:
        sumOfRatings = sumOfRatings + rLu[u-1][i]
    
    if amountOfRatings == 0:
        return None
    else:
        return sumOfRatings/amountOfRatings

# The mean of all the movie's ratings
def meanMovieRatingPrediction(u, m, rLm):
    sumOfRatings = 0
    amountOfRatings = len(rLm[m - 1])
    for i in rLm[m - 1]:
        sumOfRatings = sumOfRatings + rLm[m-1][i]
    
    if amountOfRatings == 0:
        return None
    else:
        return sumOfRatings/amountOfRatings

# Prediction based on age and gender
def demRatingPrediction(u, m, userList, rLu):
    gender = userList[u - 1]["gender"]
    age = userList[u-1]["age"]
    ageRange = [age - 5, age + 6]
    validUserIndices = []
    # Find the users in the demographics
    for i in range(len(userList)):
        if (userList[i]["gender"] == gender) and (ageRange[0] <= userList[i]["age"] and userList[i]["age"] < ageRange[1]) and (i != u - 1):
            validUserIndices.append(i)
    
    # Find the ratings of movie m for that particular demographic
    sumOfRatings = 0
    amountOfRatings = 0
    for userMinusOne in validUserIndices:
        if m in rLu[userMinusOne]:
            sumOfRatings = sumOfRatings + rLu[userMinusOne][m]
            amountOfRatings = amountOfRatings + 1
    
    if amountOfRatings == 0:
        return None
    else:
        return sumOfRatings/amountOfRatings

# Prediction based on the genre and the user's previous ratings
def genreRatingPrediction(u, m, movieList, rLu):
    sumOfRatings = 0
    amountOfRatings = 0
    M = sameGenre(m, movieList)
    for movie in M:
        if movie in rLu[u - 1] and movie != m:
            sumOfRatings = sumOfRatings + rLu[u - 1][movie]
            amountOfRatings = amountOfRatings + 1
        
    if amountOfRatings == 0:
        return None
    else:
        return sumOfRatings/amountOfRatings

# Function that finds the movies that are the same genre as a movie m
def sameGenre(m, movieList):
    movieIndices = []
    movieGenres = []
    for i in range(19):
        if movieList[m - 1]["genre"][i] == 1:
            movieGenres.append(i)
    for i in range(len(movieList)):
        same = False
        for j in movieGenres:
            if movieList[i]["genre"][j] == 1:
                same = True
        if same == True:
            movieIndices.append(i + 1)
    return movieIndices

# Splitting the ratings into a training and a testing set
def partitionRatings(rawRatings, testPercent):
    ratings = rawRatings.copy()
    testSize = int(len(rawRatings) * testPercent / 100)
    testSet = []
    for i in range(testSize):
        testSet.append(ratings.pop(random.randint(1, len(ratings) - 1)))
    
    trainingSet = ratings
    return [trainingSet, testSet]

# Computing the RMSE of predicted ratings
def rmse(actualRatings, predictedRatings):
    sumOfSquaredDifferences = 0
    numRatings = 0
    for i in range(len(actualRatings)):
        if predictedRatings[i] != None:
            sumOfSquaredDifferences = sumOfSquaredDifferences + (actualRatings[i] - predictedRatings[i]) ** 2
            numRatings = numRatings + 1
    average = sumOfSquaredDifferences / numRatings
    return average ** (1/2)

def draw_boxplot(data, labels):
    plt.boxplot(x=data, labels=labels)
    plt.title("Algorithm performance comparison")
    plt.ylabel("RMSE values")
    plt.show()
    plt.close()






randAve, userAve, movieAve, demAve, genreAve = [], [], [], [], []
for i in range(10):
    userList = createUserList()
    movieList = createMovieList()
    rawRatings = readRatings()
    numUsers = len(userList)
    numItems = len(movieList)
    genres = createGenreList()
    [rLu, rLm] = createRatingsDataStructure(numUsers, numItems, rawRatings)
    [trainingSet, testSet] = partitionRatings(rawRatings, 20)
    [trainingRLu, trainingRLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)
    actualRatings = []
    rand = []
    userAverage = []
    movieAverage  = []
    demographicRating  = []
    genreAverage = []
    
    for rating in testSet:
        actualRatings.append(rating[2])
        rand.append(randomPrediction(rating[0], rating[1])),
        userAverage.append(meanUserRatingPrediction(rating[0], rating[1], trainingRLu))
        movieAverage.append(meanMovieRatingPrediction(rating[0], rating[1], trainingRLm))
        demographicRating.append(demRatingPrediction(rating[0], rating[1], userList, trainingRLu))
        genreAverage.append(genreRatingPrediction(rating[0], rating[1], movieList, trainingRLu))
    
    
    randAve.append(rmse(actualRatings, rand))
    userAve.append(rmse(actualRatings, userAverage))
    movieAve.append(rmse(actualRatings, movieAverage))
    demAve.append(rmse(actualRatings, demographicRating))
    genreAve.append(rmse(actualRatings, genreAverage))
    
data = [randAve, userAve, movieAve, demAve, genreAve]
labels = ["Algo1", "Algo2", "Algo3", "Algo4", "Algo5"]
draw_boxplot(data, labels)
data = [userAve, movieAve, demAve, genreAve]
labels = ["Algo2", "Algo3", "Algo4", "Algo5"]
draw_boxplot(data, labels)