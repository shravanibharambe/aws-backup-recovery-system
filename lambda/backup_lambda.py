import os
import boto3
from datetime import datetime, timezone

ec2 = boto3.client('ec2')

VOLUME_ID = os.environ['VOLUME_ID']
RETENTION_LIMIT = 3

def lambda_handler(event, context):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    description = f"BackupProject-Auto-Snapshot-{timestamp}"
    
    # 1. Create the snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=description,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {'Key': 'Project', 'Value': 'BackupProject'},
                    {'Key': 'BackupType', 'Value': 'Automated'},
                    {'Key': 'CreatedAt', 'Value': timestamp}
                ]
            }
        ]
    )

    new_snapshot_id = response['SnapshotId']
    print(f"Created new snapshot: {new_snapshot_id}")
    
    # 2. Query automated snapshots
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {'Name': 'tag:Project', 'Values': ['BackupProject']},
            {'Name': 'tag:BackupType', 'Values': ['Automated']}
        ]
    )['Snapshots']
    
    # 3. Sort snapshots newest first
    sorted_snapshots = sorted(
        snapshots,
        key=lambda s: s['StartTime'],
        reverse=True
    )

    print(f"Total automated snapshots found: {len(sorted_snapshots)}")
    
    # 4. Prune snapshots older than retention limit
    if len(sorted_snapshots) > RETENTION_LIMIT:
        snapshots_to_delete = sorted_snapshots[RETENTION_LIMIT:]

        for snap in snapshots_to_delete:
            snap_id = snap['SnapshotId']
            print(f"Deleting expired snapshot: {snap_id}")
            ec2.delete_snapshot(SnapshotId=snap_id)
    else:
        print(
            f"Snapshot count is within limit "
            f"({RETENTION_LIMIT}). No deletion needed."
        )
        
    return {
        'statusCode': 200,
        'body': (
            f"New snapshot {new_snapshot_id} created. "
            f"Retention evaluated."
        )
    }
