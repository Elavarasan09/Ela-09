from netmiko import ConnectHandler , redispatch
from datetime import datetime
import time
import re
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

start = time.time()  # Current time
now = datetime.now()  # Current date

router_credentials = [
    {'username': 'admin', 'password': '@dmi^@123'},
    {'username': '013980', 'password': 'Sept+0987654'},
    {'username': '015956', 'password': 'Heshmitha!234'}
]

# Define the terminal server details
terminal_server = {
    'device_type': 'terminal_server',
    'ip': '172.29.1.252',
    'username': 'sifyvpnuser',
    'password': 'securesify',
    'port': 22,
    'secret': 'enable_password'
}

# Define the path to your CSV file containing IPs
csv_file = 'C:/ip_add/ip_add.csv'

# Establish SSH connection to the terminal server
try:
    router = ConnectHandler(**terminal_server)
    print("SIFY VPN SERVER SSH connection established successfully.")
except Exception as e:
    print(f"Failed to connect to SIFY VPN server: {str(e)}")
    exit(1)

# Connect to beaconadmin server from SIFY VPN server
try:
    router.write_channel("ssh beaconadmin@223.31.98.56\n")
    time.sleep(2)
    output = router.read_channel()
    print(output)
    
    if "password" in output or "Password" in output:
        router.write_channel("be@c0n@dm!n\n")
        time.sleep(1)
    
    print(f"BEACON SERVER SSH IS SUCCESSFUL: {router.find_prompt()} \r")
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

# Loop through each device IP and perform operations
for device_ip in ips:
    print(device_ip)

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", device_ip):
        print("Invalid IP address")
        continue

    def ssh_login_to_router(device_ip):
        for creds in router_credentials:
            print(f"Trying to log in to {device_ip} as {creds['username']}")
            try:
                
                router1 = {
                    'device_type' : 'cisco_ios',
                    'host': device_ip,
                    'username': creds['username'],
                    'password': creds['password'],
                    'port': 22,  # Adjust this if SSH runs on a different port
                }
                
                connection = ConnectHandler(**router1)
                print(f"Successfully logged in to {device_ip} as {creds['username']}")
                return connection  # Return the connection object for further use
            except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
                print(f"Login failed: {e}")
                continue  # Try the next set of credentials
        print(f"All login attempts failed for {device_ip}")
        return None

    
    
    router_connection = ssh_login_to_router(device_ip)
    if router_connection:
        # Successfully logged in, you can now send commands
        output = router_connection.send_command('show version')
        print(output)

        # Don't forget to disconnect after your operations
        router_connection.disconnect()
        print("Router connection closed.")


