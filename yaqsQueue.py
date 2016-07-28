from collections import deque
import uuid

__version__ = 1.0

class QueueData(object): # base object of queue managment
    """docstring for QueueData
       This is a basic multi-priority job queueing system."""

    def __init__(self):
        self.HPque = deque()    #Creates high priority que
        self.SPque = deque()    #Creates standard priority que
        self.LPque = deque()    #Creates low priority que
        self.runningJobs = []   #Creates running job list
        self.jobsAvailable = 0  #Counter of currently avalible jobs

    def pickleCurrentQueue(self, db): # will be implemted later
        return 0

    def unPickleCurrentQueue(self, db): # will be implemted later
        return 0

    def addJob(self, jobName, command, priority): #adds a job to specified que
        # and increments jobsAvailable by 1
        if priority == 1:
            self.HPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
            self.jobsAvailable += 1
            return 0
        elif priority == 2:
            self.SPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
            self.jobsAvailable += 1
            return 0
        elif priority == 3:
            self.LPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
            self.jobsAvailable += 1
            return 0
        else:
            return -1

    def getJobInfo(self, jobID):    # Retrives a jobs info
        for item in self.HPque:
            if item[0] == jobID:
                return item
            else:
                pass
        for item in self.SPque:
                if item[0] == jobID:
                    return item
                else:
                    pass
        for item in self.LPque:
            if item[0] == jobID:
                return item
            else:
                pass
        else:
            return -1

    def getAllJobs(self):   #Gets all job names + IDs

        jobsHP = [] #High priority jobs
        jobsSP = [] #standard priority jobs
        jobsLP = [] #Low priority jobs
        jobsRN = []

        for item in self.HPque:                 #These loop through ques
            jobsHP.append([item[0], item[1]])   #and extract the job name
                                                #plus the jobs ID
        for item in self.SPque:
            jobsSP.append([item[0], item[1]])

        for item in self.LPque:
            jobsLP.append([item[0], item[1]])

        for item in self.runningJobs:
            jobsRN.append([item[0], item[1]])
        jobs = [jobsHP, jobsSP, jobsLP, jobsRN]
        return jobs

    def removeJob(self, jobID): #Removes a job from que and decrements jobs
                                #avalible by 1
        found = False

        for item in self.HPque:
            if item[0] == jobID:
                self.HPque.remove(item)
                found = True
                break
            else:
                pass

        for item in self.SPque:
            if item[0] == jobID:
                self.SPque.remove(item)
                found = True
                break
            else:
                pass

        for item in self.LPque:
            if item[0] == jobID:
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
        return job_to_run

    def getJobsAvailable(self): # returns nuber of jobs avalible
        return self.jobsAvailable

    def markRunningJobComplete(self, job_ID): # marks a running job as completed
        try:
            for item in self.runningJobs:
                if item[0] == job_ID:
                    self.runningJobs.remove(item)
                    break
                else:
                    pass
        except:
            return -1
        else:
            return 0

if __name__ == '__main__':
    # test code
    q = QueueData()
