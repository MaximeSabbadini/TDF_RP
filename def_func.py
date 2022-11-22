# Import des bibliothèques ###

from tkinter import *
import pygame
import sqlite3
import tkinter.messagebox
from PIL import Image, ImageTk
from pathlib import Path
import matplotlib.pyplot as plt
from ctypes import *
from tkinter import ttk


# Définition du chemin principal ###

# main_path = Path("/Users/maximesabbadini/Desktop/Cours/Aéro2/Grand_projet_programmation/GP21/")

main_path = Path(__file__).parent.absolute()
# Définition des fonctions principales ###

# Accueil


def main_menu():
    def quitter():
        tkinter.messagebox.showinfo('Au Revoir', 'A bientôt sur Race Predictor !')
        accueil.destroy()
    accueil = Tk()
    accueil.title('Tour de France Race Predictor 2020')
    L_x = accueil.winfo_screenwidth()
    L_y = accueil.winfo_screenheight()
    x_coin_sup_gauche = 0
    y_coin_sup_gauche = 0
    accueil.geometry('%dx%d+%d+%d' % (L_x, L_y, x_coin_sup_gauche, y_coin_sup_gauche))

    # klaxon()

    padx = 40
    pady = 10

    # load1 = Image.open("/Users/maximesabbadini/Desktop/Cours/Aéro2/Grand_projet_programmation/GP21/Pictures/fond3.png")
    load1 = Image.open(main_path / "Pictures/fond5.png")
    render = ImageTk.PhotoImage(load1)
    img = Label(image=render)
    img.image = render
    img.place(x=0, y=0)

    b1 = Button(accueil, text='Classement 2019', command=classement)
    b1.place(relx=0.35, rely=0.6, height=50, width=160)
    b2 = Button(accueil, text='Prédiction de la Course', command=connect)
    b2.place(relx=0.55, rely=0.6, height=50, width=160)
    b3 = Button(accueil, text='Statistiques 2019', command=stats)
    b3.place(relx=0.45, rely=0.7, height=50, width=160)
    b4 = Button(accueil, text='Quitter', command=quitter)# , background='red')
    b4.place(relx=0.9, rely=0.9, height=50, width=120)

    accueil.mainloop()


def classement():
    # tkinter.messagebox.showinfo("Attention", "Vous êtes sur le point de consulter le classement de 2019")
    def retour():
        classement_menu.destroy()

    classement_menu = Tk()
    classement_menu.title('Choix du Classement')
    classement_menu.geometry('400x100')
    l1 = Label(classement_menu, text='Choisissez un classement')
    l1.place(relx=0.3, rely=0)
    b_overall = Button(classement_menu, text='Général', command=overall)
    b_overall.place(relx=0, rely=0.3, height=40, width=90)
    b_sprint = Button(classement_menu, text='Sprint', command=sprint)
    b_sprint.place(relx=0.4, rely=0.3, height=40, width=90)
    b_kom = Button(classement_menu, text='KOM', command=kom)
    b_kom.place(relx=0.78, rely=0.3, height=40, width=90)
    b1 = Button(classement_menu, text='Retour', command = retour)
    b1.place(relx=0, rely=0.8)
    classement_menu.mainloop()


def klaxon():
    pygame.init()
    music = pygame.mixer.Sound("1807.wav")
    music.play()

# Classement 2019


def overall():
    def mouse_scroll(e):
        if e.delta < 0:
            c1.yview_scroll(1, 'units')
        elif e.delta > 0:
            c1.yview_scroll(-1, 'units')

    def retour():
        overall_rank.destroy()

    connexion = sqlite3.connect("classement_2019.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM Rankings WHERE Rank <= 154 ")
    result = curseur.fetchall()
    chaine = " "

    for r in result:
        # print(r)
        r = list(r)
        del r[3]
        del r[4]
        chaine = chaine + str(r) + "\n" + "\n"
        chaine = chaine.replace(',', '\t')
        chaine = chaine.replace("'", " ")
        chaine = chaine.replace("[", " ")
        chaine = chaine.replace("]", " ")

    connexion.close()

    overall_rank = Tk()
    overall_rank.title("Classement général")
    c1 = Canvas(overall_rank)
    c1.create_text(0, 0, anchor=NW, text=chaine)
    c1.grid(row=1, column=0)

    lo = Label(overall_rank, text="Le classement général 2019")
    lo.grid(row=0, column=0)

    bo = Button(overall_rank, text="Retour", command=retour)
    bo.grid(row=6, column=1)
    l1 = Label(overall_rank, text='Place')
    l1.place(x=0, y=60)
    l2 = Label(overall_rank, text='Nom')
    l2.place(x=70, y=60)
    l3 = Label(overall_rank, text='Equipe')
    l3.place(x=130, y=60)
    l4 = Label(overall_rank, text='Dossard')
    l4.place(x=190, y=60)

    scb1 = Scrollbar(overall_rank, orient='vertical', command=c1.yview)
    scb1.grid(row=0, column=2, sticky='ns')

    c1['yscrollcommand'] = scb1.set

    overall_rank.bind('<MouseWheel>', mouse_scroll)
    """move_text()"""
    move_bar()
    c1.grid(row=0, column=0)

    overall_rank.mainloop()


def sprint():
    def mouse_scroll(e):
        if e.delta < 0:
            c1.yview_scroll(1, 'units')
        elif e.delta > 0:
            c1.yview_scroll(-1, 'units')

    def retour():
        sprint_rank.destroy()

    connexion = sqlite3.connect("classement_2019.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM Rankings WHERE Sprint > 1 ")
    result = curseur.fetchall()
    result = sorted(result, key=lambda x: x[4], reverse=True)
    chaine = " "

    for r in result:
        r = list(r)
        del r[5]
        del r[0]
        del r[2]
        print(r)
        chaine = chaine + str(r) + "\n" + "\n"
        chaine = chaine.replace(',', '\t')
        chaine = chaine.replace("'", " ")
        chaine = chaine.replace("[", " ")
        chaine = chaine.replace("]", " ")
        # chaine = str(chaine)

    connexion.close()

    sprint_rank = Tk()
    sprint_rank.title("Classement meilleur sprinteur")
    c1 = Canvas(sprint_rank)
    c1.create_text(0, 0, anchor=NW, text=chaine)
    c1.grid(row=1, column=0)

    lo = Label(sprint_rank, text="Le classement du meilleur sprinteur 2019")
    lo.grid(row=0, column=0)

    bo = Button(sprint_rank, text="Retour", command=retour)
    bo.grid(row=6, column=4)
    scb1 = Scrollbar(sprint_rank, orient='vertical', command=c1.yview)
    scb1.grid(row=0, column=2, sticky='ns')
    l1 = Label(sprint_rank, text='Nom')
    l1.place(x=6, y=60)
    l2 = Label(sprint_rank, text='Equipe')
    l2.place(x=70, y=60)
    l3 = Label(sprint_rank, text='Points')
    l3.place(x=140, y=60)
    c1['yscrollcommand'] = scb1.set

    sprint_rank.bind('<MouseWheel>', mouse_scroll)
    """move_text()"""
    move_bar()
    c1.grid(row=0, column=0)

    sprint_rank.mainloop()

def kom ():
    def mouse_scroll(e):
        if e.delta < 0:
            c1.yview_scroll(1, 'units')
        elif e.delta > 0:
            c1.yview_scroll(-1, 'units')

    def retour():
        kom_rank.destroy()

    connexion = sqlite3.connect("classement_2019.db")
    curseur = connexion.cursor()

    curseur.execute("SELECT * FROM Rankings WHERE KOM > 1 ")
    result = curseur.fetchall()
    result=sorted(result, key=lambda x: x[5], reverse=True)
    chaine = " "
    # i = 1
    for r in result:
        r = list(r)
        del r[0]
        del r[3]
        del r[2]
        chaine = chaine + str(r) + "\n" + "\n"
        chaine = chaine.replace(',', '\t')
        chaine = chaine.replace("'", " ")
        chaine = chaine.replace("[", " ")
        chaine = chaine.replace("]", " ")
        # i += 1

    connexion.close()

    kom_rank = Tk()
    kom_rank.title("Classement meilleur grimpeur")
    c1 = Canvas(kom_rank)
    c1.create_text(0, 0, anchor=NW, text=chaine)
    c1.grid(row=1, column=0)

    lo = Label(kom_rank, text="Le classement du meilleur grimpeur 2019")
    lo.grid(row=0, column=0)
    l1 = Label(kom_rank, text='Nom')
    l1.place(x=6, y=60)
    l2 = Label(kom_rank, text='Equipe')
    l2.place(x=70, y=60)
    l3 = Label(kom_rank, text='Points')
    l3.place(x=140, y=60)

    bo = Button(kom_rank, text="Retour", command=retour)
    bo.grid(row=6, column=4)

    scb1 = Scrollbar(kom_rank, orient='vertical', command=c1.yview)
    scb1.grid(row=0, column=2, sticky='ns')

    c1['yscrollcommand'] = scb1.set

    kom_rank.bind('<MouseWheel>', mouse_scroll)
    """move_text()"""
    move_bar()
    c1.grid(row=0, column=0)

    kom_rank.mainloop()


def stats():

    def lbget():
        select = listetk.get()
        if select == ('Pourcentages des équipes présentes dans le top 10 du général'):
            stats1()
            # fenetre.destroy()
        elif select == ('Pourcentages des équipes présentes dans le top 10 du classement sprint'):
            stats2()
        elif select == ('Pourcentages des équipes présentes dans le top 10 du classement de la montagne'):
            stats3()


    fenetre = Tk()
    fenetre.title('Statistiques 2019')
    fenetre.geometry("500x100")
    Liste = ['Pourcentages des équipes présentes dans le top 10 du général', 'Pourcentages des équipes présentes dans le top 10 du classement sprint', 'Pourcentages des équipes présentes dans le top 10 du classement de la montagne']
    listetk = ttk.Combobox(fenetre, values=Liste, width=200, justify=CENTER)
    # listetk.bind("<<ComboboxSelected>>", choix)
    listetk.pack()
    b1 = Button(fenetre, text='Valider', command=lbget)
    b1.pack()
    # l1 = Label(fenetre, text='Pourcentages des équipes présentes dans le top 10 du général')
    # l1.grid(row=0, column=0)
    # l2 = Label(fenetre, text='Pourcentages des équipes présentes dans le top 10 du classement sprint')
    # l2.grid(row=2, column=0)
    # l3 = Label(fenetre, text='Pourcentages des équipes présentes dans le top 10 du classement de la montagne')
    # l3.grid(row=4, column=0)
    # b1 = Button(fenetre, text='Afficher', command=stats1)
    # b1.grid(row=1, column=0)
    # b2 = Button(fenetre, text='Afficher', command=stats2)
    # b2.grid(row=3, column=0)
    # b3 = Button(fenetre, text='Afficher', command=stats3)
    # b3.grid(row=5, column=0)
    fenetre.mainloop()

def stats1():
    TEAMS = ['DQT', 'INS', 'BOH', 'ALM', 'TBM', 'GFC', 'MOV', 'AST', 'TJV', 'EF1', 'MTS', 'CCC', 'UAD', 'TFS', 'SUN', 'COF', 'LTS', 'TDE', 'TKA', 'WGG', 'TDD', 'PCB']
    T = []
    L = []
    # i = 0
    for name in TEAMS:
        connexion = sqlite3.connect('classement_2019.db')
        curseur = connexion.cursor()
        curseur.execute("SELECT Name FROM Rankings WHERE TEAM = ? AND Rank < 10", (name,))
        result = curseur.fetchall()
        connexion.close()
        nbre = len(result)
        if nbre != 0:
            L.append(nbre)
            T.append(name)
    # print(L)
    plt.pie(L, labels=T, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Pourcentages des équipes présentes dans \n le top 10 du général')
    plt.show()


def stats2():
    TEAMS = ['DQT', 'INS', 'BOH', 'ALM', 'TBM', 'GFC', 'MOV', 'AST', 'TJV', 'EF1', 'MTS', 'CCC', 'UAD', 'TFS', 'SUN', 'COF', 'LTS', 'TDE', 'TKA', 'WGG', 'TDD', 'PCB']
    T = []
    L = []
    for name in TEAMS:
        connexion = sqlite3.connect('classement_2019.db')
        curseur = connexion.cursor()
        curseur.execute("SELECT Name FROM Rankings WHERE TEAM = ? AND Sprint >= 119", (name,))
        result = curseur.fetchall()
        connexion.close()
        nbre = len(result)
        if nbre != 0:
            L.append(nbre)
            T.append(name)
    plt.pie(L, labels=T, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Pourcentages des équipes présentes dans \n le top 10 du classement sprint')
    plt.show()


def stats3():
    TEAMS = ['DQT', 'INS', 'BOH', 'ALM', 'TBM', 'GFC', 'MOV', 'AST', 'TJV', 'EF1', 'MTS', 'CCC', 'UAD', 'TFS', 'SUN', 'COF', 'LTS', 'TDE', 'TKA', 'WGG', 'TDD', 'PCB']
    T = []
    L = []
    for name in TEAMS:
        connexion = sqlite3.connect('classement_2019.db')
        curseur = connexion.cursor()
        curseur.execute("SELECT Name FROM Rankings WHERE TEAM = ? AND KOM >= 42", (name,))
        result = curseur.fetchall()
        connexion.close()
        nbre = len(result)
        if nbre != 0:
            L.append(nbre)
            T.append(name)
    plt.pie(L, labels=T, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Pourcentages des équipes présentes dans \n le top 10 du classement de la montagne")
    plt.show()


# Race Predictor


def connect():

    def signin():
        fenetre.destroy()
        signin1()

    def signup():
        fenetre.destroy()
        signup1()

    fenetre = Tk()
    fenetre.title('Connexion')
    # fenetre.geometry('400x400')
    l1 = Label(fenetre, text='Vous avez déjà fait une prédiction ?')
    # l1.place(relx=0.2, rely=0.3)
    l1.grid(row=0, column=0)
    b1 = Button(fenetre, text='Connexion', command=signin)
    # b1.place(relx=0.3, rely=0.35, height=50, width=160)
    b1.grid(row=0, column=1)
    l2 = Label(fenetre, text='Vous êtes nouveau ?')
    # l2.place(relx=0.25, rely=0.45)
    l2.grid(row=1, column=0)
    b2 = Button(fenetre, text='Inscrivez-vous', command=signup)
    # b2.place(relx=0.3, rely=0.5, height=50, width=160)
    b2.grid(row=1, column=1)
    fenetre.mainloop()


def signin1():

    def db_searchconnex():

        connexion = sqlite3.connect("classement_2019.db")
        curseur = connexion.cursor()
        username = str(e1.get())
        password = str(e2.get())
        curseur.execute("SELECT IdUser FROM User WHERE (Mail, Mdp) = (?,?)", (username, password))
        result = curseur.fetchone()
        # print(result)
        connexion.close()

        if(result is None):
            tkinter.messagebox.showinfo('Attention', "L'email et le mot de passe ne correspondent pas")
            e1.delete(0, END)
            e2.delete(0, END)
        else:
            sign.destroy()
            prediction_course(result[0])

    def retour():
        sign.destroy()
        connect()

    sign = Tk()
    sign.title("Se connecter")
    l1 = Label(sign, text="Adresse mail")
    l1.grid(row=0, column=0)
    l2 = Label(sign, text='Mot de Passe')
    l2.grid(row=1, column=0)
    e1 = Entry(sign)
    e1.grid(row=0, column=1)
    e2 = Entry(sign, show='*')
    e2.grid(row=1, column=1)
    b1 = Button(sign, text='Connexion', command=db_searchconnex)
    b1.grid(row=2, column=1)
    b2 = Button(sign, text="Retour", command=retour)
    b2.grid(row=2, column=0)

    sign.mainloop()


def signup1():

    def password_check():

        pass1 = str(e5.get())
        pass2 = str(e6.get())
        mail = str(e1.get())

        connexion = sqlite3.connect("classement_2019.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT IdUser FROM User WHERE Mail = ?", (mail,))
        result = curseur.fetchone()
        connexion.close()

        if result is None:
            if (pass1 == pass2):
                connexion = sqlite3.connect("classement_2019.db")
                curseur = connexion.cursor()
                name = str(e2.get())
                surname = str(e3.get())
                phone = str(e4.get())
                curseur.execute("INSERT INTO User ('Nom', 'Prenom', 'Mail', 'Telephone', 'Mdp') VALUES (?, ?, ?, ?, ?)", (name, surname, mail, phone, pass1))
                connexion.commit()
                curseur.execute("SELECT IdUser from User WHERE Mail = ?", (mail,))
                result = curseur.fetchone()
                connexion.close()
                tkinter.messagebox.showinfo("Information", "Inscription prise en compte")
                register.destroy()
                prediction_course(result[0])
            else:
                tkinter.messagebox.showinfo('Erreur', 'Les mots de Passe ne correspondent pas')
                e5.delete(0, END)
                e6.delete(0, END)
        else:
            tkinter.messagebox.showinfo('Attention', 'Mail déjà utilisé')
            e1.delete(0, END)

    def retour():
        register.destroy()
        connect()

    register = Tk()
    register.title('Inscription')
    l1 = Label(register, text='Adresse Mail : ')
    l1.grid(row=0, column=0)
    e1 = Entry(register)
    e1.grid(row=0, column=1)
    l2 = Label(register, text='Nom : ')
    l2.grid(row=1, column=0)
    e2 = Entry(register)
    e2.grid(row=1, column=1)
    l3 = Label(register, text='Prénom : ')
    l3.grid(row=2, column=0)
    e3 = Entry(register)
    e3.grid(row=2, column=1)
    l4 = Label(register, text='Téléphone : ')
    l4.grid(row=3, column=0)
    e4 = Entry(register)
    e4.grid(row=3, column=1)
    l5 = Label(register, text='Mot de Passe : ')
    l5.grid(row=4, column=0)
    e5 = Entry(register, show='*')
    e5.grid(row=4, column=1)
    l6 = Label(register, text='Confirmation Mot de Passe : ')
    l6.grid(row=5, column=0)
    e6 = Entry(register, show='*')
    e6.grid(row=5, column=1)

    b1 = Button(register, text="S'inscrire", command=password_check)
    b1.grid(row=6, column=1)
    b2 = Button(register, text="Retour", command=retour, background='red')
    b2.grid(row=6, column=0)
    register.mainloop()

def prediction_course(IdUser):
    # print(IdUser)
    def recherche_coureur(place):

        def doButton(evt):
            # print(evt.widget.myId)
            team_name = str(evt.widget.myId)
            # print(type(team_name))
            affichage_coureur(team_name)

        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)[0]
            # print('You selected item %d: "%s"' % (index, value))
            if place == 'premier':
                l9.config(text=value)
                # print('Le premier sera modifié')
            elif place == 'deuxieme':
                # print('Le deuxieme sera modifié')
                l10.config(text=value)
            elif place == 'troisieme':
                l11.config(text=value)
            elif place == 'quatrieme':
                l12.config(text=value)
            elif place == 'cinquieme':
                l13.config(text=value)
            elif place == 'sprint':
                l14.config(text=value)
            elif place == 'kom':
                l15.config(text=value)
            fenetre.destroy()
            fen.destroy()

        def affichage_coureur(name):
            connexion = sqlite3.connect('classement_2019.db')
            curseur = connexion.cursor()
            curseur.execute('SELECT Name FROM Rankings WHERE Team = ?', (name,))
            result = curseur.fetchall()
            # print(result)
            connexion.close()
            global fen
            fen = Tk()
            fen.title("Coureurs de l'équipe " + name)
            lb = Listbox(fen, name='lb')
            lb.bind('<<ListboxSelect>>', onselect)
            n = 0
            for coureur in result:
                lb.insert(n, coureur)
                n += 1
            lb.grid(row=0, column=0)
            fen.mainloop()

        fenetre = Tk()
        fenetre.title('Recherche de Coureur')
        TEAMS2 = ['Deceuninck Quick Step', 'Ineos', 'Bora Hansgrohe', 'AG2R La Mondiale', 'Team Bahrain Merida', 'Groupama FDJ', 'Movistar', 'Astana', 'Team Jumbo Visma', 'Education First', 'Mitchelton Scott', 'CCC', 'UAE Team Emirates', 'Trek Segafredo', 'Sunweb', 'Cofidis', 'Lotto Soudal', 'Total Direct Energie', 'Katusha', 'Wanty Gobert', 'Dimension Data', 'Arkea Samsic']
        TEAMS = ['DQT', 'INS', 'BOH', 'ALM', 'TBM', 'GFC', 'MOV', 'AST', 'TJV', 'EF1', 'MTS', 'CCC', 'UAD', 'TFS', 'SUN', 'COF', 'LTS', 'TDE', 'TKA', 'WGG', 'TDD', 'PCB']
        max_column = 10
        line = 0
        col = 0
        i = 0
        for name in TEAMS:
            b = Button(fenetre, text=TEAMS2[i])
            b.grid(row=line, column=col)
            b.bind("<Button-1>", doButton)
            b.myId = name
            col += 1
            i += 1
            if col == 11:
                line = 1
                col = 0
        fenetre.mainloop()

    def get():
        # print('Validé !')
        premier = l9.cget("text")
        deuxieme = l10.cget("text")
        troisieme = l11.cget("text")
        quatrieme = l12.cget("text")
        cinquieme = l13.cget("text")
        sprint = l14.cget("text")
        kom = l15.cget("text")

        # print(premier, deuxieme, troisieme, quatrieme, cinquieme, sprint, kom)
        connexion = sqlite3.connect('classement_2019.db')
        curseur = connexion.cursor()

        if not(Inscrit):
            curseur.execute("INSERT INTO Choix ('IdUser', 'Firstoverall', 'Secondoverall', 'Thirdoverall', 'Fourthoverall', 'Fifthoverall', 'FirstSprint', 'FirstKOM') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (IdUser, premier, deuxieme, troisieme, quatrieme, cinquieme, sprint, kom))
            connexion.commit()
            # connexion.close()
        else:
            curseur.execute("UPDATE Choix SET ('Firstoverall', 'Secondoverall', 'Thirdoverall', 'Fourthoverall', 'Fifthoverall', 'FirstSprint', 'FirstKOM') = (?, ?, ?, ?, ?, ?, ?) Where IdUser = ?", (premier, deuxieme, troisieme, quatrieme, cinquieme, sprint, kom, IdUser))
            connexion.commit()
            # connexion.close()
        #tkinter.messagebox.showinfo('Information', 'Prédiction prise en compte !')
        curseur.execute("SELECT IdUser From Choix WHERE Firstoverall = ?", (premier,))
        result = curseur.fetchall()
        nombre = len(result)-1
        # connexion.close()
        if nombre != 0:
            tkinter.messagebox.showinfo('Information', str(nombre) + ' Personne(s) a (ont) prédit le même vainqueur que vous !')
        else :
            tkinter.messagebox.showinfo('Information', 'Prédiction prise en compte !')

        maliste = [premier, deuxieme, troisieme, quatrieme, cinquieme]
        teamlist = []
        for coureur in maliste:
            curseur.execute("SELECT Team From Rankings WHERE Name = ?", (coureur,))
            result = curseur.fetchone()
            # print('a:', result[0])
            teamlist.append(result[0])
        n = 0
        nbre = []
        T = []
        T2 = []
        L2 = []
        TEAMS = ['DQT', 'INS', 'BOH', 'ALM', 'TBM', 'GFC', 'MOV', 'AST', 'TJV', 'EF1', 'MTS', 'CCC', 'UAD', 'TFS', 'SUN', 'COF', 'LTS', 'TDE', 'TKA', 'WGG', 'TDD', 'PCB']
        for team in TEAMS:
            n = teamlist.count(team)
            curseur.execute("SELECT Name FROM Rankings WHERE TEAM = ? AND Rank <= 5", (team,))
            result = curseur.fetchall()
            # connexion.close()
            nombre = len(result)
            if nombre != 0:
                L2.append(nombre)
                T2.append(team)
            if n != 0:
                nbre.append(n)
                T.append(team)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle('Comparaison des pourcentages des équipes présentes dans \n le top 5 du classement général \n de 2019 (à gauche) avec votre prédicition (à droite)')
        ax1.pie(L2, labels=T2, autopct='%1.1f%%', startangle=90)
        ax2.pie(nbre, labels=T, autopct='%1.1f%%', startangle=90)
        plt.show()
        connexion.close()
        predict.destroy()

    def doButton1(evt):
        place = str(evt.widget.myId)
        print(evt.widget.myId)
        recherche_coureur(place)

    connexion = sqlite3.connect('classement_2019.db')
    curseur = connexion.cursor()
    curseur.execute("SELECT Firstoverall, Secondoverall, Thirdoverall, Fourthoverall, Fifthoverall, FirstSprint, FirstKOM FROM Choix Where IdUser = ?", (IdUser,))
    result = curseur.fetchone()
    # print(result)
    connexion.close()
    predict = Tk()
    predict.title("Race Predictor")
    predict.geometry('600x200')

    l1 = Label(predict, text='Classement général', background='yellow2')
    l1.grid(row=0, column=1)
    l2 = Label(predict, text='1er')
    l2.grid(row=1, column=0)

    b1 = Button(predict, text='Ajouter un coureur')
    b1.grid(row=1, column=2)
    b1.bind("<Button-1>", doButton1)
    b1.myId = 'premier'
    l3 = Label(predict, text='2ème')
    l3.grid(row=2, column=0)

    b2 = Button(predict, text='Ajouter un coureur')
    b2.grid(row=2, column=2)
    b2.bind("<Button-1>", doButton1)
    b2.myId = 'deuxieme'
    l4 = Label(predict, text='3ème')
    l4.grid(row=3, column=0)

    b3 = Button(predict, text='Ajouter un coureur')
    b3.grid(row=3, column=2)
    b3.bind("<Button-1>", doButton1)
    b3.myId = 'troisieme'
    l5 = Label(predict, text='4ème')
    l5.grid(row=4, column=0)

    b4 = Button(predict, text='Ajouter un coureur')
    b4.grid(row=4, column=2)
    b4.bind("<Button-1>", doButton1)
    b4.myId = 'quatrieme'
    l6 = Label(predict, text='5ème')
    l6.grid(row=5, column=0)

    b5 = Button(predict, text='Ajouter un coureur')
    b5.grid(row=5, column=2)
    b5.bind("<Button-1>", doButton1)
    b5.myId = 'cinquieme'
    l7 = Label(predict, text='Meilleur Sprinteur', background='lime green')
    l7.grid(row=0, column=3)

    b6 = Button(predict, text='Ajouter un coureur')
    b6.grid(row=1, column=4)
    b6.bind("<Button-1>", doButton1)
    b6.myId = 'sprint'
    l8 = Label(predict, text='Meilleur Grimpeur', background='red')
    l8.grid(row=3, column=3)

    b7 = Button(predict, text='Ajouter un coureur')
    b7.grid(row=4, column=4)
    b7.bind("<Button-1>", doButton1)
    b7.myId = 'kom'
    b8 = Button(predict, text='Valider', command=get)
    b8.grid(row=6, column=4)

    if result is None:
        Inscrit = False
        l9 = Label(predict, text='')
        l9.grid(row=1, column=1)
        l10 = Label(predict, text='')
        l10.grid(row=2, column=1)
        l11 = Label(predict, text='')
        l11.grid(row=3, column=1)
        l12 = Label(predict, text='')
        l12.grid(row=4, column=1)
        l13 = Label(predict, text='')
        l13.grid(row=5, column=1)
        l14 = Label(predict, text='')
        l14.grid(row=1, column=3)
        l15 = Label(predict, text='')
        l15.grid(row=4, column=3)
        Inscrit = False
    else:
        Inscrit = True
        l9 = Label(predict, text=result[0])
        l9.grid(row=1, column=1)
        l10 = Label(predict, text=result[1])
        l10.grid(row=2, column=1)
        l11 = Label(predict, text=result[2])
        l11.grid(row=3, column=1)
        l12 = Label(predict, text=result[3])
        l12.grid(row=4, column=1)
        l13 = Label(predict, text=result[4])
        l13.grid(row=5, column=1)
        l14 = Label(predict, text=result[5])
        l14.grid(row=1, column=3)
        l15 = Label(predict, text=result[6])
        l15.grid(row=4, column=3)
    predict.mainloop()
