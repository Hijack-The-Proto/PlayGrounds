class REVISION_DATA:
    def __init__(self, test, state, host):
        self.test = test
        self.state = state
        self.host = host

'''
here is an example of a dictionary containing all the info about a test failure state. 
I can write a list of known tests that run. if no result is given an assumed pass occurs

r100 = {"credentialscontainer-store-basics.https.html":{"expected":"PASS","actual":"TEXT"}

then when I receive an object containing all the results of a run I can write that to a list of revisions run.
History = [r100,r101,r102,....]
revision data objects are then stored in this list and the list can be travered to create the history output 


Output mockup:

                r100    r101    r102 ......
Test001.html    0       0       0
Test002.html    1       1       0
Test003.html    1       0       1
Test004.html    0       1       0

0 indicates a pass, 1 a failure. Test001.html is working as expected, Test1002.html is a new regression, the last two are flaky 

'''
