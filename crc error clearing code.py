from netmiko import ConnectHandler, redispatch   
from datetime import datetime  
import time 
import re 

start = time.time() 
now = datetime.now() 

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


try:  
    router = ConnectHandler(**terminal_server)
    print("SIFY VPN SERVER SSH connection established successfully.")
except Exception as e:
    print(f"Failed to connect to SIFY VPN server: {str(e)}")
    exit(1) 
    

try: 
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


print(ips)

error_devices = [] 

show_interface = []
cmd = ['     0 input errors', ' 0 CRC', ' 0 frame', ' 0 overrun', ' 0 ignored']

# Loop through each device IP and perform operations
for device_ip in ips:
    print(device_ip)
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",device_ip): 
        print("Invalid Ip address") 
        continue
        
    
    try:
        # Connect to the particular router device via terminal server
        router.write_channel(f"ssh -l infinetv2sify {device_ip}\n")
        time.sleep(2)
        output = router.read_channel()

        # Check for password prompt and send password if needed
        if "Password" or "password" in output:
            router.write_channel("&!fy_Inf!n3t%@\n")
            time.sleep(1)
        
        # Find the prompt after successfully logging in
        prompt = router.find_prompt()
        time.sleep(1)
        print(f"Connected to {device_ip} with prompt {prompt}")
        print("-------------------------------------------------------------")

        # Redispatch to the correct device type (assuming it's Cisco IOS)
        redispatch(router, device_type='cisco_ios')
        time.sleep(1)
        
        # Send commands and collect output
        version_output = router.send_command("sh ip int brief")
        time.sleep(0.5)
        router_prompt = router.find_prompt() 
        print(f"{router_prompt} sh ip int brief")
        print(version_output)
        INTERFACES = []
        for line in version_output.splitlines():
            INTERFACES.append(line.split()[0]) 
        print(INTERFACES)
        for i in INTERFACES:
                if "FastEthernet0"  in i or "GigabitEthernet8" in i or "GigabitEthernet5" in i or "GigabitEthernet4" in i  :
                    sh_int = router.send_command(F" show interface {i} | i CRC") 
                    print(F"{router_prompt} show interface {i} | i CRC")
                    time.sleep(2)
                    print(sh_int)
                    time.sleep(1)
                    for line in sh_int.splitlines():
                        show_interface = (line.split(",")) 
                    print(show_interface)
                    if cmd != show_interface:
                        time.sleep(0.5)
                        
                        # Save output to a file
                        dt = now.strftime("%Y-%m-%d_%H-%M-%S") 
                        filename = f"C:/Users/017925/OneDrive - Sify Technologies Limited/Desktop/crc_input_errors_{device_ip}_{dt}.txt" ## file location and name
                        with open(filename, 'w') as f: 
                            
                            updated_show_interface = [item.strip() for item in show_interface]
                            print(updated_show_interface)
                            
                            Input_errors  = updated_show_interface[0]
                            Crc_errors = updated_show_interface[1]
                            
                            #print(Input_errors)
                            #print(Crc_errors)
                            f.write(f"ROUTER LOOPBACK = {device_ip}\n ")
                            print()
                            f.write(f"BANK NAME =  {router_prompt}\n")
                            print()
                            f.write(f"INPUT ERRORS =  {Input_errors}\n" ) 
                            print()
                            f.write(f"CRC ERRORS = {Crc_errors}\n")
                            print()
                            f.write("Now it is cleared")
                            
                        print(f"Saved output to {filename}\n ")
                        print("-------------------------------------------------------------")
                        
                        #show_interface_1 = router.send_command(f"sh run int {i}")
                        clear_crc = router.write_channel(f"clear counter {i}")
                        space  = router.write_channel("\n")
                        #clear_crc += router.write_channel("\n")
                        print(f"{router_prompt} clear counter {i}")
                        time.sleep(0.5)
                        print(clear_crc)
                        print("Cleared")
                        
                        
                    
                    else:
                        print()
                        print("It is not having any crc or input errors")
                        print() 
        router.cleanup()
        time.sleep(0.5)              

        # Save output to a file
        #dt = now.strftime("%Y-%m-%d_%H-%M-%S") 
        #filename = f"C:/Users/017925/OneDrive - Sify Technologies Limited/Desktop/show_version_{new_ip}_{dt}.txt" ## file location and name
        #with open(filename, 'w') as f: 
            #f.write(version_output) 
        
        #print(f"Saved output to {filename}")
        #print("-------------------------------------------------------------")
        
    
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
