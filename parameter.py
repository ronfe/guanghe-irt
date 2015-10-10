__author__ = 'ronfe'

from pymongo import MongoClient
from bson.objectid import ObjectId
from scipy import stats

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']
problems = db['problems']
problemHistories = db['problemhistories']


topicUserGroup = [[{'score': 2, 'userId': ObjectId('55f2da0832003b6856999446')}], [{'score': 3, 'userId': ObjectId('55b5e8e082ad9b9463470209')}, {'score': 3, 'userId': ObjectId('55a8bef81013a14377b11182')}, {'score': 3, 'userId': ObjectId('54c8aa0c10f4d57f3805c5a8')}, {'score': 3, 'userId': ObjectId('55daa202b29bf88a5165bf9d')}, {'score': 3, 'userId': ObjectId('55bf17cc73c9f6ad5f7af56b')}, {'score': 3, 'userId': ObjectId('5506186e48ceeae54a1cfb31')}], [{'score': 4, 'userId': ObjectId('55fd222985ec587f4b37d2c5')}, {'score': 4, 'userId': ObjectId('54d98a50fecd17e84a8ad404')}, {'score': 4, 'userId': ObjectId('55fad2ed593ff949572b3970')}, {'score': 4, 'userId': ObjectId('55dda82928ab60ee7a32990c')}, {'score': 4, 'userId': ObjectId('55e021ebb85d07c46aa1787e')}, {'score': 4, 'userId': ObjectId('560542a14f8980b75dda1b86')}, {'score': 4, 'userId': ObjectId('55cf2e3152eda6187a0d10a9')}, {'score': 4, 'userId': ObjectId('54ce100afd8ddc28123115cf')}, {'score': 4, 'userId': ObjectId('55cd954652eda6187a0b124e')}, {'score': 4, 'userId': ObjectId('54d859a5a37d6ca83712e215')}, {'score': 4, 'userId': ObjectId('55ddc2c563be02b07be37440')}, {'score': 4, 'userId': ObjectId('55c3422d1cd3a30061b42798')}, {'score': 4, 'userId': ObjectId('55d42327ff9a0aaa51c4c3e0')}, {'score': 4, 'userId': ObjectId('555fd800f89c611733f6e0a6')}, {'score': 4, 'userId': ObjectId('55d3206f816c3f6c5030e582')}, {'score': 4, 'userId': ObjectId('55d419c8816c3f6c5031cdef')}, {'score': 4, 'userId': ObjectId('5554579ed4e1ea751259872c')}, {'score': 4, 'userId': ObjectId('56013c0135addc0724ab5e47')}], [{'score': 5, 'userId': ObjectId('55fcda7c8577c20545f27351')}, {'score': 5, 'userId': ObjectId('55ed65fe8988d5ca61a780d0')}, {'score': 5, 'userId': ObjectId('55b46b639cb85d0a73c8a796')}, {'score': 5, 'userId': ObjectId('55c456bd2c1ae52f3a32c763')}, {'score': 5, 'userId': ObjectId('55bf08659f5cf460605b8e34')}, {'score': 5, 'userId': ObjectId('55c44c185a4196393a03751e')}, {'score': 5, 'userId': ObjectId('55e12d3a3018a1b36cd979a4')}, {'score': 5, 'userId': ObjectId('55e26ac43018a1b36cdb6d81')}, {'score': 5, 'userId': ObjectId('55f4d0d39688dc240774e547')}, {'score': 5, 'userId': ObjectId('55de6d9d63be02b07be3c807')}, {'score': 5, 'userId': ObjectId('55c9780ce70d1f6043623592')}, {'score': 5, 'userId': ObjectId('553f68ccb24e74e57af2522b')}, {'score': 5, 'userId': ObjectId('55f649f15790a0bf52fc96c6')}, {'score': 5, 'userId': ObjectId('55c6f0f6dee536d0498a971f')}, {'score': 5, 'userId': ObjectId('55d1d031ff9a0aaa51c1ab92')}, {'score': 5, 'userId': ObjectId('55b35b3a9cb85d0a73c81c75')}, {'score': 5, 'userId': ObjectId('55c9e9310a85d0fd702d8a05')}, {'score': 5, 'userId': ObjectId('55f179372e51b84e4e6e2c38')}, {'score': 5, 'userId': ObjectId('55b9a5e997bdc8242c969eea')}, {'score': 5, 'userId': ObjectId('55dfe47f725409cb5dec352f')}, {'score': 5, 'userId': ObjectId('54ce100afd8ddc28123115bd')}, {'score': 5, 'userId': ObjectId('55e445ac47c22bb0138dbb4b')}, {'score': 5, 'userId': ObjectId('55c9815fe70d1f6043624e19')}, {'score': 5, 'userId': ObjectId('55e425899c2403d6136724a0')}, {'score': 5, 'userId': ObjectId('55fcbf34faacfc1f57ab9537')}, {'score': 5, 'userId': ObjectId('54ab818f819a123915be76c9')}, {'score': 5, 'userId': ObjectId('55d2aba1816c3f6c502f8951')}], [{'score': 6, 'userId': ObjectId('55d55200ff9a0aaa51c61a43')}, {'score': 6, 'userId': ObjectId('55f911e63bf5bdfe440122cb')}, {'score': 6, 'userId': ObjectId('55e44daf47c22bb0138ddbcf')}, {'score': 6, 'userId': ObjectId('55f501065351cbcc3e949559')}, {'score': 6, 'userId': ObjectId('55c20289cf85fae957146dc4')}, {'score': 6, 'userId': ObjectId('55f3f60d42ace4766275658d')}, {'score': 6, 'userId': ObjectId('54cf50501407306471d656af')}, {'score': 6, 'userId': ObjectId('54254b72ade4de3b01cfe801')}, {'score': 6, 'userId': ObjectId('55d84d84816c3f6c50377f1a')}, {'score': 6, 'userId': ObjectId('55f581fb16d343d11f546a3f')}, {'score': 6, 'userId': ObjectId('55bb2595723bd9ef17d444c7')}, {'score': 6, 'userId': ObjectId('55fccd28e8bea82610b8760b')}, {'score': 6, 'userId': ObjectId('55c2d80df2339cc35772ea75')}, {'score': 6, 'userId': ObjectId('55ee454ee54d941839cfee1b')}, {'score': 6, 'userId': ObjectId('55e26ac43018a1b36cdb6d77')}, {'score': 6, 'userId': ObjectId('5600bbde39c769846e77bc02')}, {'score': 6, 'userId': ObjectId('55bec712d21c49625f836ca5')}, {'score': 6, 'userId': ObjectId('55c8495f6f437ff421087c8b')}, {'score': 6, 'userId': ObjectId('55bf54dd1adcd5b905170e48')}, {'score': 6, 'userId': ObjectId('55e136ea8371a8136d6cbae6')}, {'score': 6, 'userId': ObjectId('55e17fed3018a1b36cda76fc')}, {'score': 6, 'userId': ObjectId('55db1691816c3f6c503ac59c')}, {'score': 6, 'userId': ObjectId('55f17915412d2abf43a8e42f')}, {'score': 6, 'userId': ObjectId('55eebf7817e901544e64306a')}, {'score': 6, 'userId': ObjectId('56035df9f91d6f9a4161b62c')}]]
problemList = [ObjectId('54cb2729549d04051913b5f6'), ObjectId('54cf51cd04c427f9694c0259'), ObjectId('54d00999fccce2307007851c'), ObjectId('54d00a29fccce23070078527'), ObjectId('54cb24f3549d04051913b5c7'), ObjectId('54d00aa7fccce23070078536')]

# Given a list of problems and its usergroup, produce a dict of problems like
# {problemId: {difficulty: 0.1, distinction: 0.3, guessingIndex: 0.3}}
def parameter(problemList, userGroup):
    result = {}
    # Step 0 fill up all the problems into result
    for each in problemList:
        result[each] = {}

    # Step 1 guessing index
    for each in problemList:
        problem = problems.find_one({'_id': each})
        choiceNumber = len(problem['choices'])
        result[each]['guessingIndex'] = 1.0 / choiceNumber

    # Step 2 difficulty and distinction
    # 2.1 convert raw score to z score
    rawScores = []
    groupIds = {}
    for i in userGroup:
        for j in i:
            rawScores.append(j['score'])
    groupAbility = sorted(list(set(list(stats.zscore(rawScores)))))

    # 2.2 get group prob list
    probDict = {}
    for each in problemList:
        probDict[each] = {}
        for eachGroup in userGroup:
            groupIndex = userGroup.index(eachGroup)
            examineeId = []
            for eachOne in eachGroup:
                examineeId.append(eachOne['userId'])

            pipeLine = [{"$match": {
                "problem": each,
                "user": {"$in": examineeId}
            }}, {"$group": {
                "_id": "$user",
                "correctness": {"$first": "$isCorrect"}
            }}]
            groupStats = list(problemHistories.aggregate(pipeLine))
            r = 0
            t = 0
            for eachStat in groupStats:
                t += 1
                if eachStat['correctness']:
                    r += 1

            prob = float(r) / t
            probDict[each][groupAbility[groupIndex]] = prob

    return probDict

a = parameter(problemList, topicUserGroup)
print a
