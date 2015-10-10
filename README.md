An Item Response model based problem select - test - result project

For the core theory and the basic of IRT, pls refer to [this site](http://echo.edres.org:8080/irt/ )

## Parts

Planning 3 parts: item parameter estimation (Python), API server (Node.js), and frontend (AngularJS)

* Item parameter estimation calculated all the needed parameters (chapterId, topicId, difficulty, discrimination, and guessing index), this part including 3 steps:
 - Step 1: Given an ObjectId of a chapter, pick a specific number (cur. 50) of problems in its topics, and return the userIDs who did all the problems in a topic (Done)  
   To do in next sprint: optimizing processing time using [multiple processes](https://docs.python.org/2/library/multiprocessing.html#using-a-pool-of-workers )
 - Step 2: Estimate the difficulty, discrimination, and guessing index per problem (i.e item) (Doing, most difficult)  
   - 2.1 Given a list of problems and its relevant testers, return the probability of right answer for each group of testers (done)
 - Step 3: Store the data into a new db collections (Todo)

* API Server
 - Step 1: Design website instantiation and data structure
 - Step 2: Examinee estimation algorithm (incl. examinee ability estimation, item response and re-response algorithm, Python or Node?)
 - Step 3: Build APIs according to ds and algorithm

* Frontend
 - Step 1: Basic framework and working progress
 - Step 2: Data manipulation
 - Step 3: Beautify
