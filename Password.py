import hashlib
import sqlite3
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
import customtkinter as ctk
import re

def show_message_box(title, message):
    messagebox = ctk.CTk()
    messagebox.geometry("400x125")
    messagebox.minsize(400,125)
    messagebox.maxsize(400,125)
    messagebox.title(title)

    label = ctk.CTkLabel(master=messagebox, text=message, font=("", 12), justify="center")
    label.pack(pady=20)

    ok_button = ctk.CTkButton(master=messagebox, text="OK", command=messagebox.destroy)
    ok_button.pack(pady=10)

    messagebox.mainloop()

def chiffre_mot_de_passe(mot_de_passe, cle_secrete):
    # Salage du mot de passe
    sel = get_random_bytes(16)
    mot_de_passe_sale = sel + mot_de_passe.encode()

    # Chiffrement du mot de passe
    cle_hash = hashlib.sha256(cle_secrete.encode()).digest()
    cipher = AES.new(cle_hash, AES.MODE_EAX)
    nonce = cipher.nonce
    mot_de_passe_chiffre, tag = cipher.encrypt_and_digest(mot_de_passe_sale)

    # Conversion en format de texte lisible
    mot_de_passe_chiffre_base64 = b64encode(mot_de_passe_chiffre).decode('utf-8')
    nonce_base64 = b64encode(nonce).decode('utf-8')
    tag_base64 = b64encode(tag).decode('utf-8')

    return mot_de_passe_chiffre_base64, nonce_base64, tag_base64

def dechiffre_mot_de_passe(mot_de_passe_chiffre_base64, nonce_base64, tag_base64, cle_secrete):
    # Décodage des données
    mot_de_passe_chiffre = b64decode(mot_de_passe_chiffre_base64)
    nonce = b64decode(nonce_base64)
    tag = b64decode(tag_base64)

    # Déchiffrement du mot de passe
    cle_hash = hashlib.sha256(cle_secrete.encode()).digest()
    cipher = AES.new(cle_hash, AES.MODE_EAX, nonce=nonce)
    mot_de_passe_sale = cipher.decrypt_and_verify(mot_de_passe_chiffre, tag)
    sel = mot_de_passe_sale[:16]
    mot_de_passe = mot_de_passe_sale[16:].decode()

    return mot_de_passe

def enregistrer_utilisateur(conn, nom_utilisateur, mot_de_passe, cle_secrete):
    # Vérification si le nom d'utilisateur est déjà utilisé
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = ?", (nom_utilisateur,))
    result = cursor.fetchone()

    if result is not None:
        show_message_box("Information", f"Le nom d'utilisateur {nom_utilisateur} est déjà utilisé.")
        return

    # Vérification du mot de passe
    if len(mot_de_passe) < 8:
        show_message_box("Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
        return

    if not re.search("[A-Z]", mot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins une lettre majuscule.")
        return

    if not re.search("[a-z]", mot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins une lettre minuscule.")
        return

    if not re.search("[!@#$%^&*()_+.]", mot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins un caractère spécial.")
        return

    # Vérification de la key
    if len(cle_secrete) < 8:
        show_message_box("Erreur", "La clé doit contenir au moins 8 caractères.")
        return

    if not re.search("[A-Z]", cle_secrete):
        show_message_box("Erreur", "La clé doit contenir au moins une lettre majuscule.")
        return

    if not re.search("[a-z]", cle_secrete):
        show_message_box("Erreur", "La clé doit contenir au moins une lettre minuscule.")
        return

    if not re.search("[!@#$%^&*()_+.]", cle_secrete):
        show_message_box("Erreur", "La clé doit contenir au moins un caractère spécial.")
        return

    if cle_secrete != mot_de_passe:
        pass
    else:
        show_message_box("Erreur", "La clé doit être différente du mot de passe.")
        return

    # Chiffrement du mot de passe
    mot_de_passe_chiffre_base64, nonce_base64, tag_base64 = chiffre_mot_de_passe(mot_de_passe, cle_secrete)

    # Insertion de l'utilisateur dans la table
    cursor.execute("INSERT INTO utilisateurs VALUES (?, ?, ?, ?)",
                   (nom_utilisateur, mot_de_passe_chiffre_base64, nonce_base64, tag_base64))
    conn.commit()

    # Vérification de l'enregistrement de l'utilisateur
    cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = ?", (nom_utilisateur,))
    result = cursor.fetchone()

    # Assertions pour les tests
    assert result is not None  # Vérifie si l'enregistrement existe
    assert result[0] == nom_utilisateur  # Vérifie le nom de l'utilisateur
    assert result[1] == mot_de_passe_chiffre_base64  # Vérifie le mot de passe chiffré
    assert result[2] == nonce_base64  # Vérifie le nonce
    assert result[3] == tag_base64  # Vérifie le tag

def verifier_identifiant(conn, nom_utilisateur, mot_de_passe, cle_secrete):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur=?", (nom_utilisateur,))
    utilisateur = cursor.fetchone()

    try:
        mot_de_passe_enregistre = dechiffre_mot_de_passe(utilisateur[1], utilisateur[2], utilisateur[3], cle_secrete)
        if mot_de_passe == mot_de_passe_enregistre:
            return True
        else:
            raise ValueError("Mot de passe ou clé incorrect")
    except ValueError as e:
        show_message_box("Erreur", "Mot de passe ou clé incorrect")
        return False

def modifier_user(conn, nom_utilisateur, mot_de_passe, cle_secrete, newmot_de_passe):
    cursor = conn.cursor()

    #Verification des identifiants
    verifier_identifiant(conn,nom_utilisateur,mot_de_passe,cle_secrete)

    # Vérification du nouveau mot de passe
    if len(newmot_de_passe) < 8:
        show_message_box("Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
        return

    if not re.search("[A-Z]", newmot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins une lettre majuscule.")
        return

    if not re.search("[a-z]", newmot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins une lettre minuscule.")
        return

    if not re.search("[!@#$%^&*()_+.]", newmot_de_passe):
        show_message_box("Erreur", "Le mot de passe doit contenir au moins un caractère spécial.")
        return

    if cle_secrete != newmot_de_passe:
        pass
    else:
        show_message_box("Erreur", "La clé doit être différente du mot de passe.")
        return

    if mot_de_passe != newmot_de_passe:
        pass
    else:
        show_message_box("Erreur", "Le nouveau mot de passe doit être différent de l'ancien.")
        return

    # Chiffrement du mot de passe
    mot_de_passe_chiffre_base64, nonce_base64, tag_base64 = chiffre_mot_de_passe(newmot_de_passe, cle_secrete)

    # Modification de l'utilisateur dans la table
    cursor.execute("UPDATE utilisateurs SET mot_de_passe_chiffre = ?, nonce = ?, tag = ? WHERE nom_utilisateur = ?",
                   (mot_de_passe_chiffre_base64, nonce_base64, tag_base64,nom_utilisateur))
    conn.commit()

    # Vérification de la modification de l'utilisateur
    cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur = ?", (nom_utilisateur,))
    result = cursor.fetchone()

    # Assertions pour les tests
    assert result is not None  # Vérifie si l'enregistrement existe
    assert result[0] == nom_utilisateur  # Vérifie le nom de l'utilisateur
    assert result[1] == mot_de_passe_chiffre_base64  # Vérifie le mot de passe chiffré
    assert result[2] == nonce_base64  # Vérifie le nonce
    assert result[3] == tag_base64  # Vérifie le tag

def dechiffre_sans_integr(mot_de_passe_chiffre_base64, nonce_base64, cle_secrete):
    # Décodage des données
    mot_de_passe_chiffre = b64decode(mot_de_passe_chiffre_base64)
    nonce = b64decode(nonce_base64)

    # Déchiffrement du mot de passe
    cle_hash = hashlib.sha256(cle_secrete.encode()).digest()
    cipher = AES.new(cle_hash, AES.MODE_EAX, nonce=nonce)
    mot_de_passe_sale = cipher.decrypt(mot_de_passe_chiffre)
    sel = mot_de_passe_sale[:16]
    data = mot_de_passe_sale[16:].decode()

    return data

def add_mdp(nom_utilisateur, platform, identif, mot_de_passe, note, cle_secrete):
    # Vérification si l'user n'a pas déja rentré un mdp pour la même platforme avec le même pseudo
    conn = sqlite3.connect("utilisateurs.db")
    cursor = conn.cursor()

    #Vérification des inputs
    if platform == "" :
        show_message_box("Erreur", "Pas de plateforme renseignée ")

    if identif == "" :
        show_message_box("Erreur", "Pas d'identifiant renseigné")

    if mot_de_passe == "" :
        show_message_box("Erreur", "Pas de mot de passe renseigné")

    # Vérifications dans la bdd
    # Récupération des nonces à partir de la base de données
    cursor.execute("SELECT nonce_pseudo, nonce_platf, Plateforme, pseudo FROM mdp WHERE Nom_utilisateur = ?",
                   (nom_utilisateur,))
    nonces = cursor.fetchall()

    for row in nonces:
        nonce_pseudo = row[0]
        nonce_plat = row[1]
        plateformechif = row[2]
        pseudochif = row[3]

        # Vérification en déchiffrant les données et en comparant avec les valeurs fournies
        decrypted_platform = dechiffre_sans_integr(plateformechif, nonce_plat, cle_secrete)
        decrypted_pseudo = dechiffre_sans_integr(pseudochif, nonce_pseudo, cle_secrete)

        if decrypted_platform == platform and decrypted_pseudo == identif:
            show_message_box("Erreur", f"Vous avez déjà renseigné un mot de passe pour {identif} sur {platform}.")
            return

    # Chiffrement du mot de passe
    mot_de_passe_chiffre_base64, nonce_mdp_base64, pop= chiffre_mot_de_passe(mot_de_passe, cle_secrete)
    # Chiffrement des datas
    platform_chiffre64, nonce_plat_base64, _ = chiffre_mot_de_passe(platform, cle_secrete)
    pseudo_chiffre64, nonce_pseudo_base64, _ = chiffre_mot_de_passe(identif, cle_secrete)
    note_chiffre64, nonce_note_base64, _ = chiffre_mot_de_passe(note, cle_secrete)

    # Insertion des datas dans la table
    cursor.execute("INSERT INTO mdp VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (nom_utilisateur, platform_chiffre64, pseudo_chiffre64, mot_de_passe_chiffre_base64, nonce_mdp_base64, nonce_pseudo_base64, nonce_plat_base64, note_chiffre64, nonce_note_base64))
    conn.commit()

    # Vérification de l'enregistrement de l'utilisateur
    cursor.execute("SELECT * FROM mdp WHERE Nom_utilisateur = ? AND pseudo = ? AND Plateforme = ?", (nom_utilisateur,pseudo_chiffre64,platform_chiffre64))
    result = cursor.fetchone()

    # Assertions pour les tests
    assert result is not None  # Vérifie si l'enregistrement existe
    assert result[0] == nom_utilisateur
    assert result[1] == platform_chiffre64
    assert result[2] == pseudo_chiffre64
    assert result[3] == mot_de_passe_chiffre_base64
    assert result[4] == nonce_mdp_base64
    assert result[5] == nonce_pseudo_base64
    assert result[6] == nonce_plat_base64
    assert result[7] == note_chiffre64
    assert result[8] == nonce_note_base64
