import boto3

ACCESS_KEY = "replace with access key"
SECRET_KEY = "replace with secret access key"

def get_unused_volumes():
    ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    unused_volumes = []
    for volume in ec2.volumes.all():
        if volume.state == 'available':
            attachments = volume.attachments
            if not attachments:
                # replace any non-breaking space characters with regular spaces in the volume ID
                volume_id = volume.id.replace('\u00A0', ' ')
                unused_volumes.append(volume_id)
    return unused_volumes

def delete_volumes(volumes):
    ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    for volume in volumes:
        print(f"Deleting volume {volume}")
        ec2.Volume(volume).delete()

def main():
    regions = [region['RegionName'] for region in boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY).describe_regions()['Regions']]
    for region in regions:
        print(f"Checking for unused volumes in region {region}")
        boto3.setup_default_session(region_name=region)
        unused_volumes = get_unused_volumes()
        if unused_volumes:
            delete_volumes(unused_volumes)
        else:
            print(f"No unused volumes found in region {region}")

if __name__ == "__main__":
    main()
