from collections import deque
import uuid

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
        self.queues = []    #Creates container for queues
        self.queues.append(HPque)
        self.queues.append(SPque)
        self.queues.append(LPque)
        self.queues.append(runningJobs)
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

        jobsHP = [] #High priority jobs
        jobsSP = [] #standard priority jobs
        jobsLP = [] #Low priority jobs
        jobsRN = [] #runnig jobs

        for item in self.HPque:                 #These loop through ques
            jobsHP.append([item.id, item.name])   #and extract the job name
                                                #plus the jobs ID
        for item in self.SPque:
            jobsSP.append([item.id, item.name])

        for item in self.LPque:
            jobsLP.append([item.id, item.name])

        for item in self.runningJobs:
            jobsRN.append([item.id, item.name])
        jobs = [jobsHP, jobsSP, jobsLP, jobsRN]
        return jobs

    def removeJob(self, jobID): #Removes a job from que and decrements jobs
                                #avalible by 1
        found = False

        for item in self.HPque:
            if item.id == jobID:
                self.HPque.remove(item)
                found = True
                break
            else:
                pass

        for item in self.SPque:
            if item.id == jobID:
                self.SPque.remove(item)
                found = True
                break
            else:
                pass

        for item in self.LPque:
            if item.id == jobID:
                self.LPque.remove(item)
                found = True
                break
            else:
                pass

        if not found:
            return -1
        else:
            self.jobsAvailable -= 1
            return 0

    def modJob(self, jobID, job, command, priority): # will be implemted later
        return 0

    def getJobToRun(self): # retrives next job based on input order & priority
        # & decerements jobs avalible by 1
        # returns -1 if no jobs are available
        if len(self.HPque) != 0:
            job_to_run = self.HPque.pop()

        elif len(self.SPque) != 0:
            job_to_run = self.SPque.pop()

        elif len(self.LPque) != 0:
            job_to_run = self.LPque.pop()

        else:
            return -1
        self.jobsAvailable -= 1
        self.runningJobs.append(job_to_run)
        return job_to_run.getInfo()

    def getJobsAvailable(self): # returns nuber of jobs avalible
        return self.jobsAvailable

    def markRunningJobComplete(self, job_ID): # marks a running job as completed
        try:
            for item in self.runningJobs:
                if item.id == job_ID:
                    self.runningJobs.remove(item)
                    break
                else:
                    pass
        except:
            return -1
        else:
            return 0

class Job(object):
    def __init__(self, job_ID, job_name, command, working_directory):
        self.id = job_ID
        self.name = job_name
        self.command = command
        self.wDirectory = working_directory
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

if __name__ == '__main__':
    # test code
    q = QueueData()
