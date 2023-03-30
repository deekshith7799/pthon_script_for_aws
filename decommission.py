from botocore.exceptions import ClientError
import boto3
import time
import config_generator

#Change the account_num below

account_num='029916517481'
config_generator.generate_one(account_num)
session=boto3.Session(profile_name=account_num)
client=session.client(service_name='ec2')
print(r"Decomissioning the account:  ",account_num)
list_of_regions=['us-east-1', 'us-east-2']

#checks instances in both regions and will stop those instances.
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name='ec2')
        print("EC2 instance list from each region: ", each_region)
        try:
            i = 0
            for inst in ec2.instances.all():
                i += 1
                if inst != '':
                   print(inst.id, inst.state["Name"])
                if inst.state["Name"] == "running":
                        inst.stop()
            print("Instances stopped")
            if i == 0:
                print("No Instances Found")
        except ClientError as e:
            print(e)
        time.sleep(15)

#checks volumes in both regions and will detach and delete those volumes
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name="ec2")
        print("Volume list from each region: ", each_region)
        try:
            for vol in ec2.volumes.all():
                if vol != '':
                   print(vol.id, vol.state)
                else:
                    print('No Volumes found')
                print('Detaching and Deleting volumes')
                if vol.state == "in-use":
                        vol.detach_from_instance()
                time.sleep(5)
                if vol.state == "available":
                        vol.delete()
        except ClientError as e:
            print(e)

#checks AMIs in both regions and will deregister those AMIs
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name="ec2")
        print("AMI list from each region: ", each_region)
        try:
            i = 0
            for ami in ec2.images.filter(Owners=["self"]):
                i += 1
                if ami != '':
                   print(ami.id, ami.state)
                if ami.state == "available":
                       ami.deregister()
            print("AMI's Deregistered")
            if i == 0:
                print("No AMI's Found")
        except ClientError as e:
            print(e)

#checks snapshots in both regions and will delete those snapshots
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name="ec2")
        print("Snapshot list from each region: ", each_region)
        try:
            i = 0
            for snap in ec2.snapshots.filter(OwnerIds=["self"]):
                i += 1
                if snap != '':
                    print(snap.id, snap.state)
                if snap.state == "completed" or "error":
                        snap.delete()
            print("Snapshots Deleted")
            if i == 0:
                print("No Snapshots found")
        except ClientError as e:
            print(e)

#checks key-pairs in both regions and will delete those key-pairs.
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name="ec2")
        print("Key-pairs from each region: ", each_region)
        try:
            i = 0
            for key_pair in ec2.key_pairs.all():
                i += 1
                if key_pair != '':
                    print(key_pair.key_pair_id, key_pair.key_fingerprint)
                if key_pair.key_fingerprint!='':
                            key_pair.delete()
            print("Key pairs deleted")
            if i == 0:
                print("No key pairs found")
        except ClientError as e:
            print(e)

#checks Elastic IPs in both regions and will release those EIPs
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name="ec2")
        print("Elastic-Ips from each region: ", each_region)
        try:
            i = 0
            for eip in ec2.vpc_addresses.all():
                i += 1
                if eip != '':
                    print(eip.allocation_id)
                if eip.network_interface_owner_id == account_num:
                       eip.release()
            print("Elastic Ip's Released")
            if i == 0:
                print("No elastic Ip's found")
        except ClientError as e:
            print(e)

#checks instance state in both regions and will terminate those instances.
for each_region in list_of_regions:
        session=boto3.Session(profile_name=account_num, region_name=each_region)
        ec2=session.resource(service_name='ec2')
        print("EC2 instance list from each region: ", each_region)
        try:
            i = 0
            for inst in ec2.instances.all():
                i += 1
                if inst != '':
                   print(inst.id, inst.state["Name"])
                ec2.Instance(inst.id).modify_attribute(DisableApiTermination={ 'Value': False })
                if inst.state["Name"] == "stopped":
                        inst.terminate()
            print("Instances Terminated")
            if i == 0:
                print("No instances Found")
        except ClientError as e:
            print(e)
