import time
start_time = time.time()

#systemtime process pid runtime


log=[['1000001','test/97846.html','200','150'],
    ['1000002','test/97846.html','300','1'],
    ['1000005','test/97846.html','50','5'],
    ['1001000','test/97846.html','200','50']]




#Q1 count the number of processes present ie (200=2, 300=1, 50=1)


dic = dict()

for i in range(len(log)):
    if log[i][2] not in dic:
        dic[log[i][2]]=1
    else:
        dic[log[i][2]]+=1

print('Number of occurances in log '+ str(dic))


#Q2 usng the system time in the first index and the process time length in the last index, print out how many processes are runing at each point in the log

currTime = int(log[0][0])
procTime = [int(log[0][3])]
timeDiff = 0

print('Time: ' + str(currTime) + ' Processes: ' + str(len(procTime)))

for i in range(len(log)-1):
    timeDiff = int(log[i+1][0]) - currTime
    currTime=int(log[i+1][0])
    drop=0
    for x in range(len(procTime)):
        procTime[x-drop]-=timeDiff
        if procTime[x-drop]<=0:
            procTime.pop(x-drop)
            drop+=1
    procTime.append(int(log[i+1][3]))
    print('Time: ' + str(currTime) + ' Processes: ' + str(len(procTime)))


print("Process finished --- %s seconds ---" % (time.time() - start_time))