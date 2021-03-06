# Data transmission SPEC

## Message format

### Layout
```python
(command, data)
```
### Description of items

| Item | Description |
|------|-------------|
| command | A string containing desired command |
| data | An object containing any additional data |

### Example:
```python
('addJob', ['', 'HPtest', 'echo test', 1, '/home/user/dir'])
```

## Job data format

### Layout
```python
[job_uuid, job_name, job_command, priorty, working_directory]
```
### Description of items

| Item | Description | Ussage|
|------|-------------|-------|
| job_uuid | A unique identifier for the job.| Created by server on addition to the que. Afterwards used to track job.|
| job_name | Name of job. | A human readable name for the job|
| job_command | Command to be run from queue.| Defines the action a job will perform.|
| priority| Defines jobs importance. | Decides which queue the job is placed in and its order of execution.|
| working_directory | Directory for job to be run from. | Decides which directory to run command in. |
