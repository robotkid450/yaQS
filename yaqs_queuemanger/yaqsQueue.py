from collections import deque
import uuid

import pdb

__version__ = 2.1

MISSING = object()

class QueueData(object): # base object of queue managment
    """docstring for QueueData
       This is a basic multi-priority job queueing system."""

    def __init__(self):
        HPque = deque()     #Creates high priority que
        SPque = deque()     #Creates standard priority que
        LPque = deque()     #Creates low priority que
        runningJobs = []    #Creates running job list
        finishedJobs = []   #Creates comtainer to store completed jobs
        self.queues = []    #Creates container for queues
        self.queues.append(HPque)
        self.queues.append(SPque)
        self.queues.append(LPque)
        self.queues.append(runningJobs)
        self.queues.append(finishedJobs)
        self.jobsAvailable = 0  #Counter of currently avalible jobs

    def uuidGen(self): #creates an 8 char long id
        job_uuid = str(uuid.uuid4())[:8]
        return job_uuid

    def addJob(self, jobName, command, priority, workingDirectory):
        #adds a job to specified que
        #and increments jobsAvailable by 1
        job = Job(self.uuidGen(), jobName, command, workingDirectory)
        try:
            self.queues[priority-1].append(job)
            self.jobsAvailable +=1
            return 0
        except:
            return -1


    def getJobInfo(self, jobID):    # Retrives a jobs info
        for item in self.queues:
            for item in item:
                if item.id == jobID:
                    return item.getInfo()
                else:
                    pass
        else:
            return -1

    def getAllJobs(self):   #Gets all job names + IDs
        jobs = []

        for item in self.queues:
            for item in item:
                jobs.append([item.id, item.name])

        return jobs

    def removeJob(self, jobID): #Removes a job from que and decrements jobs
                                #avalible by 1
        found = False
        
        for item in self.queues:
            que = item
            for item in item:
                if item.id == jobID:
                    found = True
                    job_to_remove =item
                    
            if found:
                que.remove(job_to_remove)
                self.jobsAvailable -= 1
                return 0
                break
            else:
                pass

        if not found:
            return -1

    def modJob(self, jobID, job, command, priority): # will be implemted later
        return 0

    def getJobToRun(self): # retrives next job based on input order & priority
        # & decerements jobs avalible by 1
        # returns -1 if no jobs are available
        for item in self.queues:
            if len(item) != 0:
               job_to_run = item.pop()
               self.queues[3].append(job_to_run)
               self.jobsAvailable -= 1
               return job_to_run.getInfo()

            else:
                pass

        return -1

    def getJobsAvailable(self): # returns nuber of jobs avalible
        return self.jobsAvailable

    def markRunningJobComplete(self, job_ID, result=None): # marks a running job as completed
        found = False
        for item in self.queues[3]:
            if item.id == job_ID:
                found = True
                item.appendResult(result)
                self.queues[4].append(item)
                self.queues[3].remove(item)
                break
       
        if not found:
            return -1
        else:
            return 0

class Job(object):
    def __init__(self, job_ID, job_name, command, working_directory):
        self.id = job_ID
        self.name = job_name
        self.command = command
        self.wDirectory = working_directory
        self.commandResult = None
        return None

    def modJob(self, name=MISSING, command=MISSING, wDirectory=MISSING):
        if name != MISSING:
            self.name = name
        if command != MISSING:
            self.command = command
        if wDirectory != MISSING:
            self.wDirectory = wDirectory
        return 0

    def getInfo(self):
        info = [self.id, self.name, self.command, self.wDirectory]
        return info

    def appendResult(self, result):
        self.commandResult = result
        return 0

if __name__ == '__main__':
    # test code
    q = QueueData()
