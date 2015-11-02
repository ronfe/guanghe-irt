__author__ = 'ronfe'

from pymongo import MongoClient
from bson.objectid import ObjectId
from scipy import stats

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']

problemhistories = db['problemhistories']
user_ability = db['userability']
problem_origin_data = db['problemorigin']

chapterId = ObjectId("5409b508c34d6dc35117f23e")

def getProblemList(chapterId):
    pipeLine = [
        {"$match": {"chapter": chapterId}},
        {"$group": {"_id": "$problem", "testers": {"$addToSet": "$user"}}},
        {"$match": {"testers.100": {"$exists": True}}}
    ]
    result = list(problemhistories.aggregate(pipeLine))
    return result

def calc_user_ability(chapterId):
    pipeLine = [
        {"$match": {"chapter": chapterId}},
        {"$group": {"_id": "$user", "answered": {"$addToSet": "$problem"}}},
        {"$match": {"answered.20": {"$exists": True}}}
    ]
    user_answering = list(problemhistories.aggregate(pipeLine))

    for each in user_answering:
        userId = each["_id"]
        pipeLine = [
            {"$match": {"user": userId, "problem": {"$in": each['answered']}}},
            {"$group": {"_id": "$problem", "correctness": {"$first": "$isCorrect"}}}
        ]
        tempRes = list(problemhistories.aggregate(pipeLine))
        correctAmt = 0.0
        for eachOne in tempRes:
            if eachOne["correctness"] == True:
                correctAmt += 1

        correctRte = correctAmt / len(tempRes)
        user_ability.insert_one({"user": userId, "ability": correctRte})

def getProblemOriginalData(chapterId):
    problems = getProblemList(chapterId)
    for each in problems:
        eachId = each['_id']
        eachTesters = each['testers']
        testerIds = []
        testerScores = []
        for eachOne in eachTesters:
            eachOneAbility = user_ability.find_one({"user": eachOne})

            if eachOneAbility != None:
                testerIds.append(str(eachOne))
                eachOneAbility = eachOneAbility['ability']
                testerScores.append(eachOneAbility)

        testerZ = stats.zscore(testerScores)

        testerObj = {}
        for i in range(0, len(testerIds)):
            testerObj[testerIds[i]] = {"zscore": testerZ[i]}
            # calc response
            userResponse = problemhistories.find_one({"problem": eachId, "user": ObjectId(testerIds[i])})
            if userResponse['isCorrect']:
                testerObj[testerIds[i]]['response'] = 1
            else:
                testerObj[testerIds[i]]['response'] = 0

        problem_origin_data.insert_one({
            "problemId": eachId,
            "response": testerObj
        })


getProblemOriginalData(chapterId)