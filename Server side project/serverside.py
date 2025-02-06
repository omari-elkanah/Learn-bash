#cmd
from flask import Flask, request, jsonify; import platform; import paramiko; import uuid

app = Flask(__name__)

latest_version = "Windows 11 Pro"
update_status = {}
TARGET_MACHINES = [
    {"name": "machine1", "ip": "192.168.1.2", "user": "username", "password": "password"},
    # Add more target machines as needed
]

WINDOWS_11_ISO_PATH = "/path/to/windows11.iso"
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
    return jsonify(update_status)

@app.route('/run_update', methods=['POST'])
def run_update():
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
    app.run(host='0.0.0.0', port=5000)