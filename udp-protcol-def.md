# UDP message SPEC

## job data format
| Item | Description | Ussage|
|------|-------------|-------|
|priority| Defines jobs importance. | Decides which queue the job is placed in and its order of execution.|
| job_uuid | A unique identifier for the job.| Created by server on addition to the que. Afterwards used to track job.|
| job_name | Name of job. | A human readable name for the job|
| job_command | Command to be run from queue.| Defines the action a job will perform.|


```python
[priorty, job_uuid, job_name, job_command]
```

## UDP message format

First message:
```python
[message ID, number of messages, command]
```
Following messages
```python
[ Message ID, Message number, data ]
```
ACK responce
```python
('ACK',Message ID)
```
