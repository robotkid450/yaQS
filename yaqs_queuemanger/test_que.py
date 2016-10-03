#! /usr/bin/env python3
import yaqsQueue
from sys import exit

q = yaqsQueue.QueueData()  #create que obj

q.addJob('HPtest', 'command', 1, 'workingDirectory')
jID= q.HPque[0].id
print(q.getJobInfo(jID))

