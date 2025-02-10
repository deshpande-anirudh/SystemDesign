# Tumbling window

A **Tumbling Window** in Apache Flink is like dividing an infinite stream of data into fixed-size, non-overlapping chunks. You can think of it like splitting a long movie into small, non-overlapping scenes. Each scene gets processed independently from the others.

### How Tumbling Windows Work:
- **Fixed Size**: Each window has a **fixed size** (e.g., 1 minute). The events are grouped into these windows, and each window is processed separately.
- **No Overlap**: Once a window finishes, it **doesn't overlap** with the next one. When the next window starts, it only includes the events that arrive during that specific window’s time.
  
### Example:
Imagine you’re tracking clicks on ads:
- **Event Time**: Each click has a timestamp when it occurred.
- **Tumbling Window**: If you define a **1-minute tumbling window**, Flink will group all events that happen from **00:00:00 to 00:00:59** into one window, and all events from **00:01:00 to 00:01:59** into the next window.

### How Flink Executes Tumbling Windows:

1. **Event Arrival**: Data (like ad click events) keep arriving in real-time.
   
2. **Assigning Timestamps**: Each event gets a **timestamp**. Flink uses this timestamp to decide which window the event belongs to.

3. **Window Boundaries**: When the first event arrives, Flink starts looking for a window. It checks if the event belongs to a window (e.g., if the event timestamp falls between **00:00:00 and 00:00:59** for a 1-minute window).

4. **Windowing**: As more events arrive during the same window, they get added to that window. Flink keeps all events in memory (or state) until the window ends.

5. **Window Closing**: Once the window is over (e.g., at **00:01:00**), Flink processes the window’s data, typically applying some operation like counting or averaging. 

6. **Output the Result**: The result of the processed window (e.g., number of clicks per ad in the 1-minute period) is sent to an **Output Sink** (like a database or dashboard).

7. **Next Window**: As soon as one window is done, the next one starts, and the process repeats.

### How It Looks in Code:
If you define a 1-minute tumbling window, Flink will:
- Group events into windows that last 1 minute.
- Apply operations (like counting ad clicks) on those windows once they're full.
- Output the results at the end of each window.

For example:
```python
result_stream = (
    watermarked_stream
    .key_by(lambda value: value[0])  # Key by ad_id
    .window(TumblingEventTimeWindows.of(Time.minutes(1)))  # 1-minute window
    .reduce(lambda a, b: (a[0], a[1] + b[1]))  # Aggregation (counting clicks)
)
```

### Visualization:
- **[00:00:00 - 00:00:59]** -> Window 1 (aggregation result here)
- **[00:01:00 - 00:01:59]** -> Window 2 (new aggregation result)
- **[00:02:00 - 00:02:59]** -> Window 3 (new aggregation result)
- And so on.

### Summary:
A tumbling window divides the stream into **non-overlapping chunks**. Flink processes each window independently and produces a result once each window is completed. This makes it easier to compute aggregate functions (like counting, summing, or averaging) over time.

# Watermarks

Watermarking in **Flink** is a mechanism used to handle **event time** processing, ensuring that events are processed in the correct order, even if they arrive out of order. It is a critical part of stream processing when working with time-based windows, such as tumbling or sliding windows.

### Why Watermarking is Needed:
- **Event Time** is the timestamp that comes with the event itself, not the time it was processed by Flink. In many real-world systems, events can arrive out of order or with a delay.
- To compute correct window results (such as aggregation counts or sums), Flink needs to know when to close a window and compute results, but it can't wait forever for all events to arrive, especially when events might arrive late or be out of order.
  
Watermarks are used to tell Flink when it can safely process the events in a window, based on the assumption that any event with a timestamp earlier than the watermark will not arrive later.

---

### How Watermarking Works:

1. **Event Time**:
   - Events have timestamps (e.g., `12:00:05` for an ad click event).
   - In **Flink**, windows are defined based on event time (not processing time), meaning the time the event actually happened, not when it was processed.

2. **Watermark**:
   - A watermark represents the **progress of event time** and indicates that **all events with a timestamp less than the watermark have been processed**.
   - For example, if the watermark is at **`12:01:00`**, it means Flink has processed all events that occurred before **`12:01:00`**, and any event that arrives later will belong to the next window.

3. **Late Events**:
   - If an event arrives **after** the watermark for its window has passed, it's considered a "late event."
   - **Flink** can still process late events if they are within a defined **allowed lateness** period (e.g., 5 minutes). After this period, late events will be discarded.

4. **Watermark Generation**:
   - Watermarks are usually generated based on **event timestamps**. Flink offers different watermark strategies to suit various use cases.
   
   **Strategies for Watermark Generation**:
   
   - **Monotonous Timestamps**: The watermark increases monotonically with time. This is useful when you know that events will arrive in increasing timestamp order, but may still arrive with some delay.
   - **Punctuated Watermarks**: The watermark is generated based on certain conditions (like a specific event in the stream).
   - **Periodic Watermarks**: Watermarks are generated periodically (e.g., every 100 ms), based on the event timestamps seen so far.

---

### Example Walkthrough:

#### Scenario:
- Events are arriving with different timestamps. Some are arriving on time, while others are delayed.

#### Sample Events:
1. **Event 1**: `ad_1` at **12:00:05**
2. **Event 2**: `ad_1` at **12:00:20**
3. **Event 3**: `ad_1` at **12:01:00**
4. **Event 4**: `ad_2` at **12:02:00**
5. **Event 5**: `ad_1` at **12:01:30** (late event)

#### Watermark Behavior:
- At the time Flink processes **Event 3** (`12:01:00`), it might set a watermark at **`12:01:00`**, indicating that all events up to this time have been processed.
- **Event 5** (`12:01:30`) arrives after the watermark, but if **allowed lateness** is configured to 5 minutes, Flink can still process this event and include it in the **12:01:00 - 12:02:00** window.
- **Event 4** (`12:02:00`) would likely be processed in the next window, **12:02:00 - 12:03:00**, because it has arrived after the watermark for the previous window.

---

### Watermarking in Action with Tumbling Windows:
In your example with ad-click aggregation, here's how watermarking works with **tumbling windows**:

1. Flink processes each ad-click event, assigning it a timestamp.
2. It generates watermarks based on event time to track progress.
3. As new events arrive, Flink uses the watermark to close the current window and start the next one.
4. Late events may still be processed if they arrive within the allowed lateness, otherwise they are discarded.

---

### Key Points:
- **Watermarks** allow Flink to manage the complexities of **out-of-order events** and ensure accurate time-based processing.
- They tell Flink when it can safely process a window, ensuring correctness when computing aggregates, such as sum, count, etc.
- **Late events** can be handled by defining an **allowed lateness** period, but after that, the event is discarded.

Watermarking is an essential concept for ensuring **correct event-time processing** in stream processing systems like Flink.

# Visualize tumbling window and watermarks

![](https://plantuml.online/png/bLInRi8m4Dtz5ISceWgKE6N9qAMgkdIeL2IMIjK19bXDR6GRKF--LpjW750LbiG-l_VkteiSN3bjOFHo4Ch1XpC2sn6W1Ly8UqOhwNvWj40dJ8lcMwhQWouBPzHytouRAi12ghK-Uk2f5agCNQZ3v2dHWGfUXHA6IjqKC9UjY1ZBb7O2ZAot3lIcJuuuG2EWxhJMi4HBJwr0U557ejPXkxEC9H8qJpekYJutsehE4E26qB7FbPihTd1HL83hhmAGbhpAyogV3MJoFfFd0vbboYo8FC3j6L15LWzqanOM1OmxVpbCpWBPftetUYLizr4jZFraAxrNhe8o6nhZexV4JvR-EWraplfXb3cCtyXhEC_kJuRVbmmFoHGn6VvFCW_1PnSGf_66Tof39nuxbMcdQ3lz3WMrIQ_NxJ33vTe5DRfMKlaBHMyAw80DcUZz1x9fQ2fkqO_IRKa2cqOVQTiGKD79bFq2)

# How Apache flink works? 

### 1. **User submits a job:**
   - Imagine you have a job where you want to count how many ad clicks happen every minute (like your ad-click aggregation). The user submits this job to Flink.
   - **JobManager** (like the boss) gets this job and decides how to break it into smaller tasks.

### 2. **JobManager orchestrates the work:**
   - The **JobManager** is like the job organizer. It takes your job, **divides it into smaller tasks** (like counting clicks), and assigns them to the **TaskManagers**.
   - **JobManager** also keeps track of progress and can restart tasks if something goes wrong.

### 3. **TaskManager executes tasks:**
   - The **TaskManager** is like the worker who does the actual work.
   - The **TaskManager** has **task slots** (think of them as workstations). Each slot is a place where a single task can run.
   - **TaskManager** runs the tasks in parallel (imagine many workers handling different parts of the job at once), which helps scale the job to handle millions of events quickly.

### 4. **How the data stream is processed:**
   - The **DataStream** represents the data coming in (like the ad clicks you want to count). It is constantly streaming in, and Flink processes it step by step.
   - When the data (ad clicks) comes in, it's distributed to different **TaskManagers**.
   - Each **TaskManager** processes the data:
     - It might **map** (transform) the data (e.g., get the ad ID and timestamp).
     - It could **reduce** (aggregate) the data (e.g., count how many times each ad was clicked).
     - Or it might do other things like **windowing** (grouping data by time).
   - All this processing happens in parallel across **TaskManagers**.

### 5. **Slots and parallelism:**
   - Think of **task slots** as "workstations." Each **TaskManager** has a certain number of these slots, which allow it to handle multiple tasks at the same time.
   - If you have a lot of data (like 1 million ad clicks per second), Flink will use many **TaskManagers** and slots to divide the work into smaller chunks and process them simultaneously.
   - The more slots you have, the more parallel tasks can run, helping process the data faster.

### 6. **The output:**
   - Once the data is processed, the **TaskManager** can send the results back.
   - The output could be something like: **"Ad 1 was clicked 50 times in the last minute"**.
   - These results can be printed out, saved to a database, or sent to another system.

### Simple Flow Summary:
1. **User** submits job to Flink.
2. **JobManager** divides the job into smaller tasks and assigns them to **TaskManagers**.
3. **TaskManagers** process the incoming data using **task slots** (parallel tasks).
4. **TaskManagers** do things like map, reduce, and aggregate the data.
5. The **output** (e.g., count of ad clicks) is produced after processing.

This whole system is designed to **scale**, so even with huge data (like millions of clicks per second), Flink can handle it by distributing the tasks across many **TaskManagers** and **task slots**.

# Flink execution visualization

![](https://plantuml.online/png/VL9BRzim3BxhLn0z537GTVST1WHzO2qGD4WsxB8B8pEk45ao92fez-j7oOxjf4Dlehw7Ff92pJx0hqX1aMF3xt3rx7UmGeSD1LYiC3A5wWemWW33_SZzYV4maN_xS3YHC_9VzjPwBeny6A5xP8Gj1yAsWBdkov7oQ8qxm9rDEL4X3UUHyPAuImnRuHMyhtEfL6uHldoVDG7VO9jshM7edGLHC_IIkyOG2QxXfMFJchy43s-a4nllO6tHNKXdxOlstaGEPfUO2X1X8MveBTc-hfIQ2qIVXoF2POocSOK4xFkH5KWequY4k25DvYYXZZ8CyL_MCXsZi_MCDna_EUrRuneu4GVbw3xmri5hYlq-yc_eRkIfEccgHkPvgnlY5Dn9HxLSn6J5-BB3QJbv4UHgM3PDe0Pv4i62RflRco7XdK-IiBeqEjlIXZeVE3ylNfBxA_mW3BmZb0YVhKXUrA_IcHrNzEH0ewpSxs6FngP07zSq_C3SWKQHOcx3Mg-b2rZvG6MEOcRsu8XggYjrqdo88A6Fffxhb79UZ89fNZddEEVFgvYVZtzSYdcfhGpFT9A7yyU9nUeV)