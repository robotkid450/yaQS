import yaqsQueue
from sys import exit

q = queue.QueueData()  #create que obj

HP_test_1_add = q.addJob('HPtest', 'bash', 1) # add a serise of test jobs
if not HP_test_1_add  == 0:
    exit(-1)

HP_test_1_add = q.addJob('HPtest2', 'bash', 1)
if not HP_test_1_add  == 0:
    exit(-2)

SP_test_1_add = q.addJob('SPtest', 'bash', 2)
if not HP_test_1_add  == 0:
    exit(-3)

SP_test_2_add = q.addJob('SPtest2', 'bash', 2)
if not HP_test_1_add  == 0:
    exit(-4)

LP_test_1_add = q.addJob('LPtest', 'bash', 3)
if not HP_test_1_add  == 0:
    exit(-5)

LP_test_2_add = q.addJob('LPtest2', 'bash', 3)
if not HP_test_1_add  == 0:
    exit(-6)


# test each function

all_jobs = q.getAllJobs()


first_job_in_HPque = all_jobs[0][0][0]

job_info = q.getJobInfo(first_job_in_HPque)
if job_info == -1:
    exit(-7)


remove_job_return_code = q.removeJob(first_job_in_HPque)
if remove_job_return_code == -1:
    exit(-1)
