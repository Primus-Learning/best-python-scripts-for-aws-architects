import boto3

AWS_ACCESS_KEY_ID = "replace with access key"
AWS_SECRET_ACCESS_KEY = "replace with secret access key"

def cleanup_snapshots():
    ec2 = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    for region in regions:
        print(f"Cleaning up snapshots in {region}")
        ec2 = boto3.client('ec2', region_name=region, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        response = ec2.describe_snapshots(OwnerIds=['self'])
        snapshots = response['Snapshots']
        while snapshots:
            for snapshot in snapshots:
                print(f"Deleting snapshot {snapshot['SnapshotId']}")
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            response = ec2.describe_snapshots(OwnerIds=['self'])
            snapshots = response['Snapshots']
        print(f"Finished cleaning up snapshots in {region}")

if __name__ == '__main__':
    cleanup_snapshots()
