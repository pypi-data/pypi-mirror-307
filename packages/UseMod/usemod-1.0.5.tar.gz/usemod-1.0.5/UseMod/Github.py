import requests
import base64
import json
import UseMod as um

class Github:
    def __init__(self, token, Owner, Repo):
        self.token = token
        self.Owner = Owner
        self.Repo = Repo

    def new_file(self, file_name, file_content):
        contenu_base64 = base64.b64encode(file_content.encode('utf-8')).decode()
        url = f'https://api.github.com/repos/{self.Repo}/{self.Owner}/contents/{file_name}'
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {
            'message': "Ajout de un nouveau fichier",
            'content': file_content
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 201:
            print('Fichier créé avec succès !')
            return("True")
        else:
            print(f"Erreur : {response.status_code}, {response.text}")
            return("False")
    def new_file_content(self, file_name, file_content):
        url_get = f'https://api.github.com/repos/{self.Repo}/{self.Owner}/contents/{file_name}'
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url_get, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            sha = file_data['sha']  # On récupère le SHA pour la modification

            # Encodage du nouveau contenu en base64
            encoded_content = base64.b64encode(file_content.encode('utf-8')).decode()

            # URL pour mettre à jour le fichier
            url_put = f'https://api.github.com/repos/{self.Repo}/{self.Owner}/contents/{file_name}'

            data = {
                'message': "Ajout de un nouveau fichier",
                'content': encoded_content,
                'sha': sha  # On inclut le SHA pour identifier le fichier à modifier
            }

            # Requête pour mettre à jour le fichier
            response = requests.put(url_put, json=data, headers=headers)

            if response.status_code == 200:
                print('Fichier modifié avec succès !')
            else:
                print(f"Erreur : {response.status_code}, {response.text}")
        else:
            print(f"Erreur lors de la récupération du fichier : {response.status_code}, {response.text}")
test = Github()
tde
