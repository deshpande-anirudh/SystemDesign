Storage systems fall into 3 categories: 

# Block storage
- Block = 4KB unit (earlier 512 bytes).
- This is pure binary and non human-readable
- In the cloud, services like AWS EBS (Elastic Block Store) and Google Persistent Disks offer block storage solutions.

## Video File Storage on the laptop

### 🔧 How Video Storage Works
- A video file (e.g., 2GB) is divided into **blocks** on your computer's disk.
- These blocks are typically 4 KB each and stored in different locations on the disk.
- The file system (NTFS, APFS, ext4) keeps track of where each block is stored.

### Example Representation
```
[Video File Stored on Disk]
Block1 -> Block2 -> Block3 -> ... -> Block524288
```
- Blocks may not always be sequential but the file system knows their order.

## 🎥 How Video Playback Works
1. **File System Reads the Blocks:**
   - The file system locates all blocks and sends data to the media player.

   ```
   [File system combines blocks]
   "Here’s the complete video data!"
   ```

2. **Data Loaded into RAM:**
   - Instead of loading the entire file, only the first part of the video is buffered.

   ```
   [█████     Buffering...]
   "Let’s start playing while I grab more!"
   ```

3. **Decoding by Media Player:**
   - The media player (like VLC) decodes compressed audio and video using codecs (e.g., H.264).

   ```
   🎵 Decodes audio   🎥 Decodes video
   "Keep syncing sound and visuals!"
   ```

4. **Continuous Streaming:**
   - The player keeps fetching and decoding more blocks in the background for seamless playback.

   ```
   ✨ No interruptions — Enjoy your movie! 🎬
   ```

## 🛠 Key Components in Playback
- **File System:** Manages the locations and order of data blocks.
- **RAM:** Temporarily stores chunks of video for fast access.
- **Media Player:** Decodes and synchronizes video and audio streams.
- **Codec:** A compression algorithm that reduces file size and enables playback.

## 📚 ELI5 Analogy
Imagine a LEGO set:
- Blocks are scattered across the room (disk).
- A guide (file system) knows where all pieces are.
- You build part of it (buffer) to enjoy your creation while fetching more pieces.

-----

# File storage (vs. Block Storage)

Here’s a simple **README** that explains **file storage**, how files are stored in a **hierarchical structure**, and contrasts it with **block storage**:

---

# **File Storage vs Block Storage**

### **File Storage**

File storage is a system for storing data in a way that mimics how we organize files on our local computers. Data is stored in **files** and organized into **folders** (also called directories), forming a **hierarchical structure**.

#### **How Files Are Stored**

1. **Hierarchical File System**:  
   File storage systems organize files in a **folder structure**. You can think of this structure like a **directory tree**, where folders can contain files or other folders. Example:
   ```
   /Videos
     /Movies
       MyMovie.mp4
   ```

2. **Breaking the File into Blocks**:  
   When you store a large file, such as a video, it’s too big to fit into a single storage block. The storage system **splits the file into smaller pieces** called **blocks**. These blocks are then stored in **different locations** (like separate disks or servers).

3. **Keeping Track of Blocks**:  
   The system keeps an **index** (map) that records where each block of the file is stored. This allows it to reconstruct the original file when needed.

4. **Accessing the File**:  
   When you want to access the file (e.g., watch the movie), the system looks up the index to find where all the blocks are stored. It then puts all the blocks together and presents the file as a whole.

#### **Key Characteristics of File Storage**:
- **Hierarchical structure**: Organizes files into folders, making it easy to manage and navigate.
- **Files and directories**: Files are stored as part of a directory structure, so you can easily organize and access them.
- **Block-level storage under the hood**: Large files are broken down into smaller blocks, which are managed by the system.
  
---

### **Block Storage**

Block storage is a lower-level storage system that treats data as raw blocks rather than files. It is used for systems where data is stored as independent blocks that can be directly accessed.

#### **How Blocks Are Stored**

1. **Raw Blocks**:  
   Data in block storage is stored in **blocks** of data with no file system structure. Each block is a fixed-size chunk of data that can hold part of a file or other types of data.
   
2. **No Folder Structure**:  
   Unlike file storage, block storage doesn’t have folders or files. It is just a collection of **raw blocks**, and each block has a unique identifier (block address).

3. **Direct Access**:  
   The system allows direct access to each block of data. Applications interact with individual blocks without needing to worry about the larger file structure.

#### **Key Characteristics of Block Storage**:
- **No hierarchical structure**: Data is stored as raw blocks, without files or directories.
- **Low-level storage**: Data is accessed by addressing individual blocks rather than working with file paths.
- **Ideal for databases and high-performance applications**: Block storage is commonly used for applications that need fast, low-latency access to data, such as **databases** or **virtual machines**.

---

## **File Storage vs Block Storage: Key Differences**

| Feature                    | **File Storage**                        | **Block Storage**                        |
|----------------------------|-----------------------------------------|-----------------------------------------|
| **Structure**               | Hierarchical (files and folders)       | Raw blocks without file hierarchy      |
| **Data Organization**       | Files stored in directories            | Data stored in blocks (no file system) |
| **Access Method**           | Access files via paths and directories | Access data via block addresses        |
| **Use Cases**               | Shared file systems, media storage, collaboration, home directories | Databases, virtual machines, applications requiring fast, low-latency access |
| **Management**              | Easy to manage with file/folder system | Requires direct management of blocks   |
| **System Interface**        | File system interface (NFS, SMB)       | Block-level interface (raw device access) |
| **Performance**             | Good for file-based applications       | High-performance, low-latency access   |
| **Scalability**             | Scales with storage capacity           | Scales by adding more blocks or volumes |
| **Example Services**        | AWS EFS, Google Cloud Filestore, NFS    | AWS EBS, Google Cloud Persistent Disks, SAN |

---

## **When to Use File Storage**

- **Shared File Access**: When you need multiple users or systems to access the same file system (e.g., shared documents or media files).
- **Traditional File Systems**: When your applications require a traditional file system interface (e.g., files, directories).
- **Collaboration**: If multiple users need to access and modify files concurrently.
- **Simplicity**: When you want an easy way to organize and manage files with folders and paths.

## **When to Use Block Storage**

- **Databases**: When you need fast access to individual blocks for databases that require low-latency read/write.
- **Virtual Machines**: When storing operating system files and virtual machine data, as block storage provides high performance and flexibility.
- **High-Performance Applications**: For applications where you need direct access to raw data with little overhead, such as gaming, media processing, or large-scale data computations.

---

# Object storage

### 1. Introduction to Object Storage
- Object storage, such as **Amazon S3** (Simple Storage Service), is designed to handle massive amounts of unstructured data. 
- Unlike traditional file systems that use a hierarchical directory structure, object storage treats each file as an independent object with a unique identifier. 
- This structure allows **unlimited scalability** and **high availability**, making it ideal for storing large amounts of data such as videos.

Each object is stored with:
- **File data** (in your case, the video content)
- **Metadata** (file name, size, permissions)
- **Unique identifier** (e.g., object key)

Object storage is efficient for storing large-scale data like videos, as it doesn't suffer from the performance bottlenecks seen in traditional file storage systems.

---

### 2. Storing Large Video Files in S3
When you upload 100,000 videos (5 GB each) to an object storage service like **S3**, the files are stored as individual **objects** within a **bucket**.

Each video is uploaded as an object, and S3 automatically assigns a **unique object key** (filename) to each video, such as `video_0001.mp4`, `video_0002.mp4`, etc.

#### Key Steps in Uploading:
1. **Create a Bucket**: A bucket is a container for your objects. You can create a bucket (e.g., `my-videos-bucket`) to hold all the video files.
   
2. **Upload Videos**: Upload each video file using an SDK or AWS CLI. Amazon S3 supports multi-part uploads, which allows you to upload large files in chunks.

3. **Metadata**: Each uploaded video is stored with associated metadata, such as its size, last modified time, and custom tags.

---

### 3. File Distribution in Object Storage
In **Amazon S3**, large files are **split** into smaller **chunks** or **parts** during the upload process. Each chunk is distributed across multiple **servers** and **availability zones** to achieve high availability and durability.

#### How the Distribution Works:
1. **File Chunking**: For a 5 GB video file, S3 might split it into 10 smaller parts of 500 MB each. Each chunk is treated as a separate object during the upload process.
   
2. **Data Distribution**: Each chunk is distributed across multiple servers (physical machines) in different **availability zones** within a region. This ensures that the data is **distributed** and that a single server failure won't result in data loss.

3. **Replication**: To ensure **durability**, S3 replicates each chunk to multiple locations within different **availability zones**. This guarantees **99.999999999% durability (11 nines)**.

4. **Object Metadata**: The file metadata (size, permissions, etc.) is stored and managed separately from the actual video data, allowing S3 to track the location of each chunk and efficiently manage the file.

---

### 4. Scalability and Durability
One of the major advantages of using object storage for storing large video files is the **scalability** and **durability** it offers.

#### Scalability:
- **Infinite Scalability**: Object storage scales automatically to accommodate the increasing volume of data. As you add more videos or customers, S3 will handle the load by automatically distributing the data across additional servers and availability zones.
- **Load Balancing**: S3's architecture supports **load balancing** to handle simultaneous requests from multiple users accessing the videos at once. This is crucial for large-scale services like **video streaming platforms**.

#### Durability:
- **Replicas**: S3 automatically replicates each chunk across multiple data centers. Even if one chunk becomes unavailable due to server failure or a network issue, the replica will be available from another availability zone.
- **11 Nines of Durability**: S3 ensures your videos are stored with **99.999999999% durability**, meaning your data is extremely unlikely to be lost.
  
---

### 5. Retrieving Files
When a user requests a video (e.g., `video_0001.mp4`), S3 uses its indexing and metadata systems to **reassemble the file** from its chunks and serve it efficiently.

#### How Retrieval Works:
1. **Metadata Lookup**: S3 looks up the metadata associated with the video object (e.g., `video_0001.mp4`), which includes information on where each chunk is stored.
   
2. **Chunk Retrieval**: S3 retrieves the chunks from their respective servers and **reassembles the video file** before delivering it to the user.
   
3. **Speed and Optimization**: S3 utilizes features like **Amazon CloudFront (CDN)** to cache videos at edge locations closer to customers, minimizing latency and improving retrieval speed.

---

### 6. Best Practices for Storing Large Video Files
- **Use Multipart Upload**: For large video files, **multipart upload** allows you to upload the file in parts. This helps reduce upload times and provides fault tolerance (you can resume from the last successfully uploaded part in case of failure).
  
- **Organize by Prefixes**: Even though S3 doesn’t use a true directory structure, you can organize videos by **using prefixes**. For example, you might store videos in different "folders" using naming conventions:
  - `2025/movies/video_0001.mp4`
  - `2025/movies/video_0002.mp4`
  
  This helps you logically organize your data and manage it effectively.

- **Enable Versioning**: Enable **versioning** on your S3 bucket to maintain different versions of your video files. This helps protect against accidental overwrites or deletions.

- **Access Control**: Use **IAM roles and policies** to control access to the videos. You can define who can view or upload videos to the bucket.

---

### 7. Visualization of File Chunking

Here is a simple text visualization of how a 5 GB video file is divided into smaller chunks and stored in object storage.

#### Example: Storing a 5 GB Video (`video_0001.mp4`)

1. **Original File**: A 5 GB video file.
   
2. **File Splitting into Chunks**:
   ```
   video_0001.mp4 (5 GB) -> Chunk 1 (500 MB), Chunk 2 (500 MB), Chunk 3 (500 MB), ..., Chunk 10 (500 MB)
   ```

3. **Distributed Storage**:
   - Each chunk is stored in multiple **availability zones** across different **servers**.
   - **Replication** ensures multiple copies of each chunk across different locations for durability.
   
4. **Storage** Example:
   ```
   -----------------------------
   | Bucket: my-videos          |
   -----------------------------
   | Object: video_0001.mp4     |
   | Metadata: (file name, size)|
   | Chunks:                    |
   |  - Chunk 1 (500 MB):       |
   |      Stored in Node A, AZ1 |
   |  - Chunk 2 (500 MB):       |
   |      Stored in Node B, AZ2 |
   |  - Chunk 3 (500 MB):       |
   |      Stored in Node C, AZ3 |
   |  - ...                     |
   |  - Chunk 10 (500 MB):      |
   |      Stored in Node D, AZ1 |
   -----------------------------
   ```

5. **Chunk Retrieval**:
   - When you retrieve `video_0001.mp4`, S3 looks up the metadata to find the location of each chunk.
   - It assembles the chunks from the respective locations and serves the file to the user.


### Reasons to Prefer EFS Over S3:
- **S3**: While S3 integrates well with EC2, it doesn't support being mounted directly as a file system. To use S3 for real-time application access, you would typically interact with it via **AWS SDKs** or **APIs**, which could add complexity depending on the application.

- **Ease of Managing Files with Directory Structure**
   - **EFS**: It allows you to manage files in a **hierarchical directory structure**, much like a traditional file system. You can have **folders** and **subfolders** that are easy to navigate and manage, and you can interact with the files using traditional tools and commands.
   - **S3**: S3 uses a **flat object storage model**. While you can simulate directories with prefixes (e.g., `folder1/file.txt`), it doesn’t offer the same level of native file management as a true file system.

- **Simultaneous Read/Write Access**
   - **EFS**: EFS supports **simultaneous read and write access** from multiple EC2 instances, which is crucial for shared workloads like content management systems, web apps, or home directories for users in a multi-instance environment.
   - **S3**: S3 provides eventual consistency and is primarily read-focused. While it supports **strong consistency** for **newly written data**, its write operations are not as fast and concurrent as those in a true file system, especially when you need multiple instances to write to the same object simultaneously.

- **File Locking**
   - **EFS**: Supports **file locking** to prevent conflicts when multiple processes try to access or modify the same file simultaneously. This is useful for many applications that need synchronized access to shared files.

### When to Choose EFS Over S3:
- **Shared File Access**: If you need to **share files** between multiple EC2 instances, especially for workloads that require low-latency and frequent file access.
- **Real-time Applications**: If your application requires **real-time access** to files with the ability to **read/write concurrently** (e.g., databases, CMS, web applications).
- **POSIX Compliance**: If your application needs to interact with files using **POSIX file system semantics** (e.g., file permissions, locking).
- **Low-latency Operations**: If your application needs **low-latency access** to data, such as in media processing or analytics.


-----

### References
1. https://bytebytego.com/courses/system-design-interview
2. https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321