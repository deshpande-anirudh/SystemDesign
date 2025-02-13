# Distributed job scheduler

- Automatically instantiates and executes the task at specified times. 
- Task:
  - An ETL job (Extract, Transform, Load) on a database
  - Send emails to X people to remind them about the events
  - Remove the expired entries from the database (DynamoDB)
- Job: 
  - An instantiation of the task
  - Made up of 
    - `Task` to be executed (Send event reminder email)
    - `Parameters needed` (To John and 1000 others about event at Seattle Tech convention)
    - `Schedule` (At 1 hour before the start of the event)

# Core requirements

## Above the line
1. A user should be able to schedule the jobs - for immediate, future or re-occurring execution
2. A user should be able to query for their job status 

## Below the line
1. User should be able to cancel and reschedule their jobs

# Non-functional requirements
1. The system should be able to execute the scheduled jobs at time (within 2 seconds)
2. The system should be able to be fault-tolerant 
3. The system should be highly available (availability > consistency)
4. The system should support upto 10K jobs per second
5. The system should execute the job at-least once

## Below the line
1. The system should enforce security policies
2. The system should have CI/CD pipeline

# Core entities
1. Task: The work to be executed
2. Job: An instantiation of the task
3. Schedule: When the job should be instantiated (now, future, or reoccurring - every 1 hour, every day at 12PM)
4. User: User who can schedule the jobs or veiw the status of the jobs

## Cron Expressions Guide

This guide provides an overview of how to set up and interpret cron expressions for scheduling tasks in environments like Unix systems or task schedulers.

---

## 1. Structure of a Cron Expression
Cron expressions typically consist of 5 or 6 fields, depending on the platform. The format for a 6-field expression is:

```
[minute_of_hour] [hour_of_day] [day_of_month] [Month_of_year] [day_of_week]
```

### Fields Breakdown
| Field         | Allowed Values  | Special Characters | Description                        |
|---------------|-----------------|---------------------|------------------------------------|
| **Minutes**   | 0–59          | , - * /             | Minutes when the job will run    |
| **Hours**     | 0–23          | , - * /             | Hour when the job will run       |
| **Day of Month** | 1–31        | , - * ? / L W       | Day of the month                 |
| **Month**     | 1–12 or JAN-DEC| , - * /             | Month                             |
| **Day of Week** | 0–6 or SUN-SAT | , - * ? L #         | Day of the week                   |

---

## 2. Special Characters

| Character | Meaning                                        |
|-----------|------------------------------------------------|
| **\***     | Any value                                      |
| **?**     | No specific value (used in Day fields)         |
| **-**     | Range (e.g., 1-5 means days 1 to 5)            |
| **,**     | List (e.g., MON,WED,FRI)                       |
| **/**     | Step values (e.g., `*/15` for every 15 units)  |
| **L**     | Last (e.g., `L` in day field for last day)     |
| **W**     | Nearest weekday                                |
| **#**     | Nth occurrence of a weekday in a month         |

---

## 3. Example Cron Expressions

| Expression         | Description                                      |
|--------------------|--------------------------------------------------|
| `0 12 * * ?`       | At the 12th minute of every hour                 |
| `0 0 8 * * ?`      | Every day at 8:00 AM                             |
| `0 0 12 1 * ?`     | At noon on the 1st day of every month            |
| `0 0 9-17 * * ?`   | Every hour between 9 AM and 5 PM                 |
| `0 0/30 * * * ?`   | Every 30 minutes                                  |
| `0 0 10 ? * MON-FRI` | 10 AM on weekdays                              |

---

## 4. Testing Cron Expressions
To verify cron expressions:
- Use tools like [Crontab Guru](https://crontab.guru/).
- Test in your terminal with:
  ```bash
  crontab -e
  ```
  Add your cron job and monitor execution.

---

## 5. Best Practices
- **Use `?` carefully:** In `Day of Month` or `Day of Week`, it helps avoid conflicts.
- **Avoid over-scheduling:** Ensure your job intervals don't overwhelm the system.
- **Test locally:** Use logs to debug timing issues.

## CRON vs. ISO 8601 expressions
- CRON: Best for scheduling
- ISO 8601 best for one time execution


# API

## Create a Job
```
POST /job
headers {auth headers etc.}
body {
    task_id: "send_email",
    scheduler: user, # name this as scheduler, not user
    <optional> schedule: cron expression,
    execution_start_time: ISO 8601 date,
    execution_end_time: ISO 8601 date,
    parameters: {
      "to": "a@b.com",
      "subject": "Event reminder",
      ....
    }    
}

-> 200 OK, Job-id
```

## Get the status of a Job
```
GET /Job?id=[Job-id]&execution_start_time=[time]&execution_end_time=[time] -> [QUEUED, SCHEDULED, RUNNING, COMPLETED, ERRORRED]
```

# Data flow 
Essential for high level design
- Align with interviewer on core functionality, before getting to the implementation details
- Roadmap to guide the design decisions

1. User submits a job, with schedule, start time etc.
2. The job is stored in our system, job-id is returned to the user
3. A worker picks up the job at the scheduled time and runs the job
   1. The job is re-tred with exponential backoff (configurable)
4. User can query the job-id and get status of the job






# References
- https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler