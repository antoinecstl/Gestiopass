import customtkinter as ctk
from Password import verifier_identifiant as vi, chiffre_mot_de_passe, enregistrer_utilisateur, show_message_box, modifier_user, add_mdp, dechiffre_sans_integr
import sqlite3

#-----Function-----#

def backcnted (actualpage, identifiant, cle_secrete):
    actualpage.destroy()
    home(identifiant, cle_secrete)

def back(actualpage):
    actualpage.destroy()
    main()
    
def backward(actualpage, identifiant, cle_secrete):
    actualpage.destroy()
    mdp_consult(identifiant, cle_secrete)

def valider(revealmdp, revealkey, mdpinput, cle_secrete_input):
    value1 = revealmdp.get()
    value2 = revealkey.get()

    if value1 == 1:
        mdpinput.configure(show="")
    else:
        mdpinput.configure(show="°")

    if value2 == 1:
        cle_secrete_input.configure(show="")
    else:
        cle_secrete_input.configure(show="°")

def reveal(revealmdp, mdpinput):
    value1 = revealmdp.get()

    if value1 == 1:
        mdpinput.configure(show="")
    else:
        mdpinput.configure(show="°")


def connect(idinput, mdpinput, cle_secrete_input, login):
    conn = sqlite3.connect("utilisateurs.db")

    # Récupération de l'identifiant et du mot de passe saisis par l'utilisateur
    identifiant = idinput.get()

    # Vérification si le nom d'utilisateur existe
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = ?", (identifiant,))
    result = cursor.fetchone()

    if result is None:
        show_message_box("Erreur", "Le nom d'utilisateur n'existe pas.")
        return

    mot_de_passe = mdpinput.get()
    # Récupération de la clé secrète saisie par l'utilisateur
    cle_secrete = cle_secrete_input.get()

    # Connexion à la base de données SQLite

    if vi(conn, identifiant, mot_de_passe, cle_secrete):
        print("Identifiant valide.")
        login.destroy()
        home(identifiant, cle_secrete)

    # Fermeture de la connexion à la base de données
    conn.close()

def main():
    #-----Frame setting-----#

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    login = ctk.CTk()
    login.geometry("500x450")
    login.minsize(500,450)
    login.maxsize(500,450)
    login.title("Portail")
    frame = ctk.CTkFrame(master=login)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    #-----Frame Elements-----#

    label = ctk.CTkLabel(master=frame, text="Se connecter", font=("", 20, "bold"), justify="center")
    label.pack(pady=14, padx=10)

    idinput = ctk.CTkEntry(master=frame, placeholder_text="Profil")
    idinput.pack(pady=10)

    mdpinput = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="°")
    mdpinput.pack(pady=10)

    revealmdp = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealmdp.pack(pady=12, padx=10)

    cle_secrete_input = ctk.CTkEntry(master=frame, placeholder_text="Clé secrète", show="°")
    cle_secrete_input.pack(pady=12)

    revealkey = ctk.CTkCheckBox(master=frame, text="Afficher la clé", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealkey.pack(pady=12, padx=10)

    cntbutton = ctk.CTkButton(master=frame, text="Connexion", command=lambda: connect(idinput, mdpinput, cle_secrete_input, login))
    cntbutton.pack(pady=12, padx=10)

    """home(idinput, cle_secrete_input.get()) connect(idinput, mdpinput, cle_secrete_input, login)"""

    newusbtn = ctk.CTkButton(master=frame, text="Nouveau profil", command=lambda: New_user(login))
    newusbtn.pack(pady=12, padx=10)

    login.mainloop()
def New_user(login):
    def eu():
        identifiant = idinput.get()
        mot_de_passe = mdpinput.get()
        cle_secrete = cle_secrete_input.get()
        conn = sqlite3.connect("utilisateurs.db")
        enregistrer_utilisateur(conn, identifiant, mot_de_passe, cle_secrete)
        conn.close()
        New_user.destroy()
        show_message_box("Enregistrement réussi", "Le profil a été crée")
        main()

    login.destroy()

    # -----Frame setting-----#
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    New_user = ctk.CTk()
    New_user.geometry("500x410")
    New_user.minsize(500,410)
    New_user.maxsize(500,410)
    New_user.title("Nouveau profil")
    frame = ctk.CTkFrame(master=New_user)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    #-----Frame Elements-----#
    label = ctk.CTkLabel(master=frame, text="Créer un profil", font=("", 20, "bold"), justify="center")
    label.pack(pady=14, padx=10)

    idinput = ctk.CTkEntry(master=frame, placeholder_text="Nom du Profil")
    idinput.pack(pady=10)

    mdpinput = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="°")
    mdpinput.pack(pady=10)

    revealmdp = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealmdp.pack(pady=12, padx=10)

    cle_secrete_input = ctk.CTkEntry(master=frame, placeholder_text="Clé secrète à retenir",  show="°")
    cle_secrete_input.pack(pady=12)

    revealkey = ctk.CTkCheckBox(master=frame, text="Afficher la clé", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealkey.pack(pady=12, padx=10)

    crtbutton = ctk.CTkButton(master=frame, text="Créer", command=lambda: eu())
    crtbutton.pack(pady=12, padx=10)

    returnbutton = ctk.CTkButton(master=frame, text="Retour", command=lambda: back(New_user), width=20, height=25, corner_radius=100, fg_color="#4a4a4a", hover_color="#2b2b2b")
    returnbutton.place(x=12, y=12)

    New_user.mainloop()

def home(identifiant, cle_secrete):

    def deco():
        home.destroy()
        main()

    #-----Frame setting-----#

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    home = ctk.CTk()
    home.geometry("380x430")
    home.minsize(500,450)
    home.maxsize(500,450)
    home.title("Accueil")
    frame = ctk.CTkFrame(master=home)
    frame.pack(pady=20, padx=60, fill="both", expand=True)


    # -----Frame Elements-----#

    label = ctk.CTkLabel(master=frame, text=f"GestioPass de {identifiant}", font=("", 22, "bold"), justify="center")
    label.pack(pady=14, padx=10)

    consultbutton = ctk.CTkButton(master=frame, text="Consulter mes mots de passe", font=("", 16, "bold"), width=300, height=80, command=lambda: openmdpconsult(home, identifiant, cle_secrete), corner_radius=8, border_width=1, border_color="white", fg_color="#4a4a4a", hover_color="#2b2b2b")
    consultbutton.pack(pady=16, padx=10)

    modifbutton = ctk.CTkButton(master=frame, text="Modifier mon profil Gestiopass",font=("", 16, "bold"), width=300, height=80, command=lambda: modif_user(home,identifiant, cle_secrete), corner_radius=8,  border_width=1, border_color="white", fg_color="#4a4a4a", hover_color="#2b2b2b")
    modifbutton.pack(pady=16, padx=10)

    decobutton = ctk.CTkButton(master=frame, text="Se déconnecter",font=("", 16, "bold"), width=150, height=40, command=lambda: deco(), corner_radius=100)
    decobutton.pack(pady=24, padx=10)

    home.mainloop()

def homedestroy (home):
    home.destroy()

def mdp_consult(identifiant, cle_secrete):
    # -----Frame setting-----#

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    mdpcons = ctk.CTk()
    mdpcons.geometry("500x600")
    mdpcons.minsize(500,600)
    mdpcons.maxsize(500,600)
    mdpcons.title("Le GestioPass")

    framedad = ctk.CTkFrame(master=mdpcons)
    framedad.pack(pady=10, padx=10, fill="both", expand=True)

    frame_buttons = ctk.CTkFrame(master=framedad)
    frame_buttons.pack(pady=10)

    add_button = ctk.CTkButton(master=frame_buttons, text="+", font=("",18,"bold"), command=lambda: addmdp(mdpcons, identifiant, cle_secrete, home))
    add_button.pack(side="left", padx=10)

    return_button = ctk.CTkButton(master=frame_buttons, text="Retour", command=lambda: backcnted(mdpcons, identifiant, cle_secrete), fg_color="#4a4a4a", hover_color="#2b2b2b")
    return_button.pack(side="left", padx=10)

    scrollable_frame = ctk.CTkScrollableFrame(master=framedad, height=200)
    scrollable_frame.pack(padx=20, pady=5, fill="both", expand=True)


    def element(scrollable_frame, texte, Plateforme, pseudo, mdp, note, plat_crypt, pseudo_crypt):
        # Créer un label avec le texte souhaité
        button_element = ctk.CTkButton(master=scrollable_frame, text=texte, font=("", 18, ), height=60, width=380, command=lambda: seemdp(Plateforme, pseudo, mdp, note, plat_crypt, pseudo_crypt))
        button_element.pack(padx=10, pady=7)

    def consult_bdd():
        conn = sqlite3.connect('utilisateurs.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM mdp WHERE Nom_utilisateur=?", (identifiant,))
        rows = cursor.fetchall()

        #Dechiffrage + Recup de ce qu'on veut afficher sur les boutons.
        for row in rows:
            plat_crypt = row[1]
            pseudo_crypt = row[2]
            mdp_crypt = row[3]
            nonce_mdp = row[4]
            nonce_pseudo = row[5]
            nonce_plat = row[6]
            note_crypt = row[7]
            nonce_note = row[8]

            plat_decrypt = dechiffre_sans_integr(plat_crypt, nonce_plat, cle_secrete)
            pseudo_decrypt = dechiffre_sans_integr(pseudo_crypt, nonce_pseudo, cle_secrete)
            mdp_decrypt = dechiffre_sans_integr(mdp_crypt, nonce_mdp, cle_secrete)
            note_decrypt = dechiffre_sans_integr(note_crypt, nonce_note, cle_secrete)
            element(scrollable_frame,f"{plat_decrypt} \n {pseudo_decrypt}",plat_decrypt, pseudo_decrypt, mdp_decrypt, note_decrypt, plat_crypt, pseudo_crypt)

    def seemdp(Plateforme, pseudo, mdp, note, plat_crypt, pseudo_crypt):
        # -----Frame setting-----#

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        mdpcons.destroy()
        see_mdp = ctk.CTk()
        see_mdp.geometry("500x450")
        see_mdp.minsize(500, 450)
        see_mdp.maxsize(500, 450)
        see_mdp.title("")

        def modifier():
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
            see_mdp.destroy()
            modif_mdp = ctk.CTk()
            modif_mdp.geometry("500x450")
            modif_mdp.minsize(500, 450)
            modif_mdp.maxsize(500, 450)
            modif_mdp.title("")

            framedad = ctk.CTkFrame(master=modif_mdp)
            framedad.pack(pady=20, padx=20, fill="both", expand=True)

            frame_plateforme = ctk.CTkFrame(master=framedad)
            frame_plateforme.pack(padx=15, pady=15, fill="x")

            label_plateforme_title = ctk.CTkLabel(master=frame_plateforme, text="Plateforme:", font=("", 18, "bold"))
            label_plateforme_title.pack(side="left", padx=10)

            label_element_plateforme = ctk.CTkLabel(master=frame_plateforme, text=Plateforme, font=("", 16), wraplength=350)
            label_element_plateforme.pack(side="left", padx=10)

            frame_pseudo = ctk.CTkFrame(master=framedad)
            frame_pseudo.pack(padx=15, pady=15, fill="x")

            label_pseudo_title = ctk.CTkLabel(master=frame_pseudo, text="Pseudo:", font=("", 18, "bold"))
            label_pseudo_title.pack(side="left", padx=10)

            label_element_pseudo = ctk.CTkLabel(master=frame_pseudo, text= pseudo, font=("", 16), wraplength=350)
            label_element_pseudo.pack(side="left", padx=10)

            frame_mdp = ctk.CTkFrame(master=framedad)
            frame_mdp.pack(padx=15, pady=15, fill="x")

            label_mdp_title = ctk.CTkLabel(master=frame_mdp, text="Mot de passe:", font=("", 18, "bold"))
            label_mdp_title.pack(side="left", padx=10)

            label_element_mdp = ctk.CTkEntry(master=frame_mdp, placeholder_text="Nouveau mot de passe", font=("", 16), width=290)
            label_element_mdp.pack(side="left", padx=10)

            frame_note = ctk.CTkFrame(master=framedad)
            frame_note.pack(padx=15, pady=15, fill="x")

            label_note_title = ctk.CTkLabel(master=frame_note, text="Note:", font=("", 18, "bold"))
            label_note_title.pack(side="left", padx=10)

            label_element_note = ctk.CTkEntry(master=frame_note, placeholder_text="Nouvelle note", font=("", 16),  width=350)
            label_element_note.pack(side="left", padx=10)

            def modifier_mdp_note(identifiant, nouveau_mdp, nouvelle_note):

                mot_de_passe_chiffre_base64, nonce_mdp_base64, pop = chiffre_mot_de_passe(nouveau_mdp, cle_secrete)
                note_chiffre64, nonce_note_base64, _ = chiffre_mot_de_passe(nouvelle_note, cle_secrete)

                conn = sqlite3.connect('utilisateurs.db')
                cursor = conn.cursor()

                cursor.execute("UPDATE mdp SET mot_de_passe_chiffre = ?, Note = ?, nonce_mdp = ?, nonce_note = ? WHERE Nom_utilisateur = ? AND Plateforme = ? AND pseudo = ?",
                               (mot_de_passe_chiffre_base64, note_chiffre64,nonce_mdp_base64, nonce_note_base64, identifiant, plat_crypt, pseudo_crypt))

                conn.commit()
                conn.close()

            def govalid():
                mdp = label_element_mdp.get()
                note = label_element_note.get()
                modifier_mdp_note(identifiant, mdp, note)
                modif_mdp.destroy()
                mdp_consult(identifiant, cle_secrete)

            button_frame = ctk.CTkFrame(master=framedad)
            button_frame.pack(pady=10)

            valider_modif = ctk.CTkButton(master=button_frame, text="Valider", command=lambda: govalid())
            valider_modif.pack(side="left", padx=10, pady=10)

            return_button = ctk.CTkButton(master=button_frame, text="Retour", command=lambda: backward(modif_mdp, identifiant, cle_secrete), fg_color="#4a4a4a", hover_color="#2b2b2b")
            return_button.pack(side="left", padx=10, pady=10)

            modif_mdp.mainloop()

        def delete():

            conn = sqlite3.connect('utilisateurs.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mdp WHERE Nom_utilisateur=? AND Plateforme=? AND pseudo=?", (identifiant, plat_crypt, pseudo_crypt))
            conn.commit()
            conn.close()

        def show_message_box_choice(title, message):
            messagebox = ctk.CTk()
            messagebox.geometry("400x155")
            messagebox.minsize(400, 155)
            messagebox.maxsize(400, 155)
            messagebox.title(title)

            label = ctk.CTkLabel(master=messagebox, text=message, font=("", 12), justify="center")
            label.pack(pady=20)

            def call2():
                delete()
                messagebox.destroy()
                see_mdp.destroy()
                mdp_consult(identifiant, cle_secrete)

            button_frame = ctk.CTkFrame(master=messagebox)
            button_frame.pack(pady=10)

            Oui_button = ctk.CTkButton(master=button_frame, text="Oui", command=lambda: call2())
            Oui_button.pack(side="left",padx=10, pady=10)

            Non_button = ctk.CTkButton(master=button_frame, text="Non", command=messagebox.destroy)
            Non_button.pack(side="left", padx=10, pady=10)

            messagebox.mainloop()

        button_frame = ctk.CTkFrame(master=see_mdp)
        button_frame.pack(pady=10)

        modifier_button = ctk.CTkButton(master=button_frame, text="Modifier", command=lambda: modifier())
        modifier_button.pack(side="left", padx=10, pady=10)

        supp_button = ctk.CTkButton(master=button_frame, text="Supprimer", fg_color="#e95a5a", hover_color="#e81c1c", command=lambda: show_message_box_choice("Supprimer", "Êtes-vous sûr de vouloir supprimer ce pass ?"))
        supp_button.pack(side="left", padx=10, pady=10)

        framedad = ctk.CTkFrame(master=see_mdp)
        framedad.pack(pady=20, padx=20, fill="both", expand=True)

        frame_plateforme = ctk.CTkFrame(master=framedad)
        frame_plateforme.pack(padx=15, pady=15, fill="x")

        label_plateforme_title = ctk.CTkLabel(master=frame_plateforme, text="Plateforme:", font=("", 18, "bold"))
        label_plateforme_title.pack(side="left", padx=10)

        label_element_plateforme = ctk.CTkLabel(master=frame_plateforme, text=Plateforme, font=("", 16), wraplength=350)
        label_element_plateforme.pack(side="left", padx=10)

        frame_pseudo = ctk.CTkFrame(master=framedad)
        frame_pseudo.pack(padx=15, pady=15, fill="x")

        label_pseudo_title = ctk.CTkLabel(master=frame_pseudo, text="Pseudo:", font=("", 18, "bold"))
        label_pseudo_title.pack(side="left", padx=10)

        label_element_pseudo = ctk.CTkLabel(master=frame_pseudo, text=pseudo, font=("", 16), wraplength=350)
        label_element_pseudo.pack(side="left", padx=10)

        frame_mdp = ctk.CTkFrame(master=framedad)
        frame_mdp.pack(padx=15, pady=15, fill="x")

        label_mdp_title = ctk.CTkLabel(master=frame_mdp, text="Mot de passe:", font=("", 18, "bold"))
        label_mdp_title.pack(side="left", padx=10)

        label_element_mdp = ctk.CTkLabel(master=frame_mdp, text=mdp, font=("", 16), wraplength=350)
        label_element_mdp.pack(side="left", padx=10)

        frame_note = ctk.CTkFrame(master=framedad)
        frame_note.pack(padx=15, pady=15, fill="x")

        label_note_title = ctk.CTkLabel(master=frame_note, text="Note:", font=("", 18, "bold"))
        label_note_title.pack(side="left", padx=10)

        label_element_note = ctk.CTkLabel(master=frame_note, text=note, font=("", 16), wraplength=350)
        label_element_note.pack(side="left", padx=10)

        return_button = ctk.CTkButton(master=framedad, text="Retour", command=lambda: backward(see_mdp, identifiant, cle_secrete), fg_color="#4a4a4a", hover_color="#2b2b2b")
        return_button.pack(padx=10, pady=10)

        see_mdp.mainloop()

    consult_bdd()

    mdpcons.mainloop()


def openmdpconsult (home, identifiant, cle_secrete):
    homedestroy(home)
    mdp_consult(identifiant, cle_secrete)

def addmdp(mdpcons, nom_user, cle_secrete, home):
    # -----Frame setting-----#
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    mdpcons.destroy()
    addmdpw = ctk.CTk()
    addmdpw.geometry("500x500")
    addmdpw.minsize(500,500)
    addmdpw.maxsize(500,500)
    addmdpw.title("Nouveau mot de passe")
    frame = ctk.CTkFrame(master=addmdpw)
    frame.pack(pady=20, padx=40, fill="both", expand=True)

    label1 = ctk.CTkLabel(master=frame, text="", font=("", 20, "bold"), justify="center")
    label1.pack(pady=14, padx=10)

    label = ctk.CTkLabel(master=frame, text="Ajouter un nouveau mot de passe", font=("", 20, "bold"), justify="center")
    label.pack(pady=14, padx=10)

    platform = ctk.CTkEntry(master=frame, placeholder_text="Plateforme", width=200)
    platform.pack(pady=10)

    username = ctk.CTkEntry(master=frame, placeholder_text="Identifiant", width=200)
    username.pack(pady=10)

    mdpinput = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="°", width=200)
    mdpinput.pack(pady=10)

    revealmdp = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", command=lambda: reveal(revealmdp, mdpinput))
    revealmdp.pack(pady=12, padx=10)

    note = ctk.CTkEntry(master=frame, placeholder_text="Ajouter des notes", width=200, height=40)
    note.pack(pady=10)

    def use2def():
        add_mdp(nom_user, platform.get(), username.get(), mdpinput.get(), note.get(), cle_secrete)
        addmdpw.destroy()
        mdp_consult(nom_user, cle_secrete)

    cntbutton = ctk.CTkButton(master=frame, text="Ajouter",  command=lambda: use2def())
    cntbutton.pack(pady=12, padx=10)
    
    returnbutton = ctk.CTkButton(master=frame, text="Retour", command=lambda: backward(addmdpw, nom_user, cle_secrete), width=25, height=25, corner_radius=100, fg_color="#4a4a4a", hover_color="#2b2b2b")
    returnbutton.place(x=12, y=12)

    addmdpw.mainloop()

def modif_user (home, identifiant, cle_secrete):
    def mu():
        mot_de_passe = mdpinput.get()
        cle_secrete = cle_secrete_input.get()
        newmot_de_passe = newmdpinput.get()
        conn = sqlite3.connect("utilisateurs.db")
        modifier_user(conn, identifiant, mot_de_passe, cle_secrete, newmot_de_passe)
        conn.close()
        modifuser.destroy()
        show_message_box("Enregistrement réussi", "Le profil a été modifié")
        main()
    # -----Frame setting-----#

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    home.destroy()
    modifuser = ctk.CTk()
    modifuser.geometry("500x500")
    modifuser.minsize(500,500)
    modifuser.maxsize(500,500)
    modifuser.title("Modifier mon profil")
    frame = ctk.CTkFrame(master=modifuser)
    frame.pack(pady=20, padx=40, fill="both", expand=True)

    # -----Frame Elements-----#
    label = ctk.CTkLabel(master=frame, text="Modifier mon profil", font=("", 22, "bold"), justify="center")
    label.pack(pady=14, padx=10)

    profil = ctk.CTkButton(master=frame, text=identifiant, font=("", 18,"bold"),width=20, border_width=2, fg_color="#262626", hover=False, border_color="#878787")
    profil.pack(pady=11, padx=10)

    mdpinput = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe actuel", width=150, show="°")
    mdpinput.pack(pady=10)

    revealmdp = ctk.CTkCheckBox(master=frame, text="Afficher le mot de passe", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealmdp.pack(pady=12, padx=10)

    cle_secrete_input = ctk.CTkEntry(master=frame, placeholder_text="Clé secrète actuelle", width=150, show="°")
    cle_secrete_input.pack(pady=12)

    revealkey = ctk.CTkCheckBox(master=frame, text="Afficher la clé", command=lambda: valider(revealmdp, revealkey, mdpinput, cle_secrete_input))
    revealkey.pack(pady=12, padx=10)

    newmdpinput = ctk.CTkEntry(master=frame, placeholder_text="Nouveau Mot de passe", width=150)
    newmdpinput.pack(pady=10)

    crtbutton = ctk.CTkButton(master=frame, text="Modifier", command=lambda: mu())
    crtbutton.pack(pady=12, padx=10)

    returnbutton = ctk.CTkButton(master=frame, text="Retour", command=lambda: backcnted(modifuser, identifiant, cle_secrete), width=25, height=25, corner_radius=100, fg_color="#4a4a4a", hover_color="#2b2b2b")
    returnbutton.place(x=12, y=12)

    modifuser.mainloop()


main()