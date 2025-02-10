#to run on cmd
from flask import Flask, request, jsonify, render_template; import platform; import paramiko; import uuid; import nmap

app = Flask(__name__)

latest_version = "Windows 11 Pro"
update_status = {}
TARGET_MACHINES = [
    {"name": "Windows10Machine", "ip": "192.168.137.20", "user": "your_username", "password": "your_password"}
]

WINDOWS_11_ISO_PATH = "Downloads\Windows-11-23H2.iso"
def get_mac_address():
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return mac

def get_os_version():
    return platform.uname()

def update_os(machine):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(machine['ip'], username=machine['user'], password=machine['password'])
    
    if platform.system() == 'Windows':
        # Assuming the ISO is mounted and the update command is available
        stdin, stdout, stderr = ssh.exec_command('setup.exe /auto upgrade /quiet /noreboot')
    #elif platform.system() == 'Linux':
        #stdin, stdout, stderr = ssh.exec_command('sudo apt-get update && sudo apt-get upgrade -y')
    elif platform.system() == 'Darwin':
        stdin, stdout, stderr = ssh.exec_command('softwareupdate --all --install --force')
    else:
        print(f"Unsupported OS type: {platform.system()}")
        return False
    
    stdout.channel.recv_exit_status()
    ssh.close()
    return True
def discover_machines():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.137.0/24', arguments='-sn') #to be configured
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            TARGET_MACHINES.append({
                "name": host,
                "ip": nm[host]['addresses']['ipv4'],
                "user": "default_user",  # Replace with actual user
                "password": "default_password"  # Replace with actual password
            })


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return jsonify({'latest_version': latest_version})
    elif request.method == 'POST':
        data = request.json
        target_name = data.get('target_name')
        status = data.get('status')
        update_status[target_name] = status
        return jsonify({'message': 'Status updated successfully'}), 200

@app.route('/status', methods=['GET'])
def status():
    return render_template('status.html',update_status=update_status)

@app.route('/run_update', methods=['POST'])
def run_update():
    discover_machines()
    for machine in TARGET_MACHINES:
        target_name = machine['name']
        current_version = get_os_version()
        
        if current_version != latest_version:
            success = update_os(machine)
            update_status[target_name] = success
        else:
            update_status[target_name] = True
    
    return jsonify(update_status)

if __name__ == '__main__':
    app.run(host='127.0.1.1', port=5000)