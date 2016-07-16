# UDP Message SPEC

## UDP message format

### First message:
#### Layout
```python
[message ID, number of packets, data]
```

#### Description of items
| Item | Description | Ussage|
|:------:|:-------------:|:-------:|
| message ID | A unique identifier for each group of messages. | Allows the recipient to groups related messages|
| number of packets | An integer containing the total number packets in the message.| Used be recipient to calculate missing messages.|
| data | The payload of the Message.| Used to send and receive data.|


### Following messages:

#### Layout
``` python
[ message ID, Packet number, data ]
```
#### Description of items
| Item | Description | Ussage|
|:------:|:-------------:|:-------:|
| message ID | A unique identifier for each group of messages. | Allows the recipient to groups related messages|
| packet number | An integer containing the current message's number. | Used be recipient to calculate missing messages.|
| data | The payload of the Message.| Used to send and receive data.|

> NOTE: Follow-up messages only required for messages that are larger than the socket buffer.


### NACK responce:
#### Layout
```python
('ACK',message ID, missing messages)
```
#### Description of items
| Item | Description | Ussage|
|:------:|:-------------:|:-------:|
| ACK | String containing 'ACK'. | Signals sender the recipient has received a message or messages.|
| message ID | A unique identifier for each group of messages. | Allows the recipient to groups related messages|
| missing messages | A string containing a CSV list of messages not received. | Used to determin which messages need resent.|

---

## Job data format

### Layout
```python
[priorty, job_uuid, job_name, job_command]
```
### Description of items

| Item | Description | Ussage|
|------|-------------|-------|
|priority| Defines jobs importance. | Decides which queue the job is placed in and its order of execution.|
| job_uuid | A unique identifier for the job.| Created by server on addition to the que. Afterwards used to track job.|
| job_name | Name of job. | A human readable name for the job|
| job_command | Command to be run from queue.| Defines the action a job will perform.|
