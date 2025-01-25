#!/bin/bash

# Lancer chaque commande dans un onglet séparé avec Tilix
tilix -e "bash -c 'python3 blockchainServer.py --port 4000 --http_port 8080 --certificate ./certs/Laboratoire/Laboratoire1/Laboratoire1cert.pem --private_key ./certs/Laboratoire/Laboratoire1/Laboratoire1key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_laboratoire1.json --log_path ./logs/log_laboratoire1.log --genesis; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4001 --http_port 8081 --certificate ./certs/Laboratoire/Laboratoire2/Laboratoire2cert.pem --private_key ./certs/Laboratoire/Laboratoire2/Laboratoire2key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_laboratoire2.json --log_path ./logs/log_laboratoire2.log --remote_nodes \"127.0.0.1:4000\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4002 --http_port 8082 --certificate ./certs/Laboratoire/Laboratoire3/Laboratoire3cert.pem --private_key ./certs/Laboratoire/Laboratoire3/Laboratoire3key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_laboratoire3.json --log_path ./logs/log_laboratoire3.log --remote_nodes \"127.0.0.1:4001\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4003 --http_port 8083 --certificate ./certs/Pharmacie/Pharmacie1/Pharmacie1cert.pem --private_key ./certs/Pharmacie/Pharmacie1/Pharmacie1key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_pharmacie1.json --log_path ./logs/log_pharmacie1.log --remote_nodes \"127.0.0.1:4002\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4004 --http_port 8084 --certificate ./certs/Pharmacie/Pharmacie2/Pharmacie2cert.pem --private_key ./certs/Pharmacie/Pharmacie2/Pharmacie2key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_pharmacie2.json --log_path ./logs/log_pharmacie2.log --remote_nodes \"127.0.0.1:4003\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4005 --http_port 8085 --certificate ./certs/Pharmacie/Pharmacie3/Pharmacie3cert.pem --private_key ./certs/Pharmacie/Pharmacie3/Pharmacie3key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_pharmacie3.json --log_path ./logs/log_pharmacie3.log --remote_nodes \"127.0.0.1:4004\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4006 --http_port 8086 --certificate ./certs/Transporteur/Transporteur1/Transporteur1cert.pem --private_key ./certs/Transporteur/Transporteur1/Transporteur1key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_transporteur1.json --log_path ./logs/log_transporteur1.log --remote_nodes \"127.0.0.1:4005\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4007 --http_port 8087 --certificate ./certs/Transporteur/Transporteur2/Transporteur2cert.pem --private_key ./certs/Transporteur/Transporteur2/Transporteur2key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_transporteur2.json --log_path ./logs/log_transporteur2.log --remote_nodes \"127.0.0.1:4006\"; exec bash'" &
sleep 0.1

tilix -e "bash -c 'python3 blockchainServer.py --port 4008 --http_port 8088 --certificate ./certs/Transporteur/Transporteur3/Transporteur3cert.pem --private_key ./certs/Transporteur/Transporteur3/Transporteur3key.pem --key_passphrase \"Azerty123*\" --blockchain_path ./blockchains/blockchain_transporteur3.json --log_path ./logs/log_transporteur3.log --remote_nodes \"127.0.0.1:4007\"; exec bash'" &
