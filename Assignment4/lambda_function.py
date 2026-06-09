import datetime
from datetime import timezone
import boto3


def lambda_handler(event, context):
    # Initialize the EC2 client using Boto3
    ec2 = boto3.client("ec2")

    # =========================================================================
    # CONFIGURATION SETTINGS
    # TODO: Replace 'vol-xxxxxxxxxxxxxxxxx' with your actual Volume ID from Step 1
    # =========================================================================
    VOLUME_ID = "vol-0a6511c72c8fff428"
    RETENTION_DAYS = 30

    print(f"Starting automated EBS snapshot job for volume: {VOLUME_ID}")

    # -------------------------------------------------------------------------
    # PHASE 1: Create a fresh snapshot of the specified volume
    # -------------------------------------------------------------------------
    try:
        new_snapshot = ec2.create_snapshot(
            VolumeId=VOLUME_ID,
            Description=f"Automated backup created by Lambda. Volume: {VOLUME_ID}",
        )
        snapshot_id = new_snapshot["SnapshotId"]
        print(f"SUCCESS: Created new snapshot -> {snapshot_id}")

        # Optional: Tag the new snapshot so you know it was made via automation
        ec2.create_tags(
            Resources=[snapshot_id],
            Tags=[{"Key": "CreatedBy", "Value": "LambdaAutomation"}],
        )

    except Exception as e:
        print(f"ERROR: Failed to create snapshot for volume {VOLUME_ID}: {e}")
        return {"statusCode": 500, "body": "Snapshot creation failed."}

    # -------------------------------------------------------------------------
    # PHASE 2: Scan existing snapshots and delete those older than 30 days
    # -------------------------------------------------------------------------
    print(f"Scanning for stale snapshots older than {RETENTION_DAYS} days...")

    # Calculate our cutoff timeline threshold (Current time minus 30 days)
    time_limit = datetime.datetime.now(timezone.utc) - datetime.timedelta(
        days=RETENTION_DAYS
    )

    try:
        # Retrieve all snapshots owned by your AWS account that belong to this volume
        snapshots_response = ec2.describe_snapshots(
            OwnerIds=["self"],
            Filters=[{"Name": "volume-id", "Values": [VOLUME_ID]}],
        )

        deleted_count = 0

        for snapshot in snapshots_response["Snapshots"]:
            # Extract creation timestamp and snapshot ID
            creation_time = snapshot["StartTime"]
            snap_id = snapshot["SnapshotId"]

            # Compare snapshot birthday against our 30-day cutoff limit
            if creation_time < time_limit:
                print(
                    f"Found expired snapshot {snap_id} (Created: {creation_time}). Deleting..."
                )
                ec2.delete_snapshot(SnapshotId=snap_id)
                deleted_count += 1
                print(f"SUCCESS: Deleted stale snapshot -> {snap_id}")

        print(
            f"Cleanup cycle complete. Total stale snapshots deleted: {deleted_count}"
        )

    except Exception as e:
        print(f"ERROR: Exception occurred during retention cleanup phase: {e}")
        return {
            "statusCode": 200,
            "body": f"Snapshot {snapshot_id} created, but cleanup phase encountered errors.",
        }

    return {
        "statusCode": 200,
        "body": f"Job completed successfully. Created: {snapshot_id}. Cleaned up: {deleted_count} stale snapshots.",
    }