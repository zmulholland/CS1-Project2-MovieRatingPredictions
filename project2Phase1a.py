#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 10:51:59 2023

@author: zackmulholland
"""

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
    f = open("ml-100k/u.item", encoding="windows-1252")
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