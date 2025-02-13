# 2 phase commit

```plantuml
@startuml
actor User
entity "Coordinator" as coordinator
entity "Participant 1" as p1
entity "Participant 2" as p2

User -> coordinator: Start Transaction
coordinator -> p1: Send "Prepare"
coordinator -> p2: Send "Prepare"

note right of p1
  Log: Record Prepare request,
  vote (Yes or No)
end note
note right of p2
  Log: Record Prepare request,
  vote (Yes or No)
end note

p1 -> coordinator: Send Vote (Yes/No)
p2 -> coordinator: Send Vote (Yes/No)

note right of coordinator
  Log: Record responses from participants.
  If all votes are Yes, proceed with Commit.
  If any vote is No, Abort.
end note

coordinator -> p1: Send "Commit" or "Abort"
coordinator -> p2: Send "Commit" or "Abort"

note right of p1
  Log: Record Commit/Abort message.
  Apply Commit or Abort.
end note
note right of p2
  Log: Record Commit/Abort message.
  Apply Commit or Abort.
end note

note right of coordinator
  Log: Record Commit/Abort decision.
  Ensure all participants have received the final decision.
end note

' Scenario: Recovery after failure
actor "Failed Coordinator" as failed_coordinator
failed_coordinator -> coordinator: Recover from failure
note right of failed_coordinator
  Log: Check transaction logs to decide Commit or Abort.
  Re-initiate communication if needed.
end note

' Scenario: Participant failure
actor "Failed Participant" as failed_participant
failed_participant -> p1: Recover from failure
note right of failed_participant
  Log: Check logs to determine Commit or Abort.
end note

@enduml
```

### Explanation of the Diagram:
- **Coordinator**: The central entity that orchestrates the 2PC process. It sends "prepare" requests to participants, collects votes, and then sends the final "commit" or "abort" decision.
- **Participants (P1, P2)**: These are the nodes that hold the data and participate in the transaction. They vote on whether they can commit or need to abort based on their state.
- **Log**: Each entity (Coordinator, Participants) maintains a log for transaction recovery in case of failures.
  - Logs are used to record the actions taken (such as receiving the "prepare" request, voting, and committing/aborting). In case of a failure, the logs help the system recover to a consistent state.

### Notes:
- **Participant logs**: They store actions related to the transaction, including whether they voted "Yes" or "No" and whether the transaction was committed or aborted.
- **Coordinator log**: It records the votes received from the participants and the final decision (commit or abort).
- **Recovery**: If the coordinator or a participant fails during the process, upon recovery, they check their respective logs to determine the transaction's final outcome (commit or abort) and re-initiate the necessary communication.

This diagram represents the sequence of actions and how logs are used to ensure atomicity and consistency in distributed systems with 2PC.