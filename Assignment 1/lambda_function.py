import boto3


def lambda_handler(event, context):
    # Initialize the Boto3 EC2 client
    ec2 = boto3.client("ec2")

    print("Starting automated EC2 power management job...")

    # -------------------------------------------------------------------------
    # PHASE 1: Find and STOP instances tagged with Action = Auto-Stop
    # -------------------------------------------------------------------------
    # Filter looking for: Tag Key 'Action' with Value 'Auto-Stop'
    stop_filters = [
        {"Name": "tag:Action", "Values": ["Auto-Stop"]},
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        },  # Only target running instances
    ]

    # Search for matching instances
    stop_response = ec2.describe_instances(Filters=stop_filters)

    stop_instance_ids = []
    for reservation in stop_response["Reservations"]:
        for instance in reservation["Instances"]:
            stop_instance_ids.append(instance["InstanceId"])

    # Execute the STOP command if any instances were found
    if stop_instance_ids:
        print(f"Found instances to STOP: {stop_instance_ids}")
        ec2.stop_instances(InstanceIds=stop_instance_ids)
        print(f"SUCCESS: Issued STOP command for {stop_instance_ids}")
    else:
        print("No running instances found with tag 'Action=Auto-Stop'.")

    # -------------------------------------------------------------------------
    # PHASE 2: Find and START instances tagged with Action = Auto-Start
    # -------------------------------------------------------------------------
    # Filter looking for: Tag Key 'Action' with Value 'Auto-Start'
    start_filters = [
        {"Name": "tag:Action", "Values": ["Auto-Start"]},
        {
            "Name": "instance-state-name",
            "Values": ["stopped"],
        },  # Only target stopped instances
    ]

    # Search for matching instances
    start_response = ec2.describe_instances(Filters=start_filters)

    start_instance_ids = []
    for reservation in start_response["Reservations"]:
        for instance in reservation["Instances"]:
            start_instance_ids.append(instance["InstanceId"])

    # Execute the START command if any instances were found
    if start_instance_ids:
        print(f"Found instances to START: {start_instance_ids}")
        ec2.start_instances(InstanceIds=start_instance_ids)
        print(f"SUCCESS: Issued START command for {start_instance_ids}")
    else:
        print("No stopped instances found with tag 'Action=Auto-Start'.")

    # -------------------------------------------------------------------------
    # Response Payload
    # -------------------------------------------------------------------------
    return {
        "statusCode": 200,
        "body": {
            "StoppedInstances": stop_instance_ids,
            "StartedInstances": start_instance_ids,
        },
    }