__author__ = 'ronfe'

from pymongo import MongoClient
from bson.objectid import ObjectId
import operator

divide = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

dbClient = MongoClient('mongodb://localhost:27017')
db = dbClient['yangcong']

problemhistories = db.problemhistories
users = db.users

# Given a dict of topic processing result, return a list of [[userId, score]]
def calcScore(topicObj):
    examinees = topicObj['sampleUsers']
    items = topicObj['selectedProblems']

    result = []

    for each in examinees:
        thisUser = users.find_one({"_id": each})
        if thisUser['role'] == 'student':
            pipeLine = [
                {"$match": {"user": each, "problem": {"$in": items}}},
                {"$group": {"_id": "$problem", "first": {"$first": "$isCorrect"}}},
                {"$match": {"first": True}}
            ]
            tempResult = len(list(problemhistories.aggregate(pipeLine)))
            result.append({"userId": each, "score": tempResult})

    return result

# Given a list of user scores and divide them into 7 groups
def divideGroup(userScores):
    sortedList = sorted(userScores, key=operator.itemgetter('score'))
    userAmount = len(sortedList)
    dividedList = divide(sortedList, userAmount / 7 + 1)
    return dividedList


unitTopic = {'topicId': ObjectId('54c708798bac81fccbd4bae5'), 
             'selectedProblems': [
                 ObjectId('54d00acafccce2307007853b'), 
                 ObjectId('54d00c25fccce23070078563'), 
                 ObjectId('54d00bd1fccce23070078559'), 
                 ObjectId('54cb25f8549d04051913b5e4'), 
                 ObjectId('54cf519404c427f9694c0254'), 
                 ObjectId('54cf51cd04c427f9694c0259')
             ], 
             'sampleUsers': [
                 ObjectId('55e6ce0d741430a274e71463'), 
                 ObjectId('55c99a876fe0007d3cb7e4c1'), 
                 ObjectId('55cafcd9ef7c5115104c6f40'), 
                 ObjectId('5509246048ceeae54a1d8320'), 
                 ObjectId('5603db1b902b94b81d2ff6bc'), 
                 ObjectId('55f7fb334ad99025624c4c9a'), 
                 ObjectId('55dd5edddbfa242b60697546'), 
                 ObjectId('55b078a3024909516ae9affe'), 
                 ObjectId('55dda82928ab60ee7a32990c'),
                 ObjectId('55e44daf47c22bb0138ddbc1'), 
                 ObjectId('55e44daf47c22bb0138ddbc2'), 
                 ObjectId('55d498bcff9a0aaa51c5b1d7'), 
                 ObjectId('55e6c8316980054275984575'), 
                 ObjectId('55fccb7d5f50716b0f51a43c'), 
                 ObjectId('55e8e742eff4782275b8af56'), 
                 ObjectId('55dff7abd9e1904b5e5f6ac9'), 
                 ObjectId('55f4d0d39688dc240774e547'), 
                 ObjectId('54d7ae43dc24a6d1de85e52e'), 
                 ObjectId('560605ebf2aa24653a4a7203'), 
                 ObjectId('55d1f3fd22a1be3e510fbe19'), 
                 ObjectId('55ed885e284c401e6ba4cc81'), 
                 ObjectId('55bde7daf99db93c3727d590'), 
                 ObjectId('55bc655525b056a645c5d96e'), 
                 ObjectId('5597e35cac2a17dc4c6ddbd1'), 
                 ObjectId('55dfe9c33d19956b5eb32cdd'), 
                 ObjectId('55a8b065e0b3c555770c65c7'), 
                 ObjectId('55c3141d9216a7f3578add3e'), 
                 ObjectId('55c357d810a56f57614cd569'), 
                 ObjectId('553f68ccb24e74e57af2522b'), 
                 ObjectId('55c831beafd73eea2db0254a'), 
                 ObjectId('55f649f15790a0bf52fc96c6'), 
                 ObjectId('55da9ad522a1be3e511a0c84'), 
                 ObjectId('55ddcfd863be02b07be38f1c'), 
                 ObjectId('55decf48915225cf5ae851a6'), 
                 ObjectId('55c9f1140a85d0fd702d9b05'), 
                 ObjectId('55fad2ed593ff949572b3970'), 
                 ObjectId('55cdfaabb143f7387a62f228'), 
                 ObjectId('55f95e2f3baabd967d3a672f'), 
                 ObjectId('55db1691816c3f6c503ac59c'), 
                 ObjectId('55cda23252eda6187a0b44b7'), 
                 ObjectId('55fcbf34faacfc1f57ab9537'), 
                 ObjectId('55b19bd3d54080e8522acc7f'), 
                 ObjectId('55c8569565e687a05e641b0a'), 
                 ObjectId('56035df9f91d6f9a4161b62c'), 
                 ObjectId('55b60c386cb41ff96203bb25'), 
                 ObjectId('55f2ad26dac54d0b25461109'), 
                 ObjectId('55f2c91a3a8ad22d122412e4'), 
                 ObjectId('55ed65fe8988d5ca61a780d0'), 
                 ObjectId('55fcda7c8577c20545f27351'), 
                 ObjectId('55f2b1f1adececee3d573c97'), 
                 ObjectId('55f501065351cbcc3e949559'), 
                 ObjectId('55c9912551c85b963c44de2e'), 
                 ObjectId('55bf08659f5cf460605b8e34'), 
                 ObjectId('55fbfe4b031ec03b1b4f4803'), 
                 ObjectId('55a88d9527352e427e2a153b'), 
                 ObjectId('55c2d7ddf2339cc35772e9d3'), 
                 ObjectId('55c47a8a2c1ae52f3a333534'), 
                 ObjectId('552c54065a7a42a11a4813f5'), 
                 ObjectId('55e26ac43018a1b36cdb6d60'), 
                 ObjectId('55b613fed6bd646663933e75'), 
                 ObjectId('55d6f7e6ff9a0aaa51c8d378'), 
                 ObjectId('55dc49c6013c4e4445754ba7'), 
                 ObjectId('55d70c90ff9a0aaa51c8f569'), 
                 ObjectId('55fd6d967d78fe3e7ad17eda'), 
                 ObjectId('55e6f785eff4782275b67a58'), 
                 ObjectId('55cf2e3152eda6187a0d10a9'), 
                 ObjectId('55cb0d3fb42d078f206e3d4e'), 
                 ObjectId('55c2fed6eecbd7b9571b9b5f'), 
                 ObjectId('55e00ea81a76eee86a41234b'), 
                 ObjectId('55f80d6f3e0826d329d1140c'), 
                 ObjectId('55b35b3a9cb85d0a73c81c75'),
                 ObjectId('55d70e3cb29bf88a51624be4'),
                ObjectId('55eac65b33b141510403c381'),
                ObjectId('55cae538a559d04710df3b42'),
                ObjectId('55fbe0d6e82bd1d20c48e2db'),
                ObjectId('55dbee8c524b7b835c9b2aaf'),
                ObjectId('55dea960915225cf5ae7d03b'),
                ObjectId('55bcb22348b8286937ab24db'),
                ObjectId('55eac65b33b141510403c396'),
                ObjectId('54ab818f819a123915be76c9'),
                ObjectId('55fad2ed593ff949572b399b'),
                ObjectId('55f3f60d42ace4766275658d'),
                ObjectId('55dc49c6013c4e4445754ba0'),
                ObjectId('55c2db5c9216a7f3578a3c1d'),
                ObjectId('55e6e8bd741430a274e76df0'),
                ObjectId('55deae625f12b00f5bcbc789'),
                ObjectId('55dc504a013c4e4445754c19'),
                ObjectId('55dc504a013c4e4445754c16'),
                ObjectId('55c0a4cbac87b7d52041dadd'),
                ObjectId('55dd718c7a14bf647b161e38'),
                ObjectId('55e623700b36db9d7110f0c5'),
                ObjectId('55a8bef81013a14377b11182'),
                ObjectId('54ce0fdffd8ddc281231140e'),
                ObjectId('55ffa0786313e28127fc7e5b'),
                ObjectId('55f514c029fa382a60216210'),
                ObjectId('55cac737a559d04710def114'),
                ObjectId('55ca022e0a85d0fd702dbf6f'),
                ObjectId('5600e49e283580be43640533'),
                ObjectId('55909749cb9d9af21894fb10'),
                ObjectId('55c06ad49093ee932037a3ec'),
                ObjectId('55e26ac43018a1b36cdb6d81'),
                ObjectId('55fd4ba2bab648ca784da37f'),
                ObjectId('55d4863fb29bf88a515ef5cc'),
                ObjectId('55a8c4c7cf05cc0b3f23a391'),
                ObjectId('56025467bb3ffb7d31cadd48'),
                ObjectId('55dc49c6013c4e4445754b95'),
                ObjectId('55c1943b894bfa7d5ce317ab'),
                ObjectId('55fa7167b513cebb25644d28'),
                ObjectId('55065518246a8f9f4b7d055e'),
                ObjectId('55f96148faef115e0d48632b'),
                ObjectId('55e1a32e8371a8136d6df1bd'),
                ObjectId('550eb348d6c7cf976a645093'),
                ObjectId('55cae4e0be72d53410befb1f'),
                ObjectId('55fcda6e8577c20545f272f4'),
                ObjectId('55f3f96710ca53e16706a4cc'),
                ObjectId('5600114fadab023b5f705cc3'),
                ObjectId('55bcc3c08461358f37412c78'),
                ObjectId('55d1d031ff9a0aaa51c1ab92'),
                ObjectId('55bc7e0df99db93c37263730'),
                ObjectId('55bf54dd1adcd5b905170e48'),
                ObjectId('55c9e9310a85d0fd702d8a05'),
                ObjectId('55c3229f9216a7f3578b09b2'),
                ObjectId('55e021ebb85d07c46aa1787e'),
                ObjectId('55dc03a55f2565335cc36e12'),
                ObjectId('55d40347816c3f6c5031a096'),
                ObjectId('55fbcead8e4f77d7536473c9'),
                ObjectId('55dfe47f725409cb5dec352f'),
                ObjectId('557556ccbc6b514911dba48d'),
                ObjectId('55e93f2df83adcd375c1f554'),
                ObjectId('55d57423b29bf88a515fd3c8'),
                ObjectId('55dc4f16013c4e4445754bd6'),
                ObjectId('55dc49c6013c4e4445754b9f'),
                ObjectId('55dc4a0f2e7375c740962664'),
                ObjectId('56081cd34aa10683023d8bb5'),
                ObjectId('55d57837b29bf88a515fe043'),
                ObjectId('54d4b9b0aa43fb310905856c'),
                ObjectId('55c994496fe0007d3cb7cf04'),
                ObjectId('560542a14f8980b75dda1b86'),
                ObjectId('55be09416a98826570a70e75'),
                ObjectId('55e26ac43018a1b36cdb6d49'),
                ObjectId('54a951c0264b1a9c2bb4a51d'),
                ObjectId('55f8153d7d9f432d49ed6ed6'),
                ObjectId('55f02116afffaeb46141d7b7'),
                ObjectId('55b4bfe9f7d05596727a0be4'),
                ObjectId('55ee8955609681770df25b3f'),
                ObjectId('559a5cd4a66c86ae4fc142ec'),
                ObjectId('55fa99e622aed93074f4cb0e'),
                ObjectId('55a8ca719935e98a42d47b46'),
                ObjectId('5602550c64fe716a67bcf3f3'),
                ObjectId('55d2cc0db29bf88a515c18f6'),
                ObjectId('55dc49c6013c4e4445754b8d'),
                ObjectId('5606164c43fa3c056d86fe0b'),
                ObjectId('55d30ec0ff9a0aaa51c39a64'),
                ObjectId('55ab4b1b645981f977bf3833'),
                ObjectId('551cd4b50298b61b134977cd'),
                ObjectId('55dc57fdc9f0e313412fc4d6'),
                ObjectId('55c49380b953b1751b6d7074'),
                ObjectId('55f7a5f17350af591dba01ca'),
                ObjectId('55c2d80df2339cc35772ea75'),
                ObjectId('55ec3b23b2cb6f9f28efe588'),
                ObjectId('55c99ce851c85b963c4507b1'),
                ObjectId('55e79fb5eff4782275b6f85e'),
                ObjectId('55f6b5b273b3e5f606eb6d67'),
                ObjectId('55e6f785eff4782275b67a52'),
                ObjectId('5601516c1e1e9a3504d2990b'),
                ObjectId('55c3524410a56f57614cc742'),
                ObjectId('55d414a6b29bf88a515dfa23'),
                ObjectId('55bec712d21c49625f836ca5'),
                ObjectId('55e26ac43018a1b36cdb6d77'),
                ObjectId('55e6d7f8741430a274e72d79'),
                ObjectId('55fd3546f28e3e3824521770'),
                ObjectId('55c87ec0465c0e4375fb9300'),
                ObjectId('55f17915412d2abf43a8e42f'),
                ObjectId('55c494dbb953b1751b6d730a'),
                ObjectId('55d2f6d2816c3f6c50307788'),
                ObjectId('55d712f922a1be3e5116b91d'),
                ObjectId('55cd71e6f968d1587a350a94'),
                ObjectId('55c8346420283b532eafaf2f'),
                ObjectId('55d810f1816c3f6c5036f856'),
                ObjectId('55d55200ff9a0aaa51c61a43'),
                ObjectId('55c456bd2c1ae52f3a32c763'),
                ObjectId('55f7e4ced400569e7ca2c4ad'),
                ObjectId('55e63310923c8b5a71a960f4'),
                ObjectId('55b5e8e082ad9b9463470209')
            ]}
a = calcScore(unitTopic)

a = divideGroup(a)

print a[6]