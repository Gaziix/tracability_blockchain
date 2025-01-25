import os
import socket
import threading
import time
import traceback
from blockchain import *  # Assuming this is a custom module you've provided
import json
import copy
import datetime
import random
from httpBlockchainServer import Httpd
import argparse
ERROR_CODES = {
    710: "Invalid signature"
}
class Server:
    def __init__(self, private_key_file_path, private_key_passphrase, certificate_file_path, log_file_path, blockchain_file_path, chest_value, remote_nodes = [], max_transactions = 10, listening_host='0.0.0.0', host='127.0.0.1', port=4000, http_port=8080):
        self.public_host = host
        self.listening_host = listening_host
        self.port = port
        self.remote_nodes = remote_nodes
        self.chest = chest_value

        self.private_key = Crypto.get_privatekey_from_file(private_key_file_path, private_key_passphrase) 
        self.certificate = Crypto.get_certificate_from_file(certificate_file_path)

        self.transaction_pool = []
        self.blockchain = None
        self.id = self.certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.max_transactions = max_transactions
        self.log_file_path = log_file_path
        self.blockchain_file_path = blockchain_file_path

        self.httpd = Httpd(self.broadcast_transaction,source_id=self.id,port=http_port, log_function=self.log,blockchain_file_path=blockchain_file_path, listening_host=self.listening_host)

    def start_server(self, genesis_node=False, blockchain_version='0.5'):
        self.log("Server is running in the background...")

        if genesis_node:
            if os.path.exists(self.blockchain_file_path):
                try:
                    # Open the file and load the blockchain data
                    with open(self.blockchain_file_path, 'r') as file:
                        self.blockchain = convert_to_blockchain(json.load(file))  # Directly load JSON from the file
                    self.log("Blockchain successfully loaded.")
                except Exception as e:
                    self.log(f"Error loading blockchain: {e}", error=e)
                    return  # Stop execution if loading fails
            else:
                # Create a new blockchain if it doesn't exist
                self.blockchain = Blockchain(blockchain_version, self.max_transactions)
                self.add_actor(self.id, self.certificate, self.chest)
                self.log('New blockchain successfully created.')
        else:
            self.init_node()
        # Save the blockchain after loading or creating it
        self.save_blockchain()
        self.start_background_processes()

    def run_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.listening_host, self.port))
        self.server_socket.listen()
        self.log(f"Blockchain Server started. Listening on {self.listening_host}:{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            # Create a new thread for each client and add it to the dictionary
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()    

    def init_node(self):
        try:
            # Initialize connections and synchronize blockchain
            initial_connection = self.remote_nodes[0]
            message = json.dumps({
                        "action": "init",
                        "metadata": {
                            "source_id": self.id,"timestamp": datetime.datetime.now().isoformat() 
                        },
                        "payload": {
                            "host": self.public_host,"port": self.port,"certificate": self.certificate.public_bytes(serialization.Encoding.PEM).decode(),"chest_value": self.chest
                        }
                    })
            response = self.send_data(message, *initial_connection)
            if response:
                if response["action"] == "init_response" and "nodes" in response["payload"]:
                    # Check if nodes are not None before iterating
                    nodes = response["payload"]["nodes"]
                    if nodes:  # Only proceed if nodes is not None
                        for node in nodes:
                            host = node["host"]
                            port = node["port"]
                            if [host, port] not in self.remote_nodes and port != self.port:
                                self.remote_nodes.append([host, port])
                                self.log(f"Node ({host}, {port}) added from init_response.")

            for server_ip, server_port in self.remote_nodes:
                if [server_ip, server_port] == initial_connection:
                    continue  # Skip the initial connection node
                
                # Prepare and send the initialization message
                message = json.dumps({
                    "action": "init",
                    "metadata": {
                        "source_id": self.id,
                        "timestamp": datetime.datetime.now().isoformat()
                    },
                    "payload": {
                        "host": self.public_host,
                        "port": self.port,
                        "certificate": self.certificate.public_bytes(serialization.Encoding.PEM).decode(),
                        "chest_value": self.chest
                    }
                })
                self.send_data(message, server_ip, server_port)
                # Attempt to load the blockchain from one of the remote servers
            self.load_blockchain_from_remote()

        except Exception as e:
            self.log(f"Error initializing network connections: {e}")
            exit("Could not initialize network connections")

    def load_blockchain_from_remote(self):
        for server_ip, server_port in self.remote_nodes:
            try:
                message = json.dumps({
                    "action": "get_blockchain",
                    "metadata": {
                        "source_id": self.id,
                        "timestamp": datetime.datetime.now().isoformat()
                    },
                    "payload": None
                })
                response = self.send_data(message, server_ip, server_port)
                if response:
                    if response["action"] == "get_blockchain_response" and "payload" in response:
                        blockchain_data = response["payload"]["blockchain"]
                        if blockchain_data:
                            self.blockchain = convert_to_blockchain(blockchain_data)
                            self.log(f"Blockchain successfully loaded from ('{server_ip}', {server_port})")
                            break
                        else:
                            self.log(f"No blockchain data found in the response from ('{server_ip}', {server_port})")
                    else:
                        self.log(f"Invalid response structure from ('{server_ip}', {server_port}'): {response}")
                else:
                    self.log(f"No response received from ('{server_ip}', {server_port})")
            except Exception as e:
                self.log(f"Failed to load blockchain from ('{server_ip}', {server_port}): {e}")

        if not self.blockchain:
            self.log("Could not get the blockchain")
            exit("Could not get the blockchain")

    def start_background_processes(self):
        self.httpd.blockchain_server = self
        threading.Thread(target=self.httpd.run_server, daemon=True).start()
        threading.Thread(target=self.run_server, daemon=True).start()
        self.cli()

    def cli(self):
        cmd=None
        while cmd != 'exit':
            cmd = input("cmd: ")
            self.log(f'Input : {cmd}',display=False)
            if cmd == "blockchain":
                print(self.blockchain)
            elif cmd == 'node':
                for i in self.remote_nodes:
                    print(i)
            elif cmd == "pool":
                for i in self.transaction_pool:
                    print(i)
            elif cmd == 'clean pool':
                id = input("transaction id (None for all)")
                if id != '':
                    del self.transaction_pool[id]
                else:
                    del self.transaction_pool[:]
            elif cmd == "cert":
                print(self.certificate)
            elif cmd == "new trans":
                print(" | ".join(f"[{i}] {actor}" 
                for i, actor in enumerate(
                    (a for a in self.blockchain.actors.keys() if a != self.id), start=1)))
                choice = int(input("Enter the number of your choice: "))
                product_id = int(input("Enter the product id (int): "))
                product_sn = int(input("Enter the product nerial number (int): "))
                chosen_actor = list(self.blockchain.actors.keys())[choice - 1]
                self.broadcast_transaction(chosen_actor,self.id,product_id,product_sn)
            elif cmd == "new rand trans":
                number_transactions = int(input("number of transactions : "))
                for i in range(0,number_transactions):
                    random_actor = random.choice([a for a in self.blockchain.actors.keys() if a != self.id])
                    random_product_id = random.randint(1,100)
                    random_product_sn = random.randint(100,1000)
                    self.broadcast_transaction(random_actor,self.id,random_product_id,random_product_sn)
            elif cmd == "next validatot":
                print(self.blockchain.select_validator())
            elif cmd == "actors":
                print(self.blockchain.actors)
        self.log("Stoping server ...")

    def add_actor(self, actor_id, actor_certificate, chest=1000, reputation = 100):
        self.blockchain.actors[actor_id] = actor_certificate, chest, reputation
        self.log(f"new actor added {actor_certificate, chest, reputation}")

    def process_data(self, addr, json_data):
        if json_data["action"] == "init":
            remote_node_host = json_data["payload"]["host"]
            remote_node_port = json_data["payload"]["port"]
            remote_node_id = json_data["metadata"]["source_id"]
            remote_node_certificate = x509.load_pem_x509_certificate(json_data["payload"]["certificate"].encode())
            remote_node_chest = json_data["payload"]["chest_value"]
            message= {
                "action": "init_response",
                "metadata": {
                    "source_id": self.id,
                    "timestamp": datetime.datetime.now().isoformat() 
                },
                "payload": {
                    "nodes": [{"host": item[0], "port": item[1]} for item in self.remote_nodes] if self.remote_nodes else None
                }
            }
            if [remote_node_host,remote_node_port] not in self.remote_nodes:
                self.remote_nodes.append([remote_node_host, remote_node_port])  # Always use list format
                self.log(f"New node [{remote_node_host},{remote_node_port}] added")
            
            
            self.add_actor(remote_node_id,remote_node_certificate)
            self.save_blockchain()
            return message

        elif json_data["action"] == "get_blockchain":  
            message = {
                "action": "get_blockchain_response",
                "metadata": {
                    "source_id": self.id,
                    "timestamp": datetime.datetime.now().isoformat() 
                },
                "payload": {
                    "blockchain": self.blockchain.to_dict()  # Add a key to wrap the blockchain data
                }
            }
            self.log(f"Blockchain sent to {addr}")
            return message

        elif json_data["action"] == "new_transaction":
            new_transaction = convert_to_blocktransaction(json_data["payload"]["new_transaction"])
            if not new_transaction.verify_sig(self.blockchain.actors[new_transaction.source_id][0].public_key()):
                message = {
                    "action": "error",
                    "metadata": {
                        "source_id": self.id,
                        "timestamp": datetime.datetime.now().isoformat() 
                    },
                    "payload": {
                        "response_to": "new_transaction", "code": 710, "message": "Invalid transaction signature",
                        "details": {
                            "transaction_id": new_transaction.id,
                            "source_id": new_transaction.source_id
                        }
                    }
                }
            else : 
                message = {
                    "action": "new_transaction_response",
                    "metadata": {
                        "source_id": self.id,
                        "timestamp": datetime.datetime.now().isoformat() 
                    },
                    "payload": {
                        "status": "accepted",
                        "reason": None
                    }
                }
                self.transaction_pool.append(new_transaction)
                self.log(f"new transaction added to the pool")
             
            if len(self.transaction_pool) >= self.max_transactions:
                threading.Thread(target=self.seal_curent_block).start()

            return message
        
        elif json_data["action"] == "new_block":
            if json_data["payload"]:
                if json_data["payload"]["new_block"]:
                    # Conversion du bloc reçu en objet Block
                    new_block = convert_to_block(json_data["payload"]["new_block"])

                    # Vérification de la validité du bloc
                    if new_block.is_valid(self.blockchain.actors):
                        # Ajouter le bloc à la chaîne si tout est valide
                        

                        

                        # Répondre avec un message de confirmation
                        message = {
                            "action": "new_block_response",
                            "metadata": {
                                "source_id": self.id,
                                "timestamp": datetime.datetime.now().isoformat()
                            },
                            "payload": {
                                "status": "accepted",
                                "block_id": new_block.header.id,
                                "message": "Block successfully added to the chain"
                            }
                        }
                        self.blockchain.chain.append(new_block)
                        self.log(f"New block {new_block.header.id} added to the blockchain.")
                        # Nettoyer la pool de transactions en enlevant celles déjà incluses dans ce bloc
                        self.clean_pool(new_block)
                        self.blockchain.reward_validator(new_block.validator_id)
                        self.save_blockchain()
                    else:
                        # Si le bloc est invalide, retour d'un message d'erreur
                        message = {
                            "action": "error",
                            "metadata": {
                                "source_id": self.id,
                                "timestamp": datetime.datetime.now().isoformat()
                            },
                            "payload": {
                                "response_to": "new_block",
                                "code": 711,
                                "message": "Invalid block",
                                "details": {
                                    "block_id": new_block.header.id
                                }
                            }
                        }
                        self.log(f"Received an invalid block {new_block.header.id}. Rejected.")
                else:
                    message = {
                        "action": "error",
                        "metadata": {
                            "source_id": self.id,
                            "timestamp": datetime.datetime.now().isoformat()
                        },
                        "payload": {
                            "response_to": "new_block",
                            "code": 712,
                            "message": "No block data provided"
                        }
                    }
                    self.log("Received an invalid request for a new block: No block data.")
            else:
                message = {
                    "action": "error",
                    "metadata": {
                        "source_id": self.id,
                        "timestamp": datetime.datetime.now().isoformat()
                    },
                    "payload": {
                        "response_to": "new_block",
                        "code": 713,
                        "message": "Payload is missing in the request"
                    }
                }
                self.log("Received an invalid request for a new block: Missing payload.")

            return message

    
    def create_and_seal_block(self):
        valid_transactions = []
        transaction_index = 1

        # Étape 1 : Validation des transactions
        for tx in self.transaction_pool:
            try:
                # Vérification de la signature de la transaction
                if tx.verify_sig(self.blockchain.actors[tx.source_id][0].public_key()):
                    # Réassigner un nouvel ID et recalculer le hash
                    valid_transaction = tx
                    valid_transaction.id = transaction_index
                    transaction_index += 1
                    valid_transaction.hash = valid_transaction.calculate_hash()
                    valid_transactions.append(valid_transaction)

                else:
                    raise ValueError("Invalid transaction signature")
                
            except Exception as e:
                # Journalisation des erreurs
                self.log(f"Transaction {tx.source_id}=>{tx.destination_id} "
                        f"[{tx.product.id},{tx.product.serial_number}] is invalid: {e}")
        
        if not valid_transactions:
            self.log("No valid transactions to seal into the block.")
            return None

        new_block = self.blockchain.new_block()
        new_block.transactions = valid_transactions  
        new_block.validator_id = self.id
        new_block.sign(self.private_key)
        new_block.hash = new_block.calculate_hash()
        return new_block

    def seal_curent_block(self):
        time.sleep(0.5)
        selected_validator = self.blockchain.select_validator()
        self.log(f'validator for the current block {selected_validator}')
        if self.id == selected_validator:
            new_block = self.create_and_seal_block()
            self.broadcast_new_block(new_block)
        return
    
    
    def handle_client(self, conn, addr):
        with conn:
            try:
                length_bytes = conn.recv(4)  # Receive the first 4 bytes indicating the length
                if not length_bytes:
                    return  # Connection was closed or error occurred
                message_length = int.from_bytes(length_bytes, 'big')
                data = b''
                while len(data) < message_length:
                    to_read = min(1024, message_length - len(data))
                    data_chunk = conn.recv(to_read)
                    if not data_chunk:
                        raise ConnectionError("Connection lost while receiving data.")
                    data += data_chunk

                json_data = json.loads(data.decode("utf-8"))
                self.log(f"Received from {addr}: {json_data['action']}")
                response = json.dumps(self.process_data(addr, json_data)).encode("utf-8")
                response_length = len(response)
                conn.sendall(response_length.to_bytes(4, 'big')) 
                conn.sendall(response)
            except Exception as e:
                self.log(f"Error receiving data from {addr}", error=e)
    
    def send_data(self, message, target_host, target_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((target_host, target_port))
                message = message.encode('utf-8')
                message_length = len(message)
                client_socket.sendall(message_length.to_bytes(4, 'big'))  # Send the length of the message
                client_socket.sendall(message)  # Send the actual message
                length_bytes = client_socket.recv(4)  # Receive the first 4 bytes indicating the length
                if not length_bytes:
                    return  # Connection was closed or error occurred
                message_length = int.from_bytes(length_bytes, 'big')
                data = b''
                while len(data) < message_length:
                    to_read = min(1024, message_length - len(data))
                    data_chunk = client_socket.recv(to_read)
                    if not data_chunk:
                        raise ConnectionError("Connection lost while receiving data.")
                    data += data_chunk
                return json.loads(data.decode('utf-8'))
            except ConnectionRefusedError:
                self.log(f"Failed to connect to {target_host} {target_port}.")
        
    
    def broadcast_transaction(self, dest_id, source_id, product_id, product_sn):
        transaction_broadcast_status = True
        new_transaction = create_new_transaction(dest_id, source_id, product_id, product_sn,self.private_key)
        message = json.dumps({
                "action": "new_transaction",
                "metadata": {
                    "source_id": self.id,"timestamp": datetime.datetime.now().isoformat() 
                },
                "payload": {
                    "new_transaction": new_transaction.to_dict()
                }
            })
        for server_ip, server_port in self.remote_nodes:
            try:
                response = self.send_data(message, server_ip, server_port)
                if response:
                    if response["action"]=="new_transaction_response" and response["payload"]:
                        if response["payload"]["status"]=="accepted":
                            self.log(f"Transacion succesfully sent to ('{server_ip}', {server_port})")
                    else:
                        reason = response["payload"].get("message", "Unknown reason")
                        self.log(f"Transaction rejected by ('{server_ip}', {server_port}): {reason}")
                        transaction_broadcast_status = False
                else:
                    self.log(f"No response from ('{server_ip}', {server_port})")
            except :
                self.log(f"Error when sennding trasacion to ('{server_ip}', {server_port})")
        
        if transaction_broadcast_status:
            self.transaction_pool.append(new_transaction)
            self.log(f"new transaction {source_id}=>{dest_id} [{product_id},{product_sn}] added to the pool")

        if len(self.transaction_pool) >= self.blockchain.transactions_per_block and transaction_broadcast_status:
            self.seal_curent_block()
        
        return transaction_broadcast_status


    def broadcast_new_block(self, new_block):
        # Convertir le bloc en un message JSON
        message = json.dumps({
            "action": "new_block",
            "metadata": {
                "source_id": self.id,
                "timestamp": datetime.datetime.now().isoformat()
            },
            "payload": {
                "new_block": new_block.to_dict()
            }
        })

        block_accepted = True

        # Parcourir tous les nœuds distants pour envoyer le bloc
        for server_ip, server_port in self.remote_nodes:
            try:
                # Envoi du message au nœud distant
                response = self.send_data(message, server_ip, server_port)
                # Vérification de la réponse du nœud distant
                if response and response.get("action") == "new_block_response": 
                    if not response or response.get("action") != "new_block_response":
                        self.log(f"Block {new_block.header.id} broadcast failed to ({server_ip}, {server_port}): {response['payload'].get('message', 'Unknown error')}")
                        block_accepted = False 
                else:
                    self.log(f"Unexpected response from ({server_ip}, {server_port}): {response}")
                    
            except Exception as e:
                # Gestion des erreurs lors de l'envoi
                self.log(f"Error when sending new block to ({server_ip}, {server_port}): {str(e)}")

        # Si le bloc a été accepté par au moins un nœud, tu peux l'ajouter définitivement à la blockchain
        if block_accepted:
            self.blockchain.chain.append(new_block)
            self.clean_pool(new_block)
            self.log(f"Block {new_block.header.id} successfully broadcasted and added to the local blockchain.")
            self.blockchain.reward_validator(self.id)
            self.save_blockchain()
        else:
            self.log(f"Block {new_block.header.id} was not accepted by any remote node.")

                
    def clean_pool(self, new_block):
        if not new_block.is_valid(self.blockchain.actors):
            print("New block is invalid, clean pool process canceled.")
            self.log("New block is invalid, cleaning pool canceled.")
            return

        if not new_block or not new_block.transactions:
            self.log("No transactions to clean from the pool.")
            return

        self.log("Starting pool cleaning process.")

        # Create a set of signatures from the new block for fast lookup
        new_transaction_signatures = {tx.signature for tx in new_block.transactions if tx.signature}
        if not new_transaction_signatures:
            self.log("No valid transaction signatures found in the new block.")

        # Log the current state of the transaction pool for debugging purposes
        self.log(f"Pool before cleaning: {len(self.transaction_pool)} transactions")

        # Remove transactions with matching signatures
        initial_pool_size = len(self.transaction_pool)
        self.transaction_pool = [
            tx for tx in self.transaction_pool if tx.signature not in new_transaction_signatures
        ]

        cleaned_count = initial_pool_size - len(self.transaction_pool)

        # Log how many transactions were removed from the pool
        self.log(f"Pool cleaned. {cleaned_count} transactions removed. Remaining transactions: {len(self.transaction_pool)}.")

    def log(self, message, display=True, error=None):
        x = datetime.datetime.now()
        log_message = f"{x} {message}"
        
        if error:
            # Ajoute le type d'erreur, le message, et la trace complète si disponible
            log_message += f"\n  [ERROR] Type: {type(error).__name__}, Message: {error}\n"
            log_message += f"  [TRACEBACK] {traceback.format_exc()}"

        if display:
            print(log_message)
            
        with open(self.log_file_path, "a") as f:
            f.write(log_message + "\n")
    
    def save_blockchain(self):
        self.log("Blockchain saved.")
        with open(self.blockchain_file_path, 'w') as f:
            json.dump(self.blockchain.to_dict(), f)
            f.flush()
            return


if __name__ == "__main__":
    def str_to_bytes(value):
        return value.encode()  # Default encoding is utf-8
    parser = argparse.ArgumentParser(description='Run the blockchain server.')
    parser.add_argument('--port', type=int, required=True, default=4000, help='Port number to run the server on. Default is 4000.')
    parser.add_argument('--http_port', type=int, required=True, default=8080, help='HTTP port number for additional server interface. Default is 8080.')
    parser.add_argument('--certificate', required=True, default='path/to/default/cert.pem', help='Path to the server certificate file. Default path is "path/to/default/cert.pem".')
    parser.add_argument('--private_key', required=True, default='path/to/default/key.pem', help='Path to the server private key file. Default path is "path/to/default/key.pem".')
    parser.add_argument('--key_passphrase', type=str_to_bytes, required=True, default='default_passphrase', help='Passphrase for the private key. Default is "default_passphrase".')
    parser.add_argument('--blockchain_path', required=True, default='path/to/default/blockchain.json', help='File path to save blockchain data. Default path is "path/to/default/blockchain.json".')
    parser.add_argument('--log_path', required=True, default='path/to/default/log.txt', help='File path for logging server activity. Default path is "path/to/default/log.txt".')
    parser.add_argument('--genesis', action='store_true', help='Flag to start the server as a genesis node.')
    parser.add_argument('--chest_value', type=int, default=1000, help='Value of the chest for proof of stake')
    parser.add_argument('--remote_nodes', nargs='*', default=[], help='List of remote node addresses in the format ip:port.')
    parser.add_argument('--max_transactions', type=int, default=2, help='Number of transactions per block.')

    try:
        args = parser.parse_args()
    except SystemExit:
        # Handle specific missing argument scenarios if needed
        print("Required arguments were missing.")
        parser.print_help()
        exit(1)

    # Convert ip:port strings into tuples
    remote_nodes = []
    if args.remote_nodes:
        remote_nodes = [
            [ip_port.split(':')[0].strip(), int(ip_port.split(':')[1].strip())]
            for ip_port in args.remote_nodes[0].split(',')  # Split the single string by commas
        ]
    
    server = Server(
        port=args.port,
        certificate_file_path=args.certificate,
        private_key_file_path=args.private_key,
        private_key_passphrase=args.key_passphrase,
        chest_value = args.chest_value,
        blockchain_file_path=args.blockchain_path,
        log_file_path=args.log_path,
        remote_nodes=remote_nodes,
        max_transactions=args.max_transactions,
        http_port=args.http_port
    )

    server.start_server(genesis_node=args.genesis)
