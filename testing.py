__author__ = 'ronfe'

from pymongo import MongoClient
import math
import random

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']
problemParameters = db['problemupdate']

# Given a number of current Theta value estimated,
# A list of items that user already answered, and
# A list of all the items
# Return the next problem's id
def chooseProblem(curTheta, usedItems, itemPool):
    maxInformation = 0.0
    maxProbId = ''
    maxProbProb = 0.0

    # Get unused problems
    unusedProbs = list(set(itemPool).difference(set(usedItems)))

    # Traverse the unused problems
    for each in unusedProbs:
        # get problem parameter from db
        eachParameters = problemParameters.find_one({'problemId': each})
        # eachA = math.log(eachParameters['distinction'] + 1, 2)
        eachA = eachParameters['a']
        eachB = eachParameters['b']
        eachC = eachParameters['c'] - 0.1


        if abs(eachB) <= 3 and abs(eachA) <= 2.8:
            P_each_theta = eachC + (1-eachC) * (1 / (1 + math.exp(-eachA * (curTheta - eachB))))
            eachInfo = (eachA * eachA) * ((1 - P_each_theta) / P_each_theta) * ((P_each_theta - eachC * eachC) / (1 - eachC * eachC))
            if eachInfo > maxInformation:
                maxProbId = each
                maxInformation = eachInfo
                maxProbProb = P_each_theta

    return [maxProbId, maxProbProb]

def calcProblemProb(problemId, theta):
    problemParam = problemParameters.find_one({"problemId": problemId})
    # a = math.log(problemParam['distinction'], 2)
    a = problemParam['a']
    b = problemParam['b']
    c = problemParam['c'] - 0.1
    P_theta = c + (1-c) * (1 / (1 + math.exp(-a * (theta - b))))

    return P_theta

# Given a number of old user theta estimation, and
# an id of previous problem, and
# a number of the correctness of user's response (1 for true, 0 for false)
# return a list like:
# [newTheta, standardError]
def updateEstimate(oldTheta, problemId, userResponse):
    # get problem parameter
    problemParam = problemParameters.find_one({"problemId": problemId})
    # a = math.log(problemParam['distinction'], 2)
    a = problemParam['a']
    b = problemParam['b']
    c = problemParam['c'] - 0.1
    P_theta = c + (1-c) * (1 / (1 + math.exp(-a * (oldTheta - b))))

    # newTheta = oldTheta + ((a * (userResponse - P_theta)) / (a * P_theta * (1 - P_theta)))
    # return newTheta
    itemFenzi = a * (userResponse - P_theta)
    itemFenmu = a * P_theta * (1 - P_theta)

    return [itemFenzi, itemFenmu]

def simulation(steps, realTheta, probPool):
    items = 0
    oriTheta = 0.0
    curTheta = 0.0
    fenzi = 0.0
    fenmu = 0.0
    used = []
    while items <= steps:
        items += 1

        # print 'Question ' + str(items)
        problemId = chooseProblem(curTheta, used, probPool)[0]
        correctProb = calcProblemProb(problemId, realTheta)

        # print 'The probability of right is ' + str(correctProb)
        answer = random.randint(1,100)

        if answer <= correctProb * 100:
            # print 'Answered right'
            limitation = updateEstimate(curTheta, problemId, 1)
        else:
            # print 'Answered wrong'
            limitation = updateEstimate(curTheta, problemId, 0)

        fenzi += limitation[0]
        fenmu += limitation[1]

        curTheta = oriTheta + (fenzi / fenmu)

        # print 'Current theta is ' + str(curTheta)
        used.append(problemId)
    return curTheta

problems = list(problemParameters.aggregate([{"$group": {"_id": None, "problems": {"$addToSet": "$problemId"}}}]))
problems = problems[0]["problems"]

# chooseProblem(curTheta, usedItems, itemPool)
# calcProblemProb(problemId, theta)
# random.randint(1,100)
# updateEstimate(oldTheta, problemId, userResponse)
# cur = fenzi / fenmu