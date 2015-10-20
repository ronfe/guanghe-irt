__author__ = 'ronfe'
from pymongo import MongoClient
from bson.objectid import ObjectId
from app import *
from estimation import *
from parameter import *

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']

problemParameters = db['problemParameters']

def insertChapters(chapterId):
    print "Step 1"
    wTopics = wrapUpTopics(chapterId)
    print "Step 1 Done"

    print "Step 2"
    for each in wTopics:
        unitProblemList = each['selectedProblems']
        unitTopicUserGroup = divideGroup(calcScore(each))

        unitProblems = calcParameter(unitProblemList, unitTopicUserGroup)
        # {problemId: {difficulty: 0.1, distinction: 0.3, guessingIndex: 0.3}}
        for eachProb in unitProblems.keys():
            diff = unitProblems[eachProb]['difficulty']
            dist = unitProblems[eachProb]['distinction']
            guess = unitProblems[eachProb]['guessingIndex']

            insertDoc = {
                "problem": eachProb,
                "difficulty": diff,
                "distinction": dist,
                "guessingIndex": guess
            }
            problemParameters.insert_one(insertDoc)


chapterId = ObjectId("54f3cd4c2964c9cf2002c81c")
insertChapters(chapterId)