__author__ = 'ronfe'

from pymongo import MongoClient
from bson.objectid import ObjectId
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

# chapterList = cvGrades.find_one({'_id': ObjectId("557e9e81c671eab2f357e689")})['chapters']

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

# Give a chapterId, and return a list of processed topics
def wrapUpTopics(chapterId):
    pRatio = calcProblemRatio(chapterId, 50)
    topicList = getTopics(chapterId)

    result = []
    for each in topicList:
        tempTopic = getVerifiedUsers(each, pRatio)
        result.append(tempTopic)

    return result


# chapterId = ObjectId("538fe05c76cb8a0068b14031")
# a = wrapUpTopics(chapterId)
#
# print a