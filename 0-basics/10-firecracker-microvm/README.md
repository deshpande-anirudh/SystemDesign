AWS Lambda uses **Firecracker microVMs** to efficiently run functions in a secure, isolated, and high-performance environment. Here’s how it works:  

---

### 🔹 **Lambda Execution Flow with Firecracker**  

1️⃣ **Function Invocation**  
   - When a Lambda function is triggered, AWS receives the request and routes it to the appropriate compute infrastructure.  

2️⃣ **Firecracker MicroVM Provisioning**  
   - If a suitable Firecracker microVM isn’t already running, AWS **quickly spins up a new microVM** (in milliseconds).  
   - If an existing microVM is **warm (reused)**, it handles the request immediately.  

3️⃣ **Code Execution in the MicroVM**  
   - The function’s runtime (Python, Node.js, etc.) runs inside the Firecracker VM.  
   - The VM is **isolated**, meaning it has its own kernel, preventing security issues like noisy neighbors.  

4️⃣ **Scaling & Resource Optimization**  
   - Firecracker allows AWS to **run thousands of microVMs per host** due to its **low memory footprint** (~5MB per microVM).  
   - AWS **rapidly provisions or shuts down** VMs based on demand, making Lambda cost-efficient.  

5️⃣ **MicroVM Shutdown & Cleanup**  
   - Once a function is idle (no requests for a while), AWS may **terminate the Firecracker microVM** to free up resources.  
   - If another request comes in, a new microVM may be created (cold start) or an existing one may be reused (warm start).  

---

### 🔹 **Why AWS Chose Firecracker for Lambda**  
✔ **Faster startup than traditional VMs** (~125ms boot time).  
✔ **Better isolation than containers** (each function gets its own microVM).  
✔ **Higher density** (runs thousands of microVMs per host).  
✔ **More cost-efficient & scalable** than full-fledged VMs.  

AWS Lambda **used to** run functions in **containers**, but Firecracker improved security, performance, and scalability.  

---

# Sample 2-sum problem executed on Firecracker VM

To create a Firecracker microVM in Python and execute a "2-sum" problem inside the VM, we can follow these general steps:

1. **Install Firecracker**: We need to have Firecracker running on the host machine. Since you mentioned using Mac and UTM earlier, ensure Firecracker is correctly set up on the machine or inside UTM.

2. **Create a Python script for Firecracker VM setup**: We'll need to set up the Firecracker VM, start it, execute the "2-sum" problem inside the VM, and capture the result.

### **Steps to Set Up and Run Firecracker MicroVM:**

#### **1. Set Up Firecracker with Python**

Make sure you have the **Firecracker API** available. We'll use the `firecracker` Python package to interact with the microVM.

If it's not installed yet, you can install it with:

```bash
pip install firecracker
```

You’ll need the following prerequisites:
- **Firecracker binary** (installed and available in your path).
- **Linux Kernel with Firecracker-compatible config**.
- **Root access** to run Firecracker.

#### **2. Python Code to Create Firecracker MicroVM**

Below is a Python script that demonstrates how to:
1. Create a Firecracker microVM.
2. Start it.
3. Execute the **2-sum** problem in the VM.
4. Retrieve the results.

We will mock the actual computation, but in a real-world use case, you'd create a small binary or script inside the microVM to run your logic.

```python
import os
import subprocess
import json
import time
import requests

# Define the VM configuration
fc_bin_path = '/path/to/firecracker'  # Path to Firecracker binary
fc_sock_path = '/tmp/firecracker.sock'  # Socket path for communication
rootfs_image = '/path/to/rootfs.img'  # Path to root filesystem image
kernel_path = '/path/to/vmlinux'  # Path to kernel image

# Define test cases for 2-sum problem
test_cases = [
    ([2, 7, 11, 15], 9),  # Test case 1: [2, 7, 11, 15] target 9
    ([3, 2, 4], 6),        # Test case 2: [3, 2, 4] target 6
    ([3, 3], 6)            # Test case 3: [3, 3] target 6
]

# Define 2-sum Python function
def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        lookup[num] = i
    return []

# Function to write a 2-sum Python script to a file
def write_two_sum_script():
    script = """
import sys
import json

def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        lookup[num] = i
    return []

# Read input (list of numbers and target)
input_data = json.loads(sys.argv[1])
nums = input_data["nums"]
target = input_data["target"]

# Get result
result = two_sum(nums, target)

# Output result as JSON
print(json.dumps({"result": result}))
    """
    with open("/tmp/two_sum.py", "w") as file:
        file.write(script)

# Function to create and launch a Firecracker microVM
def create_firecracker_vm():
    # Start Firecracker in the background
    fc_process = subprocess.Popen([fc_bin_path, '--api-socket', fc_sock_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the VM to be ready
    time.sleep(2)

    # Set the kernel and root filesystem image
    fc_setup_command = {
        "kernel_image_path": kernel_path,
        "boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
        "rootfs_path": rootfs_image
    }

    # Send the setup configuration to Firecracker API
    requests.put(f'http://localhost:8000/machine-config', json=fc_setup_command)

    # Start the VM
    requests.put(f'http://localhost:8000/actions', json={"action_type": "StartVM"})
    
    return fc_process

# Function to execute 2-sum problem inside Firecracker VM
def execute_two_sum(test_case):
    # Write the 2-sum script to the VM
    write_two_sum_script()

    # Prepare the input
    input_data = {"nums": test_case[0], "target": test_case[1]}
    input_json = json.dumps(input_data)

    # Execute the 2-sum script in the VM
    result = subprocess.run(['python3', '/tmp/two_sum.py', input_json], capture_output=True, text=True)

    # Parse the result
    result_json = json.loads(result.stdout)
    return result_json['result']

def main():
    # Create and start Firecracker microVM
    fc_process = create_firecracker_vm()
    
    # Execute the 2-sum problem for each test case
    results = []
    for test_case in test_cases:
        result = execute_two_sum(test_case)
        results.append(result)
    
    # Print results
    print("Test case results: ", results)

if __name__ == "__main__":
    main()
```

### **Steps in the Code:**
1. **Create and Configure Firecracker MicroVM**:
   - The `create_firecracker_vm()` function starts the Firecracker microVM using a Python subprocess and sends configuration commands to set the kernel and root filesystem.
   
2. **Write a Python script inside the MicroVM**:
   - The script for solving the "2-sum" problem (`two_sum.py`) is written to the VM, which will read input in JSON format and output the results in JSON.
   
3. **Execute 2-sum Problem**:
   - The `execute_two_sum()` function runs the Python script inside the Firecracker microVM for each test case and captures the output.

4. **Send Input and Get Result**:
   - Input data is passed in JSON format, and the result is returned as a JSON object, which contains the indices of the numbers that sum to the target.

### **Test Case Example:**
For a test case like:
```python
([2, 7, 11, 15], 9)
```
The expected output is `[0, 1]`, since `2 + 7 = 9`.

---

### **Important Notes:**
1. **Dependencies**: This example assumes you have Firecracker installed and configured correctly on your machine.
2. **Filesystem**: The root filesystem image (`rootfs.img`) should have Python installed along with any dependencies. You can create a minimal root filesystem for Firecracker with tools like `buildroot` or use pre-built images.
3. **VM Management**: The Firecracker VM setup can vary, and if you're using a different configuration (e.g., UTM), the VM creation and execution might differ.

# Mimic AWS Lambda with a simple function

Awesome! Here’s a **step-by-step plan** to build your **"Mini Lambda" system using Firecracker**:  

---

## 🏗 **Project Overview**  
You'll build a **serverless execution system** where incoming function requests trigger **Firecracker microVMs**, which execute the function and return the result.  

### 🔧 **Core Components:**  
1️⃣ **API Server** – Receives function execution requests.  
2️⃣ **Firecracker VM Manager** – Spawns and manages microVMs.  
3️⃣ **Function Execution** – Runs the provided function inside the microVM.  
4️⃣ **Result Collection & Cleanup** – Retrieves the output and shuts down the VM.  

---

## 🚀 **Step-by-Step Implementation**  

### **Step 1: Install Firecracker & Set Up UTM on macOS**  
Since Firecracker isn't natively supported on macOS, you’ll need **UTM** to run it inside a Linux VM.  

1️⃣ Install **UTM** from [mac.getutm.app](https://mac.getutm.app).  
2️⃣ Download an **Ubuntu Server ISO** and create a VM inside UTM.  
3️⃣ Inside the Ubuntu VM, install Firecracker:  
   ```bash
   curl -fsSL https://raw.githubusercontent.com/firecracker-microvm/firecracker/main/tools/devtool install | bash
   ```
4️⃣ Verify Firecracker works:  
   ```bash
   firecracker --version
   ```

---

### **Step 2: Create a Python API Server (Flask)**
This will receive function execution requests and trigger a Firecracker VM.  

📌 **Install Flask inside your Ubuntu VM**  
```bash
pip install flask
```

📌 **Create `server.py`**
```python
from flask import Flask, request, jsonify
import subprocess
import uuid

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_function():
    data = request.json
    function_code = data.get("code")

    if not function_code:
        return jsonify({"error": "No function code provided"}), 400

    vm_id = str(uuid.uuid4())[:8]
    vm_name = f"vm_{vm_id}"

    # Write function to a file
    with open(f"/tmp/{vm_name}.py", "w") as f:
        f.write(function_code)

    # Spawn a Firecracker VM and execute the function
    subprocess.run(["./run_firecracker_vm.sh", vm_name])

    # Read the output
    try:
        with open(f"/tmp/{vm_name}.out", "r") as f:
            result = f.read()
    except FileNotFoundError:
        result = "Error: Output file not found."

    return jsonify({"output": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

### **Step 3: Create a Firecracker VM Script**
This script will start a Firecracker microVM, copy the function into it, execute it, and return the output.

📌 **Create `run_firecracker_vm.sh`**
```bash
#!/bin/bash

VM_NAME=$1
KERNEL_PATH="/path/to/vmlinux"
ROOTFS_PATH="/path/to/rootfs.ext4"

# Start Firecracker VM
firecracker --api-sock /tmp/firecracker.sock <<EOF
{
  "action_type": "Create",
  "boot-source": {
    "kernel_image_path": "$KERNEL_PATH",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  },
  "drives": [{
    "drive_id": "rootfs",
    "path_on_host": "$ROOTFS_PATH",
    "is_root_device": true,
    "is_read_only": false
  }]
}
EOF

# Copy function file to VM
cp /tmp/$VM_NAME.py /mnt/root/

# Run function inside VM
firecracker --api-sock /tmp/firecracker.sock <<EOF
{
  "action_type": "Exec",
  "args": ["python3", "/root/$VM_NAME.py"]
}
EOF

# Save output
mv /mnt/root/output.txt /tmp/$VM_NAME.out

# Shutdown VM
firecracker --api-sock /tmp/firecracker.sock <<EOF
{
  "action_type": "Shutdown"
}
EOF
```

🔹 **Replace `KERNEL_PATH` and `ROOTFS_PATH` with the actual paths** to your Firecracker kernel and root filesystem.

---

### **Step 4: Test the System**  
Run the Flask API:  
```bash
python3 server.py
```

Send a function execution request using `curl`:  
```bash
curl -X POST http://localhost:5000/run -H "Content-Type: application/json" -d '{
    "code": "print(\"Hello from Firecracker!\")"
}'
```

---

## 🔥 **Next Steps & Optimizations**  
✅ **Warm Starts** – Keep a few VMs running instead of booting a new one every time.  
✅ **Concurrency Handling** – Support multiple function executions at once.  
✅ **Persistent Storage** – Use a better way to pass results back (e.g., shared volume, S3).  
✅ **Security Hardening** – Sandbox execution further to prevent VM escapes.  
