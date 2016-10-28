#! /usr/bin/env python3
import yaqsQueue
from sys import exit
import pdb

q = yaqsQueue.QueueData()  #create que obj

q.addJob('HPtest', 'command', 1, 'workingDirectory')
q.addJob('SPtest', 'command', 2, 'workingDirectory')
q.addJob('LPtest', 'command', 3, 'workingDirectory')
jobs = q.getAllJobs()
print('all jobs', jobs)
for item in jobs:
    print('Info for:', item[0])
    info = q.getJobInfo(item[0])
    print(info)
print(jobs)

jid = jobs[0][0]
print("jid :", jid)
q.removeJob(jid)
print('all jobs', q.getAllJobs())
jobToRun = q.getJobToRun()
print('Job to run: ', jobToRun)
print('marking as complete ',q.markRunningJobComplete(jobToRun[0]))
#print('marking as complete ',q.markRunningJobComplete('asd'))
