#! /usr/bin/env python3
import yaqsQueue
from sys import exit

q = yaqsQueue.QueueData()  #create que obj

q.addJob('HPtest', 'command', 1, 'workingDirectory')
q.addJob('HPtest', 'command', 2, 'workingDirectory')
q.addJob('HPtest', 'command', 3, 'workingDirectory')
hpID= q.HPque[0].id
spID= q.SPque[0].id
lpID= q.LPque[0].id
print('hp : ', q.getJobInfo(hpID))
print('sp : ', q.getJobInfo(spID))
print('lp ; ', q.getJobInfo(lpID))

print('all jobs', q.getAllJobs())

q.removeJob(hpID)
print('all jobs', q.getAllJobs())