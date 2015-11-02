__author__ = 'ronfe'

from pymongo import MongoClient
import numpy as np
from scipy import optimize
dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']

originProblems = db['problemorigin']
updatedProblems = db['problemupdate']
problems = db['problems']

def estimateParams():
    for doc in originProblems.find():
        problemId = doc['problemId']
        responses = doc['response']
        # Guessing index
        unitProblem = problems.find_one({"_id": problemId})
        if len(unitProblem['choices']) >= 4:
            c = 1.0 / len(unitProblem['choices'])
        else:
            continue

        theta = []
        res = []
        for each in responses:
            theta.append(responses[each]['zscore'])
            res.append(responses[each]['response'])

        # dd
        def itemCharacters(x, a, b):
            return c + (1-c)*(1 / (1 + np.exp(-a * (x - b))))

        initialEstimation = np.array([0.0, 0.0])
        result = optimize.curve_fit(itemCharacters, np.array(theta), np.array(res), initialEstimation)
        result = list(result[0]) + [c]

        updatedProblems.insert_one({
            "problemId": problemId,
            "a": result[0],
            "b": result[1],
            "c": result[2]
        })


estimateParams()