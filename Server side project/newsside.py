import socket; import threading;import platform;
################################################
PORT=5090
format="utf-8"
SERVER=socket.gethostbyname(socket.gethostname()) #server= "ip adrr"
print(SERVER)
print(socket.gethostname())
ADDR=(SERVER,PORT)
DISCONNECT_MESSAGE= "!DISCONNECT"
#######################################################
Clients=[], Addresses=[], update_status={}, TARGET_MACHINES=[]
uname= None
#######################################################
SERVER=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
#def close(): (just trying out new stuff)
 #   print(f"[UPDATE] {threading.active_count()}")
def handle_client(conn, addr):
    print(f"[NEW CONNECTION]{addr} connected.")

    connected=True
    while connected:#hence the threading
        msg_length = conn.recv(64).decode(format)
        ################################################
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(format)
            get_os_version()
            run_update()
            if msg== DISCONNECT_MESSAGE:
                   connected=False


            print(f"[{addr}]{msg}")
            conn.send("msg received".encode(format))

    #start of serverside commands
    ######################################################
    def get_os_version():
        return platform.uname()
    
    def run_update():
        for machine in TARGET_MACHINES:
            target_name = machine['name']
            current_version = get_os_version()
        
        if current_version != latest_version:
            success = update_os(machine)
            update_status[target_name] = success
        else:
            update_status[target_name] = True
    
        return (update_status)
    #def update_os(machine):
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(machine['ip'], username=machine['user'], password=machine['password'])
    
    #if platform.system() == 'Windows':
        # Assuming the ISO is mounted and the update command is available
        #stdin, stdout, stderr = ssh.exec_command('setup.exe /auto upgrade /quiet /noreboot')
    #elif platform.system() == 'Linux':
        #stdin, stdout, stderr = ssh.exec_command('sudo apt-get update && sudo apt-get upgrade -y')
    #elif platform.system() == 'Darwin':
        #stdin, stdout, stderr = ssh.exec_command('softwareupdate --all --install --force')
    #else:
        #print(f"Unsupported OS type: {platform.system()}")
        #return False
    
    #stdout.channel.recv_exit_status()
    #ssh.close()
    #return True

    #end of serverside commands
    ########################################################
    conn.close()
def start():
    SERVER.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn, addr= SERVER.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
print("[STARTING] server is starting...")
start()
