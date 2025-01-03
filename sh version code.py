from netmiko import ConnectHandler, redispatch  
from datetime import datetime  
import time 
import re 

start = time.time() ## Current time 
now = datetime.now() ## Current date

# Define the terminal server details
terminal_server = {
    'device_type': 'terminal_server',
    'ip': '172.29.1.252',
    'username': 'sifyvpnuser',
    'password': 'securesify',
    'port': 22,
    'secret': 'enable_password'
}

# Define the path to your CSV file containing IPs in our laptop (location of the file)
csv_file = 'C:/ip_add/ip_add.csv'


try:  ## perform some action to connect SSH connection 
    router = ConnectHandler(**terminal_server)
    print("SIFY VPN SERVER SSH connection established successfully.")
except Exception as e: 
    print(f"Failed to connect to SIFY VPN server: {str(e)}")
    exit(1)
    

try: ## perform some action to connect beamonadmin server from sify vpn server
    router .write_channel("ssh beaconadmin@223.31.98.56\n")
    time.sleep(2) 
    output=router.read_channel() 
    print(output)  
    if "password" in output: 
     router.write_channel("be@c0n@dm!n\n")
    time.sleep(1) 
    print(f"BEACON SERVER SSH IS SUCCESSFULL {router.find_prompt()} \r") 
    print("\n") 
except Exception as e: 
    print(f"Failed to connect to beacon VPN server: {str(e)}")
    exit() 
    
# Read IPs from the CSV file
with open(csv_file, 'r') as fp: 
    ips = fp.readlines() 

# Strip whitespace characters like `\n` at the end of each line
ips = [ip.strip() for ip in ips]

# Establish SSH connection to terminal server
print(ips)

error_devices = [] 

# Loop through each device IP and perform operations
for device_ip in ips:
    print(device_ip)
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",device_ip): 
        
        print("Invalid Ip address") 
        continue
    try:
        # Connect to the particular router device via terminal server
        router.write_channel(f"ssh -l sifymon {device_ip}\n")
        time.sleep(2)
        output = router.read_channel()

        # Check for password prompt and send password if needed
        if "Password" or "password" in output:
        
                router.write_channel("smon@123\n")
                time.sleep(4)
                router.write_channel("Nocop$@1234\n")
                time.sleep(2)
        
        # Find the prompt after successfully logging in
        prompt = router.find_prompt()
        print(f"Connected to {device_ip} with prompt {prompt}")
        print("-------------------------------------------------------------")

        # Redispatch to the correct device type (assuming it's Cisco IOS)
        redispatch(router, device_type='cisco_ios')
        time.sleep(2)

        # Send commands and collect output
        version_output = router.send_command("show hosts")
        time.sleep(2)
        print(version_output)
        router.cleanup()
        time.sleep(2)
        
        

        # Save output to a file
        dt = now.strftime("%Y-%m-%d_%H-%M-%S") 
        filename = f"C:/Users/017925/OneDrive - Sify Technologies Limited/Desktop/show_version_{device_ip}_{dt}.txt" ## file location and name
        with open(filename, 'w') as f: 
            f.write(version_output) 
        
        print(f"Saved output to {filename}")
        print("-------------------------------------------------------------")
        
    ## if any error occurs this will print the exact ip address which is causing error
    except Exception as e:
        print(f"Error connecting to {device_ip}: {str(e)}")
        error_devices.append(device_ip)

# Disconnect from terminal server
router.disconnect()


# Print devices with errors
if error_devices:
    print("Devices with errors:", error_devices)
else:
    print("All devices processed successfully.")
