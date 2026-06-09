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

Step 1: Provision EC2 Instances and Configuration Metadata

1. Navigate to the AWS EC2 Management Console and launch two separate virtual computing nodes (e.g., t2.micro free-tier instances).

2. Open the Instances workspace list, select the first instance, choose the Tags configuration sub-panel, and select Manage tags.

3. Create a metadata keypair matching case-sensitively:

Key: Action | Value: Auto-Stop

4. Select the second node and apply the matching keypair metadata configuration:

Key: Action | Value: Auto-Start

5. Ensure the first instance is in a Running state, and the second instance is completely Stopped prior to running tests.

# Step 2: Establish the Lambda Execution Security Context
