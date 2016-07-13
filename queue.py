from collections import deque
import uuid


class QueueData(object):
    """docstring for QueueData
       This is a basic multi-priority job queueing system."""

    def __init__(self):
        self.HPque = deque()    #Creates high priority que
        self.SPque = deque()
        self.LPque = deque()

    def pickleCurrentQueue(self, db):
        pass

    def unPickleCurrentQueue(self, db):
        pass

    def addJob(self, jobName, command, priority):   #adds a job to specified que

        if priority == 1:
            self.HPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 2:
            self.SPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        elif priority == 3:
            self.LPque.append([str(uuid.uuid4())[:8], jobName, command, 0])
        else:
            print('Bad Priority, job dropped')
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

        for item in self.HPque:                 #These loop through ques
            jobsHP.append([item[0], item[1]])   #and extract the job name
                                                #plus the jobs ID
        for item in self.SPque:
            jobsSP.append([item[0], item[1]])

        for item in self.LPque:
            jobsLP.append([item[0], item[1]])

        return jobsHP, jobsSP, jobsLP


    def removeJob(self, jobID): #Removes jobs from que

        found = False

        for item in self.HPque:
            if item[0] == jobID:
                print(item)
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
            return 0


    def modJob(self, jobID, job, command, priority):
        pass


if __name__ == '__main__':
    #temporary testing code
        q = QueueData()
        q.addJob('HPtest', 'bash', 1)
        q.addJob('HPtest2', 'bash', 1)
        q.addJob('SPtest', 'bash', 2)
        q.addJob('SPtest2', 'bash', 2)
        q.addJob('LPtest', 'bash', 3)
        q.addJob('LPtest2', 'bash', 3)

        a = q.getAllJobs()

        print('a 0 0', a[0][0][0])
        i = a[0][0][0]

        b = q.removeJob(i)
        print('b ', b)

        n = q.getAllJobs()
        print('jobs after removal', n)
