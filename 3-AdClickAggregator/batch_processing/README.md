# Ad Click Aggregation with PySpark

This PySpark project processes and aggregates ad click data, grouping click events by ad IDs and one-minute time windows.

## Features
- **Data Reading:** Reads click data from a CSV file.
- **Data Processing:**
  - Converts `click_time` column to timestamp.
  - Groups ad click events by ad ID and aggregates counts within one-minute time windows.
- **Partitioning:** Repartitions data for optimal distributed processing.
- **Output Writing:** Saves the aggregated data to a specified output directory.

---

## Project Structure
```
.
|-- input/           # Directory containing input CSV file
|-- output/          # Directory for storing output files
|-- ad_click_aggregation.py  # Main script
|-- README.md        # Documentation
```

---

## Prerequisites
- Python 3.x
- Apache Spark
- PySpark library (`pip install pyspark`)

---

## Input Format
The input CSV should have the following columns:
- `ad_id`: Identifier for the advertisement.
- `click_time`: Timestamp when the ad click occurred (in the format `YYYY-MM-DD HH:mm:ss`).

### Example Input
```
ad_id,click_time
ad_1,2025-02-09 12:00:05
ad_2,2025-02-09 12:01:10
ad_1,2025-02-09 12:02:15
```

---

## Instructions

### 1. Prepare Input Data
Ensure your input CSV file is in the `input` directory as `input.csv`.

### 2. Run the Script
Execute the main script:
```bash
python ad_click_aggregation.py
```

### 3. Output
The aggregated results will be saved in the `output` directory with the following columns:
- `ad_id`: Identifier of the ad.
- `window_start`: Start time of the aggregation window.
- `window_end`: End time of the aggregation window.
- `click_count`: Number of clicks in that window.

### Sample Output
```
ad_id,window_start,window_end,click_count
ad_1,2025-02-09 12:00:00,2025-02-09 12:01:00,3
ad_2,2025-02-09 12:01:00,2025-02-09 12:02:00,1
```

---

## Configuration
To change the input/output paths, update these lines in the script:
```python
input_directory = "input"
output_file_path = "output"
```

---

## Performance Note
The following line controls partitioning for parallel processing:
```python
df_flattened = df_flattened.repartition(5)
```
Adjust this value as needed for larger datasets.

---

## Troubleshooting
- **FileNotFoundError:** Ensure the input file path is correct.
- **Multiple Output Files:** Spark writes multiple files by default due to partitioning.

-----------

# DAG in spark

Here's a README that explains the DAG concept in Spark and the steps involved in a typical Spark job:

---

# **README: Understanding DAGs in Spark and Spark Job Execution**

## **Overview**

In Spark, a **Directed Acyclic Graph (DAG)** is a logical representation of the sequence of operations (transformations) applied to the data. The DAG is an important concept as it defines the flow of data processing and task execution in a distributed environment. This document explains how Spark creates and optimizes the DAG, the role of the driver and worker nodes, and the overall flow of a Spark job.

---

## **Key Concepts**

### **DAG (Directed Acyclic Graph)**
- A DAG represents a series of transformations on your data.  
- It is called "Acyclic" because the tasks are ordered in such a way that they do not form any loops.  
- The DAG is created when you perform **transformations** (like `map()`, `filter()`, `groupBy()`) on Spark's **RDDs (Resilient Distributed Datasets)** or **DataFrames**.  
- The DAG is **not executed immediately** but is created as a **plan** to execute the transformations when an **action** (like `collect()`, `count()`, or `save()`) is called.

---

## **Spark Job Execution Flow**

### **1. Spark Driver**
- The **driver** is the main control program that manages the Spark job.
- It performs the following tasks:
  - **Initializes the Spark Session:** Sets up the environment for Spark operations.
  - **Reads Input Data:** Loads the data (e.g., CSV files) into a Spark DataFrame or RDD.
  - **Creates the DAG:** The driver analyzes the transformations in the code and constructs a DAG representing the flow of data operations.
  - **Optimizes the DAG:** Spark optimizes the DAG for efficient execution (such as pipelining operations).
  - **Schedules Tasks:** The driver breaks the DAG into stages and tasks, which are assigned to worker nodes.
  - **Sends Tasks to Worker Nodes:** The driver coordinates execution by sending tasks to the worker nodes for processing.

---

### **2. Spark Worker Nodes**
- **Worker nodes** perform the actual data processing. Each worker is responsible for processing a partition of the data.
- Worker nodes perform the following steps:
  - **Reads Partitioned Data:** Each worker reads a partition of the input data.
  - **Applies Transformations:** Workers apply the transformations specified in the DAG (e.g., `groupBy()`, `map()`, etc.).
  - **Writes Partial Output:** Each worker generates intermediate results and writes them locally.
  - **Sends Results Back to Driver:** After completing their tasks, worker nodes send the results back to the driver.

---

### **3. Collecting Results and Writing Output**
- After the tasks have been executed on worker nodes, the driver:
  - **Collects Results:** Aggregates the results from worker nodes.
  - **Writes Output Files:** Spark writes the final results into multiple partitioned files, e.g., `part-00000.csv`, `part-00001.csv`, etc.

---

## **Example Spark Job (Click Aggregation)**

Here is an example of how a PySpark job might be executed in a job submission:

1. **User Submits PySpark Job**  
   The user submits the job to the Spark cluster.

2. **Driver: Initializes Spark Session and Reads Input Data**  
   The Spark session is created, and input data (e.g., a CSV file) is loaded into a DataFrame.

3. **Driver: Creates DAG for Transformations**  
   The driver constructs a DAG representing the sequence of transformations:
   - Parse `click_time` as a timestamp.
   - Apply a `groupBy(window)` transformation to group clicks by time window.
   - Apply a `count()` aggregation to count the number of clicks in each window.
   - Flatten the nested window structure into a simpler format.

4. **Driver: Optimizes and Schedules Tasks**  
   Spark optimizes the DAG for performance (e.g., combining steps, removing unnecessary computations) and schedules the tasks for execution.

5. **Worker Nodes: Execute Tasks**  
   Each worker node processes a partition of the data:
   - Worker 1 processes Partition 1.
   - Worker 2 processes Partition 2.
   - Both workers apply the transformations (e.g., `groupBy()` and `count()`) locally and return the partial results to the driver.

6. **Driver: Collects Results and Writes Output**  
   After all tasks are completed, the driver collects the results from the worker nodes and writes them to multiple output files (e.g., `part-00000.csv`, `part-00001.csv`, etc.).

---

## **Why is the DAG Important?**

- **Optimized Execution:** Spark can optimize the DAG to minimize data shuffling, combine operations, and improve performance.
- **Fault Tolerance:** If a task fails, Spark can recompute the lost data by using the DAG as a blueprint to re-run only the affected parts of the computation.
- **Parallel Execution:** The DAG allows Spark to execute tasks in parallel across multiple worker nodes, improving speed and scalability.

---

## **Conclusion**
Understanding the DAG is essential for optimizing Spark jobs and troubleshooting issues related to performance and fault tolerance. By leveraging the DAG, Spark can efficiently manage the flow of data and computations, ensuring that tasks are executed in an optimal and fault-tolerant manner.

