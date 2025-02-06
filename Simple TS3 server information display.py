import socket
import tkinter as tk
from tkinter import messagebox

# Server Info
host = '0.0.0.0' #Server IP
qport = 9987  #Query port
user = 'serveradmin' #ServerAdmin Username
password = 'password' #ServerAdmin Password

def get_client_list():
    try:
        # Get User List
        # ******************
        # Create a tcp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, qport))
        # ******************
        # Receive response from server
        sock.recv(4096).decode('utf-8')
        # ******************
        # Send login command
        login_command = f'login {user} {password}\n'
        sock.send(login_command.encode('utf-8'))
        sock.recv(4096).decode('utf-8')
        # ******************
        # Send command to get user list
        sock.send(b'clientlist\n')
        client_list_response = sock.recv(4096).decode('utf-8')
        # ******************
        # Disconnect
        sock.send(b'quit\n')
        sock.close()
        # ******************
        # Processing user list
        clients = []
        for line in client_list_response.split('|'):
            if 'client_nickname' in line:
                nickname = line.split('client_nickname=')[1].split(' ')[0]
                # Nicknames that have spaces between their words, this space is in the form of \s which needs to be changed, so we use the following command for that.
                nickname = nickname.replace('\s', ' ')
                clients.append(nickname)

        return clients

    except Exception as e:
        messagebox.showerror("Error", f"Cannot Connect to Server! R: {e}")
        return []

def get_server_info():
    try:
        # Get Server Info
        # ******************
        # Create TCP Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, qport))
        # ******************
        # Receive initial response from server
        sock.recv(4096).decode('utf-8')
        # ******************
        # Send login command
        login_command = f'login {user} {password}\n'
        sock.send(login_command.encode('utf-8'))
        sock.recv(4096).decode('utf-8')
        # ******************
        # Send a command to get server information
        sock.send(b'serverinfo\n')
        server_info_response = sock.recv(4096).decode('utf-8')
        # ******************
        # Disconnect
        sock.send(b'quit\n')
        sock.close()
        # ******************
        # Server information processing
        server_info = {}
        for line in server_info_response.split():
            if '=' in line:
                key, value = line.split('=', 1)
                server_info[key] = value

        return server_info

    except Exception as e:
        messagebox.showerror("Error", f"Cannot Connect To Server! R: {e}")
        return None

def update_client_list():
    try:
        # Update User List
        # ******************
        # Get user list
        clients = get_client_list()
        # ******************
        # Clear the previous list of users
        client_listbox.delete(0, tk.END)
        # ******************
        # Add users to the list
        for client in clients:
            client_listbox.insert(tk.END, client)

    except Exception as e:
        messagebox.showerror("Error", f"Cannot Refresh The Page! R: {e}")

def update_server_info():
    try:
        # Update Server Info
        # ******************
        # Get server information
        server_info = get_server_info()

        if server_info:
            # ******************
            # Show server name
            server_name = server_info.get('virtualserver_name', 'N/A')
            server_name_label.config(text=f"Server Name: {server_name}")
            # ******************
            # Show server status (online/offline)
            status = "Online" if server_info else "Offline"
            status_color = "green" if status == "Online" else "red"
            status_label.config(text=f"Status: {status}", fg=status_color)
            # ******************
            # Show Slots
            max_clients = server_info.get('virtualserver_maxclients', 'N/A')
            slot_text = f"Slot: {len(client_listbox.get(0, tk.END))}/{max_clients}"
            slot_label.config(text=slot_text)

    except Exception as e:
        messagebox.showerror("Error", f"Cannot Connect To Server! R: {e}")

def refresh_all():
    # ******************
    # Update user list
    update_client_list()
    # ******************
    # Update server information
    update_server_info()
# ******************
# Create the main window
root = tk.Tk()
root.title("TeamSpeak 3 Server Info")
# ******************
# Create frames for server information
info_frame = tk.Frame(root)
info_frame.pack(padx=10, pady=10)
# ******************
# Show server name
server_name_label = tk.Label(info_frame, text="Server Name: N/A", font=("Arial", 12))
server_name_label.pack(anchor="w")
# ******************
# Show server status
status_label = tk.Label(info_frame, text="Status: N/A", font=("Arial", 12))
status_label.pack(anchor="w")
# ******************
# Show Slots
slot_label = tk.Label(info_frame, text="Slot: N/A", font=("Arial", 12))
slot_label.pack(anchor="w")
# ******************
# Create a list box to display users
client_listbox = tk.Listbox(root, width=50, height=20)
client_listbox.pack(padx=10, pady=10)
# ******************
# Update button
refresh_button = tk.Button(root, text="Refresh", command=refresh_all)
refresh_button.pack(pady=5)
# ******************
# Run window
root.mainloop()
