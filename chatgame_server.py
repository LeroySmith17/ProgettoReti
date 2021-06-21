#importiamo i moduli necessari
import tkinter as tk
import socket
import threading
from time import sleep
import random


window = tk.Tk()
window.title("Server")

# parte superiore della GUI con i 2 pulsanti
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# parte centrale della GUI con le informazioni del server
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# parte inferiore della GUI con la lista dei client connessi
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

# campi che utilizzeremo
server = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
player_data = []
# ruoli che il server deve assegnare ai client
roles = {1 : "Zio Peppe", 2 : "Pietro Smusi", 3 : "Orazio Grinzosi", 4 : "Piermenti Sfracellozzi", 5 : "L'uomo Ago"}


# Avvia server
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # il server rimane in ascolto in attesa dei client

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Arresta server
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)

# accetta i clients
def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # avvio thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

# riceve ed invia messaggi ai client, serve principalmente per assegnare i ruoli
# e per estrarre la risposta alla domanda del client e passarlo all'altro client
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1
    global roles

    x = random.randint(1, 4)
    y = random.randint(1, 4)
    role1 = roles.get(x)
    role2 = roles.get(y)
 
    client_name = client_connection.recv(4096)
    #estrae nome del client
    clients_names.append(client_name)
    #update della lista dei client connessi col nome inserito dall'utente
    update_client_names_display(clients_names)  

    if len(clients) > 1:
        sleep(1)

        # assegna il ruolo ai due client
        clients[0].send(("role$" + role1).encode())
        clients[1].send(("role$" + role2).encode())
        # rimane in attesa

    while True:
        data = client_connection.recv(4096)
        if not data: break

        # estrae la risposta del giocatore
        player_choice = data

        msg = {
            "choice": player_choice,
            "socket": client_connection
        }

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            # invia la risposta del giocatore 1 al giocatore 2 e viceversa per poi fare il controllo e l'assegnamento dei punti
            player_data[0].get("socket").send(("$opponent_choice" + player_data[1].get("choice").decode()).encode())
            player_data[1].get("socket").send(("$opponent_choice" + player_data[0].get("choice").decode()).encode())

            player_data = []

    # trova l'indice del client, quindi lo rimuove da entrambi gli elenchi (elenco dei nomi dei client e elenco delle connessioni)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)


# Restituisce l'indice del client corrente nell'elenco dei client
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Aggiorna la visualizzazione del nome del client quando un nuovo client si connette
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c.decode()+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()