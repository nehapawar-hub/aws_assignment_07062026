# Assignment 1 - Automated EC2 Instance Management Using AWS Lambda and Boto3

# Project Objective

This project demonstrates how to automate cloud infrastructure management based on resource metadata. 

It provisions a serverless AWS Lambda function utilizing the Boto3 SDK to automatically control the operational power states (Start/Stop) of Amazon EC2 instances by scanning their assigned tags. 

This approach is commonly used in enterprise environments to optimize cloud computing costs (e.g., stopping non-production instances outside of business hours).

# Architecture & Workflow Overview

Trigger: The Lambda function is manually invoked or attached to an orchestration trigger.

Resource Discovery: The script queries the regional AWS infrastructure framework using filtering parameters to find instances with targeted metadata pairs (Action: Auto-Stop and Action: Auto-Start).

State Execution: * Active instances marked with Action=Auto-Stop receive a shutdown command (stop_instances).

Dormant instances marked with Action=Auto-Start receive a wake-up command (start_instances).

# Step-by-Step Deployment Guide 

**Step 1: Provision EC2 Instances and Configuration Metadata**

Navigate to the AWS EC2 Management Console and launch two separate virtual computing nodes (e.g., t2.micro free-tier instances).

Open the Instances workspace list, select the first instance, choose the Tags configuration sub-panel, and select Manage tags.

Create a metadata keypair matching case-sensitively: Key: Action | Value: Auto-Stop

ScreenShots:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/16dec0e4-aa55-44ac-bcfb-e7ab4a0cc1af" />

Select the second node and apply the matching keypair metadata configuration: Key: Action | Value: Auto-Start

Ensure the first instance is in a Running state, and the second instance is completely Stopped prior to running tests.
    

**Step 2: Establish the Lambda Execution Security Context**

Navigate to the IAM Dashboard and click on the Create Role Button

Define the Trusted Entity framework option as an AWS service, setting the specific use case option targeting Lambda.

Screenshots:

<img width="1910" height="1080" alt="CreateRole" src="https://github.com/user-attachments/assets/d5474c79-179b-462d-a00b-7e8e949c636d" />

Proceed to final configurations, assign a structural name identifier (e.g., EC2ManagementLambdaExecutionRole), and save the asset.

Locate the newly created role profile, choose Add permissions.Create inline policy, open the JSON editor panel, and overwrite it completely with the contents of iam_policy.json

<img width="1920" height="1080" alt="PermissionforRole" src="https://github.com/user-attachments/assets/bcee151e-07bd-4aa3-bf45-d4c06912f30f" />

 **Step 3: Instantiate and Build the Runtime Function**

Access the AWS Lambda Console and select Create function.

Select Author from scratch and input a descriptive function title (e.g., ec2-tag-power-automation).

Set the development runtime compilation layer to Python 3.x.

Expand Change default execution role, select Use an existing role, and connect your newly established IAM Role asset. Click Create function.

<img width="1920" height="1080" alt="Createfunction" src="https://github.com/user-attachments/assets/50ac77f9-3a0e-434e-ad3f-13fd24144229" />

Clear out default syntax layers inside the integrated IDE workspace file (lambda_function.py), paste the script code block from above, and click the Deploy panel control option to save your changes.

**Step 4: Validate Execution and Functional Verification**

Select the configuration drop-menu for testing assets to construct a standard empty validation payload structure.

Select the execution option Test to force invocation.

Verify that the performance logs document successful resource scanning operations and print out the respective targeted instance string IDs

Return to the live EC2 Dashboard View to verify status transitions: the instance holding the Auto-Stop parameter pair should enter a Stopping lifecycle state, while the node holding the Auto-Start token should simultaneously spin up into a Pending state.

<img width="1920" height="1080" alt="output" src="https://github.com/user-attachments/assets/be6aae34-257b-4a24-9e99-9a2f402ba45d" />

# Assignment 2 - Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

# Project Objective

This project automates cloud storage house-keeping and cost optimization. It deploys a serverless AWS Lambda function that utilizes the Boto3 SDK to automatically scan a targeted Amazon S3 bucket and permanently delete any files (objects) that are older than a 30-day retention threshold.

# WorkFlow

Trigger: The Lambda function is invoked manually (or on a schedule using Amazon EventBridge).

Scan: The function uses Boto3 to list all the metadata details for objects stored in your specific S3 bucket.

Evaluate & Delete: The script calculates the age of each file using its LastModified timestamp. If a file is older than 30 days, Lambda fires a delete command, keeping your storage clean and cost-efficient.

**Configuration Files**

1.IAM Permissions Policy(Permission_policy.json)
While the lab instructions allow the generic AmazonS3FullAccess policy, production environments require strict least-privilege access.
Below is the precise JSON configuration required to read and delete objects from S3 and write execution logs.

# Step-by-Step Deployment Guide 

Step 1: Set Up Your S3 Bucket

1.Navigate to the AWS S3 Console and click Create bucket.

2.Give your bucket a unique name (e.g., nehapawar-automated-cleanup-bucket) and click Create bucket.

3.Open your new bucket and select Upload to add several files.

Step 2 : Establish the Lambda Execution Role

1. Navigate to the IAM Dashboard Create Role.

2. Choose AWS service as your trusted entity and select Lambda as the primary use case. Click Next

3. To follow assignment constraints, search for and attach AmazonS3FullAccess. Click Next.

4. Name the role S3CleanupLambdaExecutionRole and click Create role.

Step 3 : Instantiate and Build your Lambda Function

1. Open the AWS Lambda Console and click Create function.

2. Select Author from scratch and name your function s3-bucket-cleanup-automation.
   
3. Set your runtime language selector layer to Python 3.x.

4. Expand Change default execution role, choose Use an existing role, and select the S3CleanupLambdaExecutionRole you just created. Click Create function.

5. Clear out the placeholder template code inside the built-in lambda_function.py file editor, paste the script code block from above, and update line 13 with your true S3 bucket name.

6. Click Deploy to save your changes.

Step 4: Validate and Verify Execution
Click the Test button next to the deploy panel, create a generic placeholder test event, and click Save.

Click Test again to run the function code.

Review your execution logs to verify that the script successfully scanned your bucket files and logged the names of the expired objects.

Head back to your S3 Bucket Console page and refresh it. Your expired objects will be cleared, confirming that your storage automation works perfectly.

# Assignment 3 - Automated Monitoring of Unencrypted S3 Buckets Using AWS Lambda and Boto3

# Project Objective


This project focuses on automating cloud security posture management (CSPM). It establishes a serverless AWS Lambda function using the Boto3 SDK to audit all Amazon S3 buckets in an AWS account.

The function flags buckets that do not have Server-Side Encryption (SSE) enabled, providing automated compliance monitoring to catch security misconfigurations before they leak data.

# WorkFlow Overview

1. Trigger : The Lambda function is manually invoked or scheduled to run routinely.

2. Global Inventory Check: The script contacts the S3 API to fetch an inventory list of every bucket owned by the AWS account.

3. Security Audit Loop: The code loops through each bucket and checks its get_bucket_encryption configuration. If a bucket throws a specific error code (ServerSideEncryptionConfigurationNotFoundError), it means encryption is disabled, and the script prints a warning to the logs.

# Step-by-Step Deployment Guide

Step 1: Set Up Test S3 Buckets
1.Navigate to the AWS S3 Console and click Create bucket.

2.Create 2 or 3 buckets with unique names.

3.Crucial Setup Detail: AWS now enables SSE-S3 encryption by default on new buckets. To simulate an unencrypted bucket for this assignment, open one or two of your test buckets, go to the Properties tab, scroll down to Default encryption, click Edit, select Disable, and save your changes.

Step 2: Create the Lambda IAM Execution Role

1.Navigate to the IAM Dashboard Search Roles and Create role.

2.Set the Trusted Entity to AWS service and the target use case to Lambda. Click Next

3.Search for and check the box next to AmazonS3ReadOnlyAccess to satisfy the assignment requirement. Click Next.

4.Name your role S3AuditLambdaExecutionRole and click Create role.

Step 3: Provision the Lambda Function

1.Go to the AWS Lambda Console and click Create function.

2.Choose Author from scratch and name the function s3-encryption-security-audit.

3.Set your runtime engine setting to Python 3.x.

4.Expand Change default execution role, select Use an existing role, and assign your S3AuditLambdaExecutionRole. Click Create function.

5.Clear out the default snippet inside the lambda_function.py code editor workspace, paste the full audit script from above, and click Deploy.

Step 4: Run the Audit and Verify Logs

1.Click the Test panel button, configure a simple placeholder event profile name, and hit Save

2.Click Test again to execute the security script scan.

3.Review the execution outputs in the Execution result sub-tab. The logs will display your custom report summary and clearly flag the exact names of the unencrypted buckets, confirming that your compliance filter works perfectly!


# Assignment 4 - Automatic EBS Snapshot and Cost Optimization Cleanup Using AWS Lambda

# Project Objective
This project automates data protection policies and storage infrastructure cost control. It establishes a serverless AWS Lambda automation loop driven by the Boto3 SDK to routinely execute point-in-time snapshot copies of designated Amazon Elastic Block Store (EBS) volumes. Simultaneously, it evaluates retention windows to automatically purge any snapshots older than 30 days, optimizing backup overhead costs.

# WorkFlow Overview

Trigger Configuration: The architecture is designed to trigger automatically based on a cron/rate schedule managed by Amazon EventBridge (CloudWatch Events).

Backup Execution: The script initializes the EC2 client API, sending a target payload consisting of the specific VolumeId. AWS processes the state freeze to build a backup block replica.

Lifecycle Management: The script loops through existing snapshot inventory arrays owned by the host account. It compares snapshot creation timestamps (StartTime) against an evaluation 
formula: Cutoff Age = Current Runtime Date} - 30 Days
Any snapshot matching a value older than this boundary is permanently destroyed via a drop call (delete_snapshot).

# Step-by-Step Deployment Guide

Step 1: Track the Target Block Storage Volume ID

1.Navigate to the AWS EC2 Console $\rightarrow$ Elastic Block Store $\rightarrow$ Volumes.

2.Select your targeted storage partition instance block from the main dashboard and copy its identification serial tracker sequence from the properties window (e.g., vol-0123456789abcdef0).

Step 2 : Establish the Lambda Execution IAM Role

1. Open the IAM Dashboard and search IAM Roles and Click on the Create role.

2. Designate AWS service as the core entity type option, matching the service pointer layer to Lambda.

3. Attach the AmazonEC2FullAccess structural security block rule policy script to satisfy lab parameters. Name the file tracking profile EBSBackupLambdaExecutionRole and click Create.

Step 3: Instantiate and Build the Lambda Block Routine

1.Open the AWS Lambda Console and click Create function using Author from scratch.

2.Title your resource identifier (e.g., ebs-automated-snapshot-manager) and set the runtime compiler configuration to Python 3.x.

3.Expand Change default execution role, select Use an existing role, and select EBSBackupLambdaExecutionRole. Click Create function.

4.Paste the complete script from lambda_function.py into the code editor workspace, and replace the placeholder value "vol-xxxxxxxxxxxxxxxxx" on line 13 with your copied volume ID.

5.Click Deploy.

Step 4: Configure the EventBridge Automation Scheduler (Bonus)

1.Inside your Lambda function panel layout view, navigate to the top diagram overview and choose Add trigger.

2.Select EventBridge (CloudWatch Events) from the interface source selector drop-menu.

3.Select Create a new rule, name it EBSWeeklyBackupSchedule, and set your rule configuration toggle type to Schedule expression.

4.Enter an automated cron/rate mapping string (e.g., rate(7 days)) to control execution interval routines, and click the blue Add button.

Step 5: Test Execution and Verify Infrastructure Status

1.Click the Test layout interface button control, save an empty generic profile mock payload trigger template, and execute by clicking Test.

2.Audit operational telemetry scripts inside the execution console print log reports to ensure successful snapshot creation and array tracking actions.

3.Open the EC2 Console Snapshot Dashboard window view panel to check and verify that your automated data block replica has been logged, stored, and tagged safely!

