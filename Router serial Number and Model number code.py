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
        router.write_channel(f"ssh -l 013980 {device_ip}\n")
        time.sleep(2)
        output = router.read_channel()
        time.sleep(1)

        
        
        # Check for password prompt and send password if needed
        if "Password" or "password" in output:
        
                router.write_channel("Sept+0987654\n")
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
        
        commands = router.send_command_timing("config terminal")
        prompt1= router.find_prompt()
        print(f"{prompt1} config terminal")
        print(commands)
        time.sleep(2)
        
        commands1= router.send_command(f"ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512")
        print(f"{prompt1} ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512")
        print(commands1)
        
        commands2= router.send_command(f"ip ssh client algorithm mac hmac-sha2-256 hmac-sha2-512")
        print(f"{prompt1}ip ssh client algorithm mac hmac-sha2-256 hmac-sha2-512 ") 
        print(commands2)
        
        exit = router.send_command_timing(f"exit")
        print(f"{prompt1} exit")
        print(exit)
        
        save = router.send_command_timing(f" wr")
        print("\n")
        print(f"{prompt} wr")
        print(save)
        time.sleep(3)
        
        show_commands= router.send_command(f"sh run | i ip ssh")
        print(f"{prompt1} show run | i ip ssh")
        print(show_commands)
            
        sh_ver_LIST = []   
        # Send commands and collect output
        sh_ver_model = router.send_command(f" sh version | i bytes of memory.")
        print(f"{prompt} sh version | i (revision) ")
        print(sh_ver_model)
        for line in sh_ver_model.splitlines():
            sh_ver_LIST.append(line.split()[1:2])
        print(sh_ver_LIST)
        
        sh_ver_list=[]
        sh_ver_serial = router.send_command(f"  sh version | i Processor board")
        print(f"{prompt} sh version | i Processor board")
        print(sh_ver_serial)
        
        sh_ver= router.send_command(f" sh version | i image")
        print(f"{prompt} sh version | i image")
        print(sh_ver)
        
        
        
        
        for line in sh_ver_serial.splitlines():
            sh_ver_list.append(line.split()[3:4])
        print(sh_ver_list)
        
        dt = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"C:/Users/017925/OneDrive - Sify Technologies Limited/Desktop/sh_ver_mode_serial_number _{device_ip}_{dt}.txt" ## file location and name
        with open(filename, 'w') as f:
            f.write(f"{show_commands}\n")
            f.write(f"{sh_ver_LIST}\n")
            f.write(f"{sh_ver_list}\n")
            f.write(f"{sh_ver}\n ")
            
        router.cleanup()
        time.sleep(2)    
        
    except Exception as e:
        print(f"Error connecting to {device_ip}: {str(e)}")
        error_devices.append(device_ip)
        
router.disconnect()