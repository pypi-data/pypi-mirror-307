# UseMod

UseMod est un simple module pour python qui permet plus de simpliciter dans des module ou plus de modernité

## Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Utilisation](#utilisation)
4. [Fonctionnalités](#fonctionnalités)
5. [Contribuer](#contribuer)
6. [Auteurs](#auteurs)
7. [Licence](#licence)

## Introduction

Dans use Module vous pourez y trouver :

- Un accès simple et rapide vers DropBox
- Un accès simple et rapide vers GitHub
- Un Showinfo plus modern

## Installation

Instructions pour installer et configurer le projet. Indiquez les prérequis et les étapes d'installation.

```bash
#executer la commende pip :
pip install UseMod
```
## Utilisation

1. [DropBox](#DropBox)
2. [GitHub](#installation)
3. [Showinfo](#Showinfo)

### DropBox

Importer le Module
````python
import UseMod
````
###
#### Token

````python
Token = UseMod.NewToken()
````

Le refresh Token
(non obligatoire)

````python
Token.helps() # Pour obtenir un refresh token
````
Nouveau Token a chaque lancement du projet python
````python
TOKEN = Token.AutomateTOKEN(Ton_refreshToken, Ton_AppKey, Ton_app secret
````
###

#### Fichier

````python
File = UseMod.Dropbox(ton_TOKEN)
````

Créer un nouveau fichier
````python
File.new_file(Contenu_du_fichier, accès_Dropbox_vers_le_fichier)
````

Créer un nouveau dossier
````python
File.new_folder(accès_Dropbox_vers_le_dossier) #
````

##### Créer un nouveau contenu de fichier

Depuis un fichier
````python
File.new_content().withfile(chemin_du_fichier, chemin_du_fichier_Dropbox)
````

Depuis une variable
````python
File.new_content().withvar(Contenu_du_fichier, chemin_du_fichier_Dropbox)
````

Suprimer un fichier/dossier

````python
File.del_content(chemin_du_fichier_Dropbox)
````

##### Obtenir le contenu d'un fichier

Dans un fichier
````python
File.download().infile(chemin_du_fichier, chemin_du_fichier_Dropbox)
````

Dans une variable
````python
Tavariable = File.download().invar(chemin_du_fichier_Dropbox)
````

### ShowInfo

Afficher une erreur
````python
UseMod.Message("error", Un_Nom, Un_message, un_Style : dark, light, ourien)
````

Afficher une info
````python
UseMod.Message("info", Un_Nom, Un_message, un_Style : dark, light, ourien)
````