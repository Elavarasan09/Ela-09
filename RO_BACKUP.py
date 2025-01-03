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
        time.sleep(0.5)

        
        
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
            
        BGP_SUM_LIST = []    
        # Send commands and collect output
        BGP_sum = router.send_command(f" show ip bgp sum")
        print(f"{prompt} show ip bgp sum ")
        print(BGP_sum)
        for line in BGP_sum.splitlines():
            BGP_SUM_LIST.append(line.split()[:3])
        #print(BGP_SUM_LIST)
        
        String = ""
        String1 = ""
        String2 = ""
        String3 = ""
        AS0=""
        AS1=""
        AS2=""
        AS3=""
        
        i = len(BGP_SUM_LIST)
        for a in range(0 , i):
            #print(BGP_SUM_LIST[a])
        
            
            for line in BGP_SUM_LIST[a]:
                AS=""  
                AS = BGP_SUM_LIST[a]
              #AS.append(line.split(","))
                #print(AS)
                
            if '9583' in AS[2] :
                
                String = AS[0] 
                #print(String) 
                AS0= AS[2]               
                continue
                
            elif "4755" in AS[2]:
                
                String1 = AS[0]
                #print(String1)
                AS1= AS[2]
                continue
            
            elif '9829' in AS[2]:
                
                String2 = AS[0]
                #print(String2)
                AS2= AS[2]
                continue
            elif "132215" in AS[2]:
                
                String3 = AS[0]
                #print(String3)
                AS3= AS[2]
                continue
            else:
                pass
            
        LIST1 = (String , String1 , String2, String3)
        LIST2 = (AS0 , AS1, AS2 , AS3)
        
        #New_list=[]
        #print(LIST1) 
        #print(LIST2) 
        New_list = [item.strip() for item in LIST2 if item.strip()]  
        print(New_list)   
        New_list2 = [item.strip() for item in LIST1 if item.strip()]
        print(New_list2) 
        
        
        command = [
                        'terminal length 0',
                        'show running-config',
                        'show ip bgp all summary',
                        'show ip arp',
                        'show ip interface brief',
                        'show interfaces description',
                        'show platform',
                        'show inventory'
        ]
        
        commands2 = [f'show ip bgp neighbors {i} advertised-routes',
                     f'show ip bgp neighbors {i} routes']
                        
        command1 = [    
                        'show process cpu history',
                        'show version',
                        'show ip route',
                        'show logging',
                        'show vrrp brief',
                        'show vrrp all',
                        'show environment',
                        'show clock'
                    ]
                    
                    
        # Save output to a file

        dt = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"C:/Users/017925/OneDrive - Sify Technologies Limited/Desktop/ROUTER_BACKUP _{device_ip}_{dt}.txt" ## file location and name
        with open(filename, 'w') as f:
            
            for commands in command:
                output = router.send_command(commands)
                #f.write(f"{prompt} BACKUP OF THE ROUTER {device_ip} \n")
                f.write(f"{prompt} {commands}\n {output}\n")
                
            for i in New_list2:    
                    e = router.send_command(f'show ip bgp neighbors {i} advertised-routes \n')
                    f.write(f"{prompt} show ip bgp neighbors {i} advertised-routes \n {e}")
                    g = router.send_command(f'show ip bgp neighbors {i} routes \n')
                    f.write(f"{prompt} show ip bgp neighbors {i} routes \n {g}")
                
            for command3 in command1:
                output2 = router.send_command(command3)
                #f.write(f"{prompt} BACKUP OF THE ROUTER {device_ip} \n")
                f.write(f"{prompt} {command3}\n {output2}\n")
                
                    
             #f.write("") 
        print(f"Saved output to {filename}")
        print("-------------------------------------------------------------")
        
        
        
        
        
       
                
           
                
                    
                    
                
           
                
        
            
            
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
