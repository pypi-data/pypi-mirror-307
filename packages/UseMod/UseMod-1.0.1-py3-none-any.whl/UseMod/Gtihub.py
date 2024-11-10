import requests
import base64
import json
from tkinter import messagebox

class Github:
    def __init__(self, token, Owner, Repo):
        self.token = token
        self.Owner = Owner
        self.Repo = Repo
    def new_file_content(self, file_name, file_content):
        # URL pour créer le fichier dans le dépôt GitHub
        url = f'https://api.github.com/repos/{self.Owner}/{self.Repo}/contents/{file_name}'
        headers = {'Authorization': f'token {self.token}'}

        # Encodage du contenu du fichier en base64, requis par l'API GitHub
        encoded_content = base64.b64encode(file_content).decode('utf-8')  # Pas besoin de .encode('utf-8') ici
        data = {
            "message": "Création d'un nouveau fichier",
            "content": encoded_content,
        }

        # Envoi de la requête pour créer le fichier
        response = requests.put(url, headers=headers, data=json.dumps(data))

        if response.status_code == 201:
            print(f"Fichier '{file_name}' créé avec succès dans le dépôt GitHub.")
        elif response.status_code == 422:
            print(f"Le fichier '{file_name}' existe déjà dans le dépôt.")
        else:
            print(f"Erreur lors de la création du fichier : {response.json()}")