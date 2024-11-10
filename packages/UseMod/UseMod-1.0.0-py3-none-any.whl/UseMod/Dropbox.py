import dropbox
import requests
import clipboard
import customtkinter

import requests

class NewToken:
    def __init__(self):
        """
        Exécutez cette classe pour obtenir un nouveau token non expiré.
        Exécutez en premier l'aide pour obtenir le refresh token.
        """
        pass

    def helps(self):
        """
        À exécuter une seule fois pour obtenir le refresh token.
        """
        def ok2():
            client_id = Entry1.get()  # Remplacez par votre client ID
            client_secret = Entry2.get()  # Remplacez par votre client secret
            code = Entry3.get()  # Remplacez par le code d'autorisation reçu de Dropbox
            ##redirect_uri = 'http://localhost'  # URL de redirection utilisée

            token_url = "https://api.dropbox.com/oauth2/token"
            data = {
                "code": code,
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret
            ##    "redirect_uri": redirect_uri
            }

            response = requests.post(token_url, data=data)
            tokens = response.json()

            if 'refresh_token' in tokens:
                textbox3.insert("1.0", f"Access token : {tokens['access_token']}\n")
                textbox3.insert("1.0", f"Refresh token : {tokens['refresh_token']}\n")
            else:
                textbox3.insert("1.0", f"Erreur : {tokens}\n")

        def ok():
            textbox2.insert("1.0", "Visitez cette URL : \n")
            textbox2.insert("1.0", f"https://www.dropbox.com/oauth2/authorize?client_id={Entry1.get()}&response_type=code&token_access_type=offline\n")
            textbox2.insert("1.0", f"Copier dans le presse papier\n")
            clipboard.copy(f"https://www.dropbox.com/oauth2/authorize?client_id={Entry1.get()}&response_type=code&token_access_type=offline")
        app = customtkinter.CTk()
        app.title("New token")
        app.resizable(False, False)
        textbox = customtkinter.CTkTextbox(app, font= ("Calibri", 18, "bold"), width = 400, height = 200)
        textbox.grid(column = 0, row =0, columnspan = 2, pady = 5, padx = 5, rowspan = 2)

        textbox.insert("1.0", "Suiver ces étape ci-dessu :\n")
        textbox.insert("1.0", "Accédez à la Console des applications Dropbox\n")
        textbox.insert("1.0", "Créez une application\n")
        textbox.insert("1.0", "Prenez l'App Key/ l'App Secret\n")
        textbox.insert("1.0", "Metter les ici :\n")
        Entry1 = customtkinter.CTkEntry(app, placeholder_text="App key", font= ("Calibri", 15, "bold"))
        Entry1.grid(column = 0, row =2, pady = 5, padx = 5)
        Entry2 = customtkinter.CTkEntry(app, placeholder_text="App Secret", font= ("Calibri", 15, "bold"))
        Entry2.grid(column = 1, row =2, pady = 5, padx = 5)
        BTNOK = customtkinter.CTkButton(app, text = "OK", font= ("Calibri", 15, "bold"), command = ok)
        BTNOK.grid(column = 0, row =3, pady = 5, padx = 5)
        textbox2 = customtkinter.CTkTextbox(app, font= ("Calibri", 18, "bold"), width = 400, height = 200)
        textbox2.grid(column = 0, row =4, columnspan = 2, pady = 5, padx = 5)

        Entry3 = customtkinter.CTkEntry(app, placeholder_text="code d'accès", font= ("Calibri", 15, "bold"))
        Entry3.grid(column = 3, row =0, pady = 5, padx = 5)
        BTNOK2 = customtkinter.CTkButton(app, text = "OK", font= ("Calibri", 15, "bold"), command = ok2)
        BTNOK2.grid(column = 4, row =0, pady = 5, padx = 5)

        textbox3 = customtkinter.CTkTextbox(app, font= ("Calibri", 18, "bold"), width = 400, height = 200)
        textbox3.grid(column = 3, row =1, pady = 5, padx = 5, columnspan = 2)
        app.mainloop()
    def AutomateTOKEN(self, refresh_token, APP_KEY, APP_SECRET):
        """
        Pour obtenir un nouveau token a chaque nouveau lancement de l'app

        :param refresh_token: Le refresh token obtenus avec le .helps()
        :param APP_KEY: L'app key de votre app dropbox
        :param APP_SECRET: L'app secret de votre app

        :form :
            variable = NewToken()
            TOKEN = variable.AutomateTOKEN(refresh_token, APP_KEY, APP_SECRET)

        et puis votre token est dans TOKEN
        """
        self.refresh_token = refresh_token
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        def obtenir_nouveau_jeton():
            # Envoi d'une requête pour obtenir un nouveau jeton d'accès
            response = requests.post(
                "https://api.dropboxapi.com/oauth2/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                },
                auth=(self.APP_KEY, self.APP_SECRET)
            )

            # Vérification de la réponse
            if response.status_code == 200:
                data = response.json()
                new_access_token = data.get("access_token")  # Nouveau jeton d'accès
                new_refresh_token = data.get("refresh_token")  # Nouveau jeton d'actualisation (si fourni)

                # Afficher les jetons
                print("Nouveau jeton d'accès :", new_access_token)
                print("Nouveau jeton d'actualisation :", new_refresh_token)

                return new_access_token, new_refresh_token
            else:
                print("Erreur :", response.json())
                return None, None
        access_token, refresh_token = obtenir_nouveau_jeton()
        return access_token
try :
    class Dropbox:
        def __init__(self, token):
            """
            Initialise une instance de la classe DropboxAccès.

            :param token: ton token obtenu depuis l'app Dropbox ou via la commande newToken
            """
            self.token = token
            self.dbx = dropbox.Dropbox(token)

        def new_file(self, file_content=None, dropbox_path=None):
            """
            Crée un nouveau fichier sur Dropbox.

            :param file_content: Le contenu du fichier
            :param dropbox_path: Le chemin vers le nouveau fichier Dropbox "/"+"nom_du_fichier"
            """
            try:
                if dropbox_path is None:
                    self.dbx.files_upload(file_content.encode('utf-8'), "New_File.txt")
                elif file_content is None:
                    self.dbx.files_upload("", dropbox_path)
                elif file_content and dropbox_path is None:
                    self.dbx.files_upload("", "New_File.txt")
                else:
                    self.dbx.files_upload(file_content.encode('utf-8'), dropbox_path)

            except dropbox.exceptions.ApiError as e:
                # Vérifie si l'erreur est due à un fichier déjà existant
                if e.error.is_conflict() and e.error.get_path().is_conflict() == dropbox_path:
                    print(f"Le fichier existe déjà : {dropbox_path}")
                else:
                    print(f"Erreur lors de la création du fichier : {e}")

        def new_folder(self, dropbox_path=None):
            """
            Crée un nouveau dossier sur Dropbox.

            :param dropbox_path: Le chemin vers le nouveau dossier Dropbox "/"+"nom_du_dossier"
            """
            try:
                if dropbox_path is None:
                    self.dbx.files_create_folder("New_Folder")
                else:
                    self.dbx.files_create_folder(dropbox_path)
            except dropbox.exceptions.ApiError as e:
                # Vérifie si l'erreur est due à un dossier déjà existant
                if e.error.is_conflict() and e.error.get_path().is_conflict() == dropbox_path:
                    print(f"Le dossier existe déjà : {dropbox_path}")
                else:
                    print(f"Erreur lors de la création du dossier : {e}")
        def new_content(self):
            """
            Supprime le contenu existant et crée un nouveau fichier avec le contenu donné.

            :param file_content: Contenu du fichier à envoyer
            :param dropbox_path: Chemin Dropbox où le fichier sera stocké
            """
            class File:
                def __init__(self, dbx):
                    self.dbx = dbx

                def withfile(self, path, dropbox_path):
                    self.dbx.files_delete(dropbox_path)
                    with open(path, 'rb') as f:
                        self.dbx.files_upload(f.read(), dropbox_path)
                def withvar(self, file_content, dropbox_path):
                    self.dbx.files_delete(dropbox_path)
                    self.dbx.files_upload(file_content, dropbox_path)

        def del_content(self, dropbox_path):
            self.dbx.files_delete(dropbox_path)
        def download(self):
            """
            Crée une instance de la sous-classe File pour gérer les téléchargements.
            """
            class File:
                def __init__(self, dbx):
                    self.dbx = dbx

                def infile(self, path, dropbox_path):
                    self.dbx.files_get_metadata(dropbox_path)
                    with open(path, 'wb') as f:
                        metadata, res = self.dbx.files_download(dropbox_path)
                        f.write(res.content)

                def invar(self, dropbox_path):
                    metadata, res = self.dbx.files_download(dropbox_path)
                    return res.content  # Retourne le contenu du fichier sous forme de variable

            return File(self.dbx)
except dropbox.exceptions.ApiError as e:
            if isinstance(e.error, dropbox.files.DownloadError):
                if e.error.is_path() and e.error.get_path().is_not_found():
                    print(f'Erreur : le fichier {dropbox_path} n\'existe pas sur Dropbox.')
                else:
                    print(f'Erreur lors du téléchargement : {e}')
            else:
                print(f'Erreur lors de l\'accès au fichier : {e}')
# Exemple d'utilisation
if __name__ == "__main__":
    test = NewToken()
    access_token = test.AutomateTOKEN("i2ppcPBlsTUAAAAAAAAAAf42pyeCx8Wrp7T0vdL2Dse-yD9IJ3kQEI3YqwmEF8rz", "a62jwa804kvkrvz", "1remb45pkpxu35p")  # Appelle la méthode pour obtenir le refresh token
    print("Access Token obtenu:", access_token)
    APP = DropboxA(access_token)
    print(APP.download().invar("/liste.txt"))  # Appel correct pour télécharger le contenu
