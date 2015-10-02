__author__ = 'ronfe'

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from scipy.stats import norm
import random

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']

publishers = db.publishers
cvGrades = db.cvgrades
chapters = db.chapters
topics = db.topics
tasks = db.tasks
activities = db.activities
problems = db.problems
problemhistories = db.problemhistories

chapterList = cvGrades.find_one({'_id': ObjectId("557e9e81c671eab2f357e689")})['chapters']

tempChapter = chapterList[0]

''' find histories '''
# records = problemhistories.find({"chapter": tempChapter})
# data = []
# for each in records:
#     data.append(each['problem'])
#
# data = list(set(data))
#
# # Experiment with one question
# unitProblem = data[300]
# pUsers = []

def calcParameters(qId):
    # Step 1 calc difficulty
    pipeLine = [
        {"$match": {"problem": qId}},
        {"$group": {"_id": "$user", "correct": {"$first": "$isCorrect"}}},
        {"$group": {"_id": "$correct", "count": {"$sum": 1}}}
    ]
    data = list(problemhistories.aggregate(pipeLine))
    if data[0]['_id']:
        correct = data[0]['count']
        incorrect = data[1]['count']
    else:
        correct = data[1]['count']
        incorrect = data[0]['count']
    ratio = float(correct) / (correct + incorrect)
    diff = norm.ppf(ratio)

    # Step 2 calc guessing parameter
    thisProblem = problems.find_one({"_id": qId})
    guessingParam = float(1) / len(thisProblem['choices'])

    # Step 3 calc discrimination

    print guessingParam


# calcParameters(ObjectId('54cb3731549d04051913b773'))

# Return a list of problem ids that in the topic and has at least 3 choices
def getProblems(topicId):
    pipeLine = [
        {'$match': {'topic': topicId}},
        {'$group': {'_id': '$problem'}}
    ]
    unFilteredList = list(problemhistories.aggregate(pipeLine))

    # filter the list
    result = []
    for each in unFilteredList:
        problemId = each['_id']
        thisProblem = problems.find_one({'_id': problemId})
        if thisProblem != None and len(thisProblem['choices']) >= 3:
            result.append(problemId)

    return result



# Return all the users who did the given problem id
def getUsers(problemId):
    pipeLine = [
        {'$match': {'problem': problemId}},
        {'$group': {'_id': '$user'}}
    ]
    result = list(problemhistories.aggregate(pipeLine))
    # return output
    output = []
    for each in result:
        output.append(each['_id'])

    # uniquify before return
    return list(set(output))


# Return the users who did all the problems in topicId
def getVerifiedUsers(topicId, problemRatio):
    questions = getProblems(topicId)
    questionUsers = []


    problemAmount = round(problemRatio * len(questions))
    output = {}
    output['topicId'] = topicId
    output['selectedProblems'] = random.sample(questions, int(problemAmount))

    for each in output['selectedProblems']:
        questionUsers.append(set(getUsers(each)))

    result = list(set.intersection(* questionUsers))
    output['sampleUsers'] = result
    return output

# Return a ratio number of the problems selection
def calcProblemRatio(chapterId, problemAmount):
    pipeLine = [
        {'$match': {'chapter': chapterId}},
        {'$group': {'_id': '$problem'}}
    ]
    unFilteredList = list(problemhistories.aggregate(pipeLine))

    # filter the list
    result = []
    for each in unFilteredList:
        problemId = each['_id']
        thisProblem = problems.find_one({'_id': problemId})
        if len(thisProblem['choices']) >= 3:
            result.append(problemId)

    ratio = float(problemAmount) / len(result)

    return ratio

# Return all the topics in a given chapter
def getTopics(chapterId):
    pipeLine = [
        {'$match': {'chapter': chapterId}},
        {'$group': {'_id': '$topic'}}
    ]
    tempTopics = list(problemhistories.aggregate(pipeLine))
    output = []
    for each in tempTopics:
        output.append(each['_id'])

    return output


chapterId = ObjectId("538fe05c76cb8a0068b14031")
pRatio = calcProblemRatio(chapterId, 50)
topicList = getTopics(chapterId)
a = getVerifiedUsers(topicList[0], pRatio)

print a