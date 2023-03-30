import os

config_path = 'C:\\Users\\AL27165\\.aws\\config'

def generate_one(account):
    foundprofile = False
    file_item = open(config_path, "r+")
    
    for line in file_item.readlines():
        if f"[profile {account} ]" in line:
            foundprofile = True
            print('Profile found in AWS_CONFIG file for ', account)

    if foundprofile == False: # not found, we are at the eof
        print("NO Profile found in AWS_CONFIG.  Creating profile  for", account)
        file_item.write("\n[profile "+ account + " ]\noutput = json\nregion = us-east-1\nrole_arn = arn:aws:iam::" 
        + account + ":role/CloudOperationsExecutionRole\nsource_profile = ADFS-Ops-Admin\n\n" )

