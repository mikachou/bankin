# Bankin

J'ai conçu ces scripts afin d'agréger les données envoyées par Bankin dans mes mails Gmail et de construire un dataset en CSV.
Il peut y avoir dans le CSV en résultat de nombreux champs non-renseignés (parfois des données sont absentes des mails de Bankin), il faudra donc éventuellement imputer la donnée manquante en post-traitement.

## Pré-requis

### Gmail

Le script fonctionne avec Gmail. Il faut crééer un mot de passe d'application depuis Gmail. Voir :
[https://support.google.com/mail/answer/185833?hl=en](https://support.google.com/mail/answer/185833?hl=en)

### pre-requis Python

* pyenv : [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)
* pyenv-virtualenv : [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)

## Installation

Cloner le dépôt.

```
$ git clone https://github.com/mikachou/bankin
```

Entrer dans le dossier
```
$ cd bankin
```

Installer la version de Python :

```
$ pyenv install
```

Créer un environnement virtuel pour le projet

```
$ pyenv virtualenv bankin
```

Entrer dans l'environnement virtuel

```
$ pyenv activate bankin
```

Installer les paquets
```
$ pip install -r requirements.txt
```

copier `.env.dist` en `.env` et renseigner les champs EMAIL (avec l'adresse gmail) et PASSWORD (avec le mot de passe de l'application)

## Utilisation

Il faut lancer les scripts depuis l'environnement virtuel.

Pour récupérer l'ensemble des mails de bankin contenant les soldes de comptes dans le dossier `mails/` :
```
$ python fetch_emails.py
```

Pour récupérer l'ensemble des scripts à partir d'une certaine date :
```
$ python fetch_emails.py --after=2024/04/29 # récupère tous les mails à partir du 29 avril 2024
```

Une fois les mails récupérés il créer le dataset :
```
$ python create_dataset.py 
```

Le dataset est créé dans le dossier `export/` du projet avec le nom `export.csv`
