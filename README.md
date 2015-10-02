An Item Response model based problem select - test - result project

## Parts

Planning 3 parts: item parameter estimation (Python), API server (Node.js), and frontend (AngularJS)

* Item parameter estimation calculated all the needed parameters (chapterId, topicId, difficulty, discrimination, and guessing index), this part including 3 steps:
 - Step 1: Given an ObjectId of a chapter, pick a specific number (cur. 50) of problems in its topics, and return the userIDs who did all the problems in a topic (Mainly Done)
 - Step 2: Estimate the difficulty, discrimination, and guessing index per problem (i.e item) (To do, core)
 - Step 3: Store the data into db (Todo)
