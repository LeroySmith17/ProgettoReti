

import tkinter as tk
from tkinter import messagebox
import socket
from time import sleep
import threading
import random



# campi
window_main = tk.Tk()
window_main.title("Game Client")
tuo_nome = ""
role = ""
tua_scelta = ""
scelta_avversario= ""
closing = "closing"
game_timer =60
game_closing_timer= 10
tuo_punteggio = 0
punteggio_avversario = 0
cont_domande = 1
cont_risposte = 1
stop_countdown = False
# dizionari con domande e rispote
d_domande = {
    1 : "Chi ha scoperto l'America?", 
    2 : "Chi era Napoleone Bonaparte?", 
    3 : "Quando è avvenuto il cosidetto D-Day?", 
    4 : "In che continente è avvenuta la guerra di Ace Combat 04?",
    5 : "Come si chiama l'ultimo capitolo della serie Metro?",
    6 : "Quale dei seguenti videogiochi NON è della Paradox?",
    7 : "Come si chiama il protagonista di Red Dead Redemption?",
    8 : "Quando è stato rilasciato per la prima volta Warframe?",
    9 : "Qual è il gioco dell'anno del 2018?",
    10 : "Come si chiama il remake di Nier: Gestalt?",
    11: "Che arma usa Sinon di GGO?",
    12: "Come si chiama la VTuber drago di Hololive?",
    13: "Chi è la protagonista femminile di Steins;Gate?",
    14: "Quanti anni ha Uzaki-chan all'inizio della serie?",
    15: "Qual è il miglior anime 2019?"
}

d_quesiti = {
    1 : "Cristoforo Colombo",
    2 : "Amerigo Vespucci", 
    3 : "Marco Polo",
    4 : "Imperatore Romano", 
    5 : "Generale Tedesco", 
    6 : "Imperatore Francese", 
    7 : "6 giugno 1944", 
    8 : "25 aprile 1945", 
    9 : "22 giugno 1941", 
    10: "Michelangelo", 
    11 : "Da vinci", 
    12 : "Giotto",
    13 : "Metro 2034",
    14 : "Metro Exodus",
    15 : "Metro 2033",
    16 : "Europa Universalis IV",
    17 : "Total War: Empire",
    18 : "Stellaris",
    19 : "Arthur Morgan",
    20 : "Django Freeman",
    21 : "John Marston",
    22 : "2013",
    23 : "2016",
    24 : "2009",
    25 : "Red Dead Redemption 2",
    26 : "The Last of us 2",
    27 : "Fortnite",
    28 : "Nier Automata",
    29 : "Nier Replicant",
    30 : "Drakengard",
    31 : "Spada",
    32 : "fucile di Precisione",
    33 : "Fucile d'assalto",
    34 : "Houshou Marine",
    35 : "Usada Pekora",
    36 : "Kiryu Coco",
    37 : "Alisa Amelia",
    38 : "Nagatoro",
    39 : "Kurisu Makise",
    40 : "19",
    41 : "20",
    42 : "16",
    43 : "My Hero Academia",
    44 : "Attack on Titan S4",
    45 : "DragonBall Super"
    }
# set di rispote correte
ris_esatte = {"Cristoforo Colombo",  "Imperatore Francese", "6 giugno 1944", "Da vinci", "Metro Exodus", "Total War: Empire","John Marston", 
              "2013", "Fortnite", "Nier Replicant", "fucile di Precisione","Kiryu Coco","Kurisu Makise","19","Attack on Titan S4",}


# client di rete
client = None
HOST_ADDR = '127.0.0.1'
HOST_PORT = 8080

# GUI del programma
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Nome:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connettiti", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)
top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)
top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_tuo_nome = tk.Label(top_left_frame, text="Nome: " + tuo_nome, font = "Helvetica 13 bold")
lbl_opponent_name = tk.Label(top_left_frame, text="Ruolo: " + role)
lbl_tuo_nome.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))
top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_game_timer = tk.Label(top_right_frame, text="Tempo:", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue")
lbl_game_timer.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))
top_frame.pack_forget()
middle_frame = tk.Frame(window_main)
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** SELEZIONA LA DOMANDA ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
button_frame = tk.Frame(middle_frame)
btn_questionA = tk.Button(button_frame, text="A", command=lambda : choice_question(1), height = 2, width = 5)
btn_questionB= tk.Button(button_frame, text="B",  command=lambda : choice_question(2), height = 2, width = 5)
btn_questionC = tk.Button(button_frame, text="C", command=lambda : choice_question(3), height = 2, width = 5)
btn_questionA.grid(row=0, column=0)
btn_questionB.grid(row=0, column=1)
btn_questionC.grid(row=0, column=2)
button_frame.pack(side=tk.TOP)
final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
final_frame.pack(side=tk.TOP)
middle_frame.pack_forget()
button_frame = tk.Frame(window_main)
btn_answerA = tk.Button(button_frame, text="", command=lambda : choice(btn_answerA),  state=tk.DISABLED, height = 2, width = 20)
btn_answerB = tk.Button(button_frame, text="", command=lambda : choice(btn_answerB),  state=tk.DISABLED, height = 2, width = 20)
btn_answerC = tk.Button(button_frame, text="", command=lambda : choice(btn_answerC),  state=tk.DISABLED, height = 2, width = 20)
btn_answerA.grid(row=0, column=0, pady=10)
btn_answerB.grid(row=0, column=1, pady=10)
btn_answerC.grid(row=0, column=2, pady=10)
button_frame.pack(side=tk.BOTTOM)

#funzione che prende in ingresso il numero del pulsante premuto e controlla se
#è un pulsante trappola o una domanda
def choice_question(arg):
   global check
   global cont_domande, cont_risposte
   global d_domande, d_quesiti
   global client
   global closing
   global tua_scelta
   
   check= arg 
   # sceglie a random un pulsante trappola 
   #e comunica al server che l'utente l'ha premuto
   x = random.randint(1, 3)
   if check == x:
       lbl_final_result["text"] = "In attesa dell'avversario, puoi sperare in un pareggio..."
       enable_disable_buttons_up("disable")
       enable_disable_buttons_bottom("disable")
       tua_scelta = closing    
       if client:
           client.send(tua_scelta.encode())


  # se il pulsante non è trappola fa comparire la domanda con le 3 possibili risposte      
   else:
       x = random.randint(1, 15)
       lbl_final_result["text"] = "" + d_domande.get(x)     
       btn_answerA["text"] = ""+ d_quesiti.get(x*3)
       btn_answerB["text"] = ""+ d_quesiti.get((x*3)-1)
       btn_answerC["text"] = ""+ d_quesiti.get((x*3)-2)
       enable_disable_buttons_up("disable")
       enable_disable_buttons_bottom("enable")
       
    
# comunica al server la risposta data dall'utente e disabilita i pulsanti
#rimando in attessa della riposta del server
def choice(args):
    global tuo_punteggio, punteggio_avversario
    global ris_esatte
    global tua_scelta
    btn_temp = args
    tua_scelta = btn_temp["text"]
    print(tua_scelta)
    btn_answerA["text"]= ""
    btn_answerB["text"]= "" 
    btn_answerC["text"]= "" 
    lbl_final_result["text"]=""
    lbl_final_result["text"] = "In attesa dell'avversario..."
    if client:
        client.send(tua_scelta.encode())
        enable_disable_buttons_bottom("disable")
        
        
        
#logica principale del programma che controlla se il client 1 e il client 2 hanno risposto correttamente
# o se il client 1 e i client 2 hanno premuto un pulsante trappola
def logic(you, opponent):
    global tuo_punteggio, punteggio_avversario,  game_timer
    global ris_esatte
    global closing
    global stop_countdown
    
    #assegnamento di un punto in caso di risposta corretta al client1
    #o rimozione di un punto in caso negativo
    if you in ris_esatte:
       tuo_punteggio = tuo_punteggio + 1
       lbl_final_result["text"] = ""
       enable_disable_buttons_up("enable")
    else:
        tuo_punteggio = tuo_punteggio - 1
        lbl_final_result["text"] = ""
        enable_disable_buttons_up("enable")
    #stesso procedimento per l'avversario
    if opponent in ris_esatte:
       punteggio_avversario = punteggio_avversario + 1
       
    else:
        punteggio_avversario = punteggio_avversario - 1 
    
    #controllo se l'avversario ha preso una trappola e l'utente no, in caso positivo assegnazione della vittoria e chiusura programma
    if opponent == closing and you != closing:
       game_timer=game_timer + 20
       lbl_final_result["text"] = "Avversario intrappolato, hai vinto!"
       lbl_final_result.config(foreground="green")
       enable_disable_buttons_up("disable")
       enable_disable_buttons_bottom("disable") 
       stop_countdown = True
       threading._start_new_thread(count_down_closing, ("", ""))
    
    #controllo se l'avversario e l'utente1 hanno preso una trappola, in caso positivo assegnazione del pareggio e chiusura programma
    if opponent == closing and you == closing:
       game_timer=game_timer + 20
       lbl_final_result["text"] = "Tu e il tuo avversario siete intrappolati, PAREGGIO!"
       lbl_final_result.config(foreground="black")
       enable_disable_buttons_up("disable")
       enable_disable_buttons_bottom("disable") 
       stop_countdown = True
       threading._start_new_thread(count_down_closing, ("", ""))
    #controllo se utente1 ha preso una trappola, in caso positivo assegnazione della sconfitta e chiusura programma
    if opponent != closing and you == closing:
       game_timer=game_timer + 20
       lbl_final_result["text"] = "Sei intrappolato, hai perso!"
       lbl_final_result.config(foreground="red")
       enable_disable_buttons_up("disable")
       enable_disable_buttons_bottom("disable") 
       stop_countdown = True
       threading._start_new_thread(count_down_closing, ("", ""))
    
    print(tuo_punteggio)
    print(punteggio_avversario)    
    
    
#timer principale di durata di gioco, al termine del timer si controlla chi ha piu punti
# e si asseggna la vittoria a uno dei due giocatori, viene comunicato in una label  
def count_down(nothing1, nothing2):
    global game_timer
    global tuo_punteggio, punteggio_avversario
    global stop_countdown
    
    while game_timer > 0:
        if stop_countdown:
            break
        else:    
            game_timer = game_timer - 1
            lbl_timer["text"] = game_timer
            sleep(1)
    
    if game_timer == 0:
        # calcola il risultato finale
         final_result = ""
         color = ""

         if tuo_punteggio > punteggio_avversario:
            final_result = "(Hai vinto!!!)"
            color = "green"
         elif tuo_punteggio < punteggio_avversario:
             final_result = "(Hai perso!!!)"
             color = "red"
         else:
             final_result = "(Pareggio!!!)"
             color = "black"

         lbl_final_result["text"] = "RISULTATO FINALE: " + str(tuo_punteggio) + " - " + str(punteggio_avversario) + " " + final_result
         lbl_final_result.config(foreground=color)
         enable_disable_buttons_up("disable")
         enable_disable_buttons_bottom("disable")
         count_down_closing("","")
         
         
         
    
#timer chiusura del programma, al raggingimento dello 0 si termina la connessione col server e si chiudono
# le schermate di entrambi i giocatori    
def count_down_closing(nothing1, nothing2):
    global game_closing_timer
    global window_main
    global client
    
    lbl_game_timer["text"]= "Il gioco si chiude in:"
    while game_closing_timer > 0:
        game_closing_timer = game_closing_timer - 1
        lbl_timer["text"] = game_closing_timer
        sleep(1)
    if game_closing_timer == 0:
        # chiusura connessione se si si raggiunge lo 0 e quindi il programma si deve chiudere
        client.close()
        window_main.destroy()
    
  
    
#controllo che il nome inserito non sia vuoto
def connect():
    global tuo_nome
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        tuo_nome = ent_name.get()
        lbl_tuo_nome["text"] = "Il tuo nome: " + tuo_nome
        connect_to_server(tuo_nome)




def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, tuo_nome
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
         # Invia il nome al server dopo la connessione
        client.send(name.encode())

        #disabilita i widget non piu necessari
        btn_connect.config(state=tk.DISABLED)
        ent_name.config(state=tk.DISABLED)
        lbl_name.config(state=tk.DISABLED)
        enable_disable_buttons_bottom("disable")

        # avvia un thread principale per la comunicazione server-client
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

#funzione che serve al client per ricevere i dati che invia il server del client2
def receive_message_from_server(sck, m):
    global tuo_nome, role
    global tua_scelta, scelta_avversario


    while True:
        from_server = sck.recv(4096)
       
        if not from_server: break
        #ricezione del ruolo assegnato dal server
        if from_server.startswith("role$".encode()):
            role = from_server.replace("role$".encode(), "".encode())
            lbl_opponent_name["text"] = "Ruolo: " + role.decode()
            top_frame.pack()
            middle_frame.pack()

            # sappiamo che due utenti sono connessi, il gioco puo iniziare
            threading._start_new_thread(count_down, ("", ""))
            lbl_welcome.config(state=tk.DISABLED)
            lbl_line_server.config(state=tk.DISABLED)

        elif from_server.startswith("$opponent_choice".encode()):
            # ottieni la risposta dell'avversario dal server
            scelta_avversario = from_server.replace("$opponent_choice".encode(), "".encode())
            # parte la logica per l'assegnamento dei punti e in nel caso la vittoria/sconfitta/pareggio
            # se uno dei due utenti (o entrambi) hanno premuto una trappola
            logic(tua_scelta, scelta_avversario.decode())
    # chiusura connessione se si preme sulla X per uscire dal programma
    sck.close()

#semplice funzione per diasbilitare i bottoni della scelta della risposta
def enable_disable_buttons_bottom(check):
    if check == "disable":
        btn_answerA.config(state=tk.DISABLED)
        btn_answerB.config(state=tk.DISABLED)
        btn_answerC.config(state=tk.DISABLED)
    else:
        btn_answerA.config(state=tk.NORMAL)
        btn_answerB.config(state=tk.NORMAL)
        btn_answerC.config(state=tk.NORMAL)

#semplice funzione per diasbilitare i bottoni della scelta della domanda
def enable_disable_buttons_up(check):
    if check == "disable":
        btn_questionA.config(state=tk.DISABLED)
        btn_questionB.config(state=tk.DISABLED)
        btn_questionC.config(state=tk.DISABLED)
    else:
        btn_questionA.config(state=tk.NORMAL)
        btn_questionB.config(state=tk.NORMAL)
        btn_questionC.config(state=tk.NORMAL)

window_main.mainloop()