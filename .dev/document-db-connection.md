# Connecting to a DocumentDB Database via MongoDB Compass

This guide will walk you through the steps required to connect to a DocumentDB database using MongoDB Compass. Follow each step carefully to ensure a successful connection.

---

## **1. Download MongoDB Compass**

MongoDB Compass is a GUI tool for interacting with MongoDB or DocumentDB databases.

1. Go to the [MongoDB Compass Download Page](https://www.mongodb.com/try/download/compass).
2. Select your operating system from the options provided (Windows, macOS, or Linux).
3. Download and install the application following the installation prompts for your operating system.

---

## **2. Download the Private Key**

The private key is necessary to establish an SSH tunnel to the EC2 instance hosting the DocumentDB cluster.

1. Access the location where the private key file (`id_ec2-techo`) is stored. This is typically shared via a secure channel.
2. Download the private key file and store it securely on your local machine. Place it in a directory where you have appropriate read permissions, such as `~/.ssh/` on Linux or macOS or a secure folder on Windows.
3. **Ensure proper permissions:**
   - On Linux/macOS, run the following command to set the correct permissions:
     ```bash
     chmod 400 ~/.ssh/id_ec2-techo
     ```

---

## **3. Configure SSH Tunnel Connection in MongoDB Compass**

Follow these steps to set up the SSH tunnel and connect to the DocumentDB database:

### **Step 1: Open MongoDB Compass**

Launch MongoDB Compass on your machine.

### **Step 2: Set Up Connection Parameters**

1. Click on **"New Connection"**.
2. In the **Connection String** field, enter the following URI format:
   mongodb://<user>:<password>@localhost:27017/?tls=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false

Replace the placeholders `<user>`, and `<password>` with the following:

- **User:** Your database username.
- **Password:** Your database password.

### **Step 3: Configure SSH Tunnel**

1. Scroll down to the **"More Options"** section and click on **"SSH Tunnel"**.
2. Fill in the details as follows:
- **SSH Hostname:** `<your-ec2-hostname>` (replace with the EC2 instance's public IP or hostname).
- **SSH Username:** `ec2-user` (or your specific EC2 username).
- **SSH Identity File:** Select the private key file `id_ec2-techo` that you downloaded in step 2.

### **Step 4: Test the Connection**

1. Click the **"Test Connection"** button to ensure everything is set up correctly.
2. If the connection is successful, click **"Connect"** to establish a connection to the DocumentDB database.

---

## **Additional Notes**

- Ensure that the EC2 security group allows inbound SSH traffic (port 22) from your IP.
- Also, verify that the DocumentDB security group allows inbound traffic from the EC2 instance's private IP on port 27017.

If you encounter any issues, double-check the provided details and permissions, or consult your team lead for assistance.

---

Happy coding! 🚀
