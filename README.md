
# Projet Blockchain - Sécurisation de la Traçabilité des Produits Pharmaceutiques - Guide Utilisation

## Sommaire
1. [Prérequis](#prérequis)
2. [Serveur Blockchain](#serveur-blockchain)
    1. [Lancement du serveur Blockchain](#lancement-du-serveur-blockchain)
    2. [Afficher la blockchain](#afficher-la-blockchain)
    3. [Ajouter une nouvelle transaction](#ajouter-manuellement-une-nouvelle-transaction)
    4. [Afficher les transactions en attente](#afficher-les-transactions-en-attente)
    5. [Ajouter plusieurs transactions](#ajouter-plusieurs-transactions)
3. [Serveur Web](#serveur-web)
    1. [Installation](#installation)
    2. [Configurer la base de données](#configurer-la-base-de-données)
    3. [Démarrer le serveur](#démarrer-le-serveur)
    4. [Fichiers importants](#fichiers-importants)

## Prérequis
* VM Linux (Debian, Ubuntu, Kali, etc.)
* Base de données SQL (MySQL, MariaDB, etc.)
* Python3
* Code `BlockchainServer` & `Web`
* NodeJS

### Librairies Python à installer :
* cryptography

## Serveur Blockchain

Dans un premier temps, vous devez récupérer le dossier complet du code `BlockchainServer`.

### Lancement du serveur Blockchain

Pour le premier serveur, vous devez lancer la commande suivante dans la racine du dossier `Projet_Blockchain` (cette commande va lancer le serveur qui initialisera le premier nœud de la blockchain) : 

```bash
python3 blockchainServer.py --port 4000 --http_port 8080 --certificate ./cert/laboratoire/laboratoirecert.pem --private_key ./cert/laboratoire/laboratoirekey.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_server1.json --log_path ./logs/log_serv1.log --genesis
```

Au premier lancement, vous devez obtenir un retour de ce type : 

```bash
2024-05-26 12:20:35.421001 Server is running in the background...
2024-05-26 12:20:36.864677 New blockchain successfully created.
2024-05-26 12:20:36.864677 Blockchain saved.
2024-05-26 12:20:36.864677 Web Server Server started. Listening on port 8080...
2024-05-26 12:20:36.864677 Blockchain Server started. Listening on 127.0.0.1:4000
2024-05-26 12:20:36.864677 Starting delay mining thread.
2024-05-26 12:20:36.864677 Mining scheduler thread started.
```

Pour le second serveur, vous devez lancer la commande suivante :

```bash
python3 blockchainServer.py --port <port_blockchain> --http_port <port_http> --certificate ./cert/pharmacies/pharmaciecert.pem --private_key ./cert/pharmacies/pharmaciekey.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_server2.json --log_path ./logs/_serv2.log --remote_nodes "<ip_serv_distant>:<port_serv_distant>"
```

*Si vous lancez les deux serveurs en local, remplacez `<port_blockchain>` par 4001, `<port_http>` par 8081 et `<ip_serv_distant>:<port_serv_distant>` par "127.0.0.1:4000".*

*Sinon, remplacez `<port_blockchain>` par 4000, `<port_http>` par 8080 et `<ip_serv_distant>:<port_serv_distant>` par "ip_serveur_distant:4000".*

Vous devez obtenir un retour du type : 

```bash
2024-05-26 12:34:30.786641 Server is running in the background...
2024-05-26 12:34:31.413683 Blockchain successfully loaded from ('127.0.0.1', 4000)
2024-05-26 12:34:31.413683 Blockchain saved.
2024-05-26 12:34:31.413683 Web Server Server started. Listening on port 8081...
2024-05-26 12:34:31.413683 Starting delay mining thread.
2024-05-26 12:34:31.413683 Mining scheduler thread started.
2024-05-26 12:34:31.413683 Blockchain Server started. Listening on 127.0.0.1:4001
```


### Exemple de commande pour lancer plusieurs serveurs
```bash
python3 blockchainServer.py --port 4000 --http_port 8080 --certificate ./certs/Laboratoire/Laboratoire1/Laboratoire1cert.pem --private_key ./certs/Laboratoire/Laboratoire1/Laboratoire1key.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_laboratoire1.json --log_path ./logs/log_laboratoire1.log --genesis

python3 blockchainServer.py --port 4001 --http_port 8081 --certificate ./certs/Pharmacie/Pharmacie1/Pharmacie1cert.pem --private_key ./certs/Pharmacie/Pharmacie1/Pharmacie1key.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_pharmacie1.json --log_path ./logs/log_pharmacie1.log --remote_nodes "127.0.0.1:4000"

python3 blockchainServer.py --port 4002 --http_port 8082 --certificate ./certs/Transporteur/Transporteur1/Transporteur1cert.pem --private_key ./certs/Transporteur/Transporteur1/Transporteur1key.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_transporteur1.json --log_path ./logs/log_transporteur1.log --remote_nodes "127.0.0.1:4000"

python3 blockchainServer.py --port 4003 --http_port 8083 --certificate ./certs/Transporteur/Transporteur2/Transporteur2cert.pem --private_key ./certs/Transporteur/Transporteur2/Transporteur2key.pem --key_passphrase "Azerty123*" --blockchain_path ./blockchains/blockchain_transporteur2.json --log_path ./logs/log_transporteur2.log --remote_nodes "127.0.0.1:4000"

```
### Afficher la blockchain

Pour afficher la blockchain, tapez la commande suivante :

```bash
cmd: blockchain
Blockchain:

        -------------------------------------------------- Block 0 --------------------------------------------------
        HEADER: ID: 0 | Version: 0.5 | Previous Hash: 0000000000000000000000000000000000000000000000000000000000000000 | Time: 2024-05-26 12:20:35.421001 | Difficulty: 5 | Nonce: 1355089
        TRANSACTIONS:

        TOTAL TRANSACTIONS: 0
        HASH: 00000a87ec6006b47833f635f1605dce42e043dd1a198cde4fa4c6deacc95b4c
```

### Ajouter manuellement une nouvelle transaction

Pour ajouter manuellement une nouvelle transaction, tapez la commande suivante : 

```bash
cmd: new trans
[ 1: 'Pharmacie', 2: 'Transporteur', 3: 'Laboratoire', 4: 'Usine' ]: 1
product_sn : 12
product_id : 12345
2024-05-26 12:30:50.405393 new transaction Laboratoire=>Pharmacie [12345,12] added to the pool
```

### Afficher les transactions en attente

Pour afficher les transactions en attente, tapez la commande suivante :

```bash 
cmd: pool

                -------------------------------------------------- TRANSACTION None --------------------------------------------------
                ID: None | Time: 2024-05-26 12:30:50.405393 | Source ID: Laboratoire |
                Product ID: 12345 | Serial Number: 12 |
                Destination ID: Pharmacie | Signature: 30450220736b4b0549d808969fa046b8f131b5db714d5b80b650d9e12e9043daeb2464e4022100d655e1bd39e27085626e4cfd4ec3eb7de46290b4686f992fd57dd9314aa2091a |
                Hash: None |
```

### Ajouter plusieurs transactions

Pour ajouter plusieurs transactions, tapez la commande suivante :

```bash
cmd: new rand trans    
Number of transactions: 4
2024-05-26 12:38:43.890732 new transaction Pharmacie=>Laboratoire [10,62648] added to the pool
2024-05-26 12:38:43.890732 Trasacion succesfully sent to ('127.0.0.1', 4000)
2024-05-26 12:38:43.890732 new transaction Pharmacie=>Usine [7,75027] added to the pool
2024-05-26 12:38:43.906341 Trasacion succesfully sent to ('127.0.0.1', 4000)
2024-05-26 12:38:43.906341 new transaction Pharmacie=>Laboratoire [7,19506] added to the pool
2024-05-26 12:38:43.906341 Trasacion succesfully sent to ('127.0.0.1', 4000)
2024-05-26 12:38:43.906341 new transaction Pharmacie=>Usine [2,21252] added to the pool
2024-05-26 12:38:43.906341 Trasacion succesfully sent to ('127.0.0.1', 4000)
```

## Serveur Web

Ce projet utilise Node.js avec Express, EJS, MySQL et Axios. Il s'agit d'une interface web visant à sécuriser la traçabilité des produits pharmaceutiques à l'aide de la blockchain.

## Installation

### 1. Cloner le projet

Clonez le repository sur votre machine locale :

```bash
cd NODEJS_PROJET_BLOCKCHAIN
```

### 2. Installer les dépendances

Dans le répertoire du projet, installez les dépendances nécessaires via npm :

```bash
npm install
```

Cela va installer les modules suivants :

- `express` : Framework web pour Node.js.
- `ejs` : Moteur de templates pour générer du HTML dynamique.
- `mysql2` : Bibliothèque pour interagir avec MySQL.
- `axios` : Bibliothèque pour effectuer des requêtes HTTP.

### 3. Configurer la base de données

Créez une base de données MySQL nommée `pharmaceutique`. Vous pouvez utiliser le script SQL suivant pour créer la base et ses tables :

```sql
CREATE DATABASE pharmaceutique;
USE pharmaceutique;

-- Ajoutez ici vos tables et données nécessaires
```

Dans le fichier `./config/database.js`, vous trouverez la configuration de la connexion à la base de données. Assurez-vous que les informations de connexion sont correctes pour votre environnement :

```js
const mysql = require('mysql2');

const db = mysql.createConnection({
  host: '127.0.0.1',      // Adresse du serveur de base de données
  user: 'ddb_user',       // Utilisateur MySQL
  password: 'Azerty123*', // Mot de passe MySQL
  database: 'pharmaceutique', // Nom de la base de données
});

db.connect((err) => {
  if (err) {
    console.error('Erreur de connexion à la base de données :', err);
    process.exit(1);
  }
  console.log('Connecté à la base de données MariaDB.');
});

module.exports = db;
```

### 4. Démarrer le serveur

Une fois tout configuré, vous pouvez démarrer le serveur avec la commande suivante :

```bash
node server.js
```

Cela va démarrer l'application sur le port défini (par défaut 3000). Vous pouvez accéder à l'application en ouvrant votre navigateur et en naviguant vers `http://localhost:3000`.

### 5. Fichiers importants

- `server.js` : Point d'entrée du serveur. Il configure et lance l'application Express.
- `./config/database.js` : Contient la configuration de la connexion à la base de données MySQL.
- `./routes` : Contient les routes définies pour l'application.
- `./views` : Contient les fichiers EJS pour le rendu dynamique des pages.
- `./public` : Contient les fichiers statiques (CSS, JS, images).

Example of the website : 
# Page de connexion
![Image1](https://github.com/user-attachments/assets/0ddbc08d-7762-4e85-9605-2096e7280b46)

# Listing des acteurs
![Image2](https://github.com/user-attachments/assets/0699c8c6-82bc-422e-8304-d873e4dbc0f9)

# Effectuer une transaction
![Image3](https://github.com/user-attachments/assets/981cbb07-e270-4496-bc18-423a4bfacd11)

# Affichage des transactions
![Image4](https://github.com/user-attachments/assets/3bf4181f-b33c-4db9-a37f-89fcd2b442ba)
