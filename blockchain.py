import hashlib
from datetime import datetime
import random
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.exceptions import InvalidSignature

class Product:
    def __init__(self, product_id, serial_number):
        self.id = product_id
        self.serial_number = serial_number

    def __str__(self):
        return f"[Product] ID: {self.id}, Serial Number: {self.serial_number}"

    def attributes_to_string(self):
        return f'{self.id}{self.serial_number}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'serial_number': self.serial_number
        }
    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.id == other.id and self.serial_number == other.serial_number
    
class BlockHeader:
    def __init__(self, block_id, version, previous_hash, timestamp):
        self.id = block_id
        self.version = version
        self.previous_hash = previous_hash
        self.timestamp = timestamp

    def __str__(self):
        return (f"[BlockHeader] ID: {self.id}, Version: {self.version}, "
                f"Previous Hash: {self.previous_hash}, Timestamp: {self.timestamp}")

    def to_dict(self):
        return {
            'id': self.id,
            'version': self.version,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp.isoformat()  # datetime object serialized as ISO format string
        }
    def __eq__(self, other):
        if not isinstance(other, BlockHeader):
            return False
        return (self.id == other.id and
                self.version == other.version and
                self.previous_hash == other.previous_hash and
                self.timestamp == other.timestamp)
    
class BlockTransaction:
    def __init__(self, transaction_id, timestamp, source_id, product, destination_id, signature=None):
        self.id = transaction_id
        self.timestamp = timestamp
        self.source_id = source_id
        self.product = product
        self.destination_id = destination_id
        self.signature = signature
        self.hash = None

    def __str__(self):
        return (f"\n\t[Transaction N° {self.id}]"
                f"\n\t  Timestamp: {self.timestamp}"
                f"\n\t  Source ID: {self.source_id}"
                f"\n\t  Product: {self.product}"
                f"\n\t  Destination ID: {self.destination_id}"
                f"\n\t  Signature: {self.signature}"
                f"\n\t  Hash: {self.hash}")
    
    def calculate_hash(self):
        transaction_string = f'{self.id}{self.timestamp}{self.source_id}{self.product.attributes_to_string()}{self.destination_id}{self.signature}'
        return hashlib.sha256(transaction_string.encode()).hexdigest()
    
    def verify_sig(self, public_key):
        transaction_details = f'{self.timestamp}{self.source_id}{self.product.attributes_to_string()}{self.destination_id}'
        return Crypto.verify_data(transaction_details, self.signature, public_key)

    def sign(self,private_key):
        transaction_details = f'{self.timestamp}{self.source_id}{self.product.attributes_to_string()}{self.destination_id}'
        self.signature = Crypto.sign_data(transaction_details, private_key)
        self.hash = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'source_id': self.source_id,
            'product': self.product.to_dict(),
            'destination_id': self.destination_id,
            'signature': self.signature or "",  # Gérer les signatures absentes
            'hash': self.hash or ""             # Gérer les hachages non calculés
        }
    def __eq__(self, other):
        if not isinstance(other, BlockTransaction):
            return False
        return (self.id == other.id and
                self.timestamp == other.timestamp and
                self.source_id == other.source_id and
                self.product == other.product and
                self.destination_id == other.destination_id and
                self.signature == other.signature and
                self.hash == other.hash)
@staticmethod
def create_new_transaction(dest_id, source_id, product_id, product_sn, private_key):
    new_transaction = BlockTransaction(None, datetime.now(), source_id, Product(product_id, product_sn), dest_id)
    new_transaction.sign(private_key)
    return new_transaction
     
class Block:
    def __init__(self, header_id, version, previous_hash, timestamp):
        self.header = BlockHeader(header_id, version, previous_hash, timestamp)
        self.transactions = []
        self.validator_id = None
        self.signature = None
        self.hash = None

    def __str__(self):
        transactions_str = ''.join(str(transaction) + "\n" for transaction in self.transactions)
        return (f'\n\t{"-"*50} Block {self.header.id} {"-"*50}\n'
                f'\tHEADER: {self.header}\n\tTRANSACTIONS:\n{transactions_str}'
                f'\n\tSIGNATURE: {self.signature}\n\tVALIDATOR: {self.validator_id}\n'
                f'\n\tTOTAL TRANSACTIONS: {len(self.transactions)}\n\tHASH: {self.hash}' )

    def sign(self,private_key):
        header_string = f'{self.header.id}{self.header.version}{self.header.previous_hash}{self.header.timestamp}'
        transactions_hash = ''.join(transaction.calculate_hash() for transaction in self.transactions)
        self.signature = Crypto.sign_data(f'{header_string}{transactions_hash}{self.validator_id}', private_key)

    def verify_sig(self, public_key):
        header_string = f'{self.header.id}{self.header.version}{self.header.previous_hash}{self.header.timestamp}'
        transactions_hash = ''.join(transaction.calculate_hash() for transaction in self.transactions)
        return Crypto.verify_data(f'{header_string}{transactions_hash}{self.validator_id}', self.signature, public_key)
    
    def calculate_hash(self):
        header_string = f'{self.header.id}{self.header.version}{self.header.previous_hash}{self.header.timestamp}'
        transactions_hash = ''.join(transaction.calculate_hash() for transaction in self.transactions)
        return hashlib.sha256(f'{header_string}{transactions_hash}{self.validator_id}{self.signature}'.encode()).hexdigest()

    def add_transaction(self, source_id, product_id, product_serial_number, destination_id, private_key):
        if self.hash:
            raise Exception('Error: Block is already sealed.')
        transaction_id = len(self.transactions) + 1
        new_transaction = BlockTransaction(transaction_id, datetime.now(), source_id, Product(product_id, product_serial_number), destination_id)
        new_transaction.sign(private_key)
        self.transactions.append(new_transaction)
        new_transaction.hash = new_transaction.calculate_hash()
        return new_transaction
    
    def is_valid(self, actors):
        for transaction in self.transactions:
            if not transaction.verify_sig(actors[transaction.source_id][0].public_key()):
                print(f"Transaction {transaction.id} invalid!")
                return False
        if not self.verify_sig((actors[self.validator_id][0].public_key())):
            return False
        if self.hash != self.calculate_hash():
            return False
        return True

    def to_dict(self):
        return {
            'header': self.header.to_dict(),
            'transactions': [transaction.to_dict() for transaction in self.transactions],
            'validator_id': self.validator_id or "",  # Champ `validator_id` par défaut vide
            'signature': self.signature or "",        # Champ `signature` par défaut vide
            'hash': self.hash or ""                   # Champ `hash` par défaut vide
        }
    def __eq__(self, other):
        if not isinstance(other, Block):
            return False
        return (self.header == other.header and
                self.transactions == other.transactions and
                self.validator_id == other.validator_id and
                self.signature == other.signature and
                self.hash == other.hash)
    
class Blockchain:
    def __init__(self, version, transactions_per_block  = 2):
        self.chain = []
        self.version = version
        self.transactions_per_block = transactions_per_block
        self.create_genesis_block()
        self.actors = {}

    def __str__(self):
        # Header for the blockchain
        blockchain_str = "\n" + "=" * 30 + " Blockchain " + "=" * 30 + "\n\n"

        # Display General Info
        blockchain_str += f"Version: {self.version}\n"
        blockchain_str += f"Transactions Per Block: {self.transactions_per_block}\n\n"

        # Display Actors
        blockchain_str += "Actors:\n"
        blockchain_str += "-" * 80 + "\n"
        for actor, value in self.actors.items():
            blockchain_str += f"  - {actor}:\n"
            blockchain_str += f"      Chest: {value[1]}\n"
            blockchain_str += f"      Reputation: {value[2]}\n"
        blockchain_str += "-" * 80 + "\n\n"

        # Display Blocks in the Chain
        blockchain_str += "Blocks in the Chain:\n"
        blockchain_str += "-" * 80 + "\n"
        for block in self.chain:
            blockchain_str += f"{str(block)}\n"
        blockchain_str += "-" * 80 + "\n"

        return blockchain_str

    def create_genesis_block(self):
        genesis_block = Block(0, self.version, '0' * 64, datetime.now())
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def new_block(self):
        if not self.chain[-1].hash:
            raise ValueError('Error: The last block is not sealed.')
        new_block = Block(len(self.chain), self.version, self.chain[-1].hash, datetime.now())
        return new_block

    def is_valid(self):
        previous_block_hash = '0' * 64
        for block in self.chain:
            if block.header.previous_hash != previous_block_hash:
                print("error in block hash")
                return False
            for block in self.chain:
                if not block.is_valid(self.actors):
                    return False
            previous_block_hash = block.calculate_hash()
        return True
    
    def to_dict(self):
        return {
            'chain': [block.to_dict() for block in self.chain],  # Convert each block to a dictionary
            'version': self.version,  # Blockchain version
            'transactions_per_block': self.transactions_per_block,  # Include transactions per block
            'actors': {actor_id: {
                'certificate': certificate.public_bytes(serialization.Encoding.PEM).decode(),
                'chest': chest,
                'reputation': reputation
            } for actor_id, (certificate, chest, reputation) in self.actors.items()}
        }
    def __eq__(self, other):
        if not isinstance(other, Blockchain):
            return False
        return (self.chain == other.chain and
                self.version == other.version and
                self.transactions_per_block == other.transactions_per_block and
                self.actors == other.actors)

    def reward_validator(self, actor_id, reward_chest=50, reward_reputation=10):
        if actor_id in self.actors:
            certificate, chest, reputation = self.actors[actor_id]
            self.actors[actor_id] = (certificate, chest + reward_chest, reputation + reward_reputation)
            print(f"Validator {actor_id} rewarded: +{reward_chest} chest, +{reward_reputation} reputation")
    
    def penalize_validator(self, actor_id, penalty_chest=0.1, penalty_reputation=0.5):
        if actor_id in self.actors:
            certificate, chest, reputation = self.actors[actor_id]
            new_chest = max(0, chest - chest * penalty_chest)  # Réduction proportionnelle du chest
            new_reputation = max(0, reputation - reputation * penalty_reputation)  # Réduction proportionnelle de la réputation
            self.actors[actor_id] = (certificate, new_chest, new_reputation)
            print(f"Validator {actor_id} penalized: -{penalty_chest*100:.1f}% chest, -{penalty_reputation*100:.1f}% reputation")

    def select_validator(self, previous_block_hash=None):
        # Calcul du total des stakes pondérés par la réputation
        total_weighted_stake = sum(stake * reputation for _, stake, reputation in self.actors.values())
        if total_weighted_stake == 0:
            raise ValueError("No stakes or reputation in the system.")
        # Convertir le dernier hash en un nombre
        if previous_block_hash:
            hash_value = int(previous_block_hash, 16)
        else:
            hash_value = int(self.chain[-1].hash, 16)

        # Utiliser ce hash pour choisir un index aléatoire proportionnel au stake pondéré
        cumulative_weight = 0
        random_value = hash_value % total_weighted_stake
        for actor_id, (_, stake, reputation) in self.actors.items():
            cumulative_weight += stake * reputation
            if cumulative_weight >= random_value:
                return actor_id


        
class Crypto:
    @staticmethod
    def get_privatekey_from_file(private_key_path, private_key_password):
        if isinstance(private_key_password,str):
            private_key_password = private_key_password.encode()
        with open(private_key_path, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=private_key_password)

    @staticmethod
    def sign_data(data, private_key):
        signature = private_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
        return signature.hex()
    
    @staticmethod
    def get_certificate_from_file(certificate_file_path):
        with open(certificate_file_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            return x509.load_pem_x509_certificate(cert_data)
        
    @staticmethod
    def verify_data(data, signature, public_key):
        try:
            public_key.verify(bytes.fromhex(signature), data.encode(), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

def convert_to_product(product_data):
    if not isinstance(product_data, dict) or 'id' not in product_data or 'serial_number' not in product_data:
        raise ValueError("Invalid product data for conversion.")
    return Product(product_data['id'], product_data['serial_number'])

def convert_to_blocktransaction(transaction_data):
    if not isinstance(transaction_data, dict):
        raise ValueError("Invalid transaction data for conversion.")
    
    required_fields = ['id', 'timestamp', 'source_id', 'product', 'destination_id']
    for field in required_fields:
        if field not in transaction_data:
            raise ValueError(f"Missing field '{field}' in transaction data.")

    product = convert_to_product(transaction_data['product'])
    transaction = BlockTransaction(
        transaction_id=transaction_data['id'],
        timestamp=datetime.fromisoformat(transaction_data['timestamp']),
        source_id=transaction_data['source_id'],
        product=product,
        destination_id=transaction_data['destination_id'],
        signature=transaction_data.get('signature')
    )
    transaction.hash = transaction_data.get('hash')  # Optionnel, peut être None
    return transaction

def convert_to_block(block_data):
    if not isinstance(block_data, dict) or 'header' not in block_data or 'transactions' not in block_data:
        raise ValueError("Invalid block data for conversion.")
    
    header_data = block_data['header']
    block = Block(
        header_id=header_data['id'],
        version=header_data['version'],
        previous_hash=header_data['previous_hash'],
        timestamp=datetime.fromisoformat(header_data['timestamp'])
    )
    # Ajout des transactions
    for tx_data in block_data['transactions']:
        transaction = convert_to_blocktransaction(tx_data)
        block.transactions.append(transaction)
    
    # Ajout des nouveaux champs
    block.validator_id = block_data.get('validator_id')  # Optionnel
    block.signature = block_data.get('signature')       # Optionnel
    block.hash = block_data.get('hash')                 # Optionnel
    
    return block

def convert_to_blockchain(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid blockchain data for conversion.")
    
    # Check for required fields
    required_fields = ['chain', 'version', 'transactions_per_block', 'actors']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field '{field}' in blockchain data.")
    
    # Create blockchain with transactions_per_block
    blockchain = Blockchain(data['version'], data['transactions_per_block'])
    blockchain.chain = []  # Reset chain to avoid the default genesis block
    
    # Reconstruct the chain of blocks
    for block_data in data['chain']:
        block = convert_to_block(block_data)
        blockchain.chain.append(block)
    
    # Reconstruct actors (certificates, chest, reputation)
    for actor_id, actor_data in data['actors'].items():
        certificate_pem = actor_data['certificate']
        chest = actor_data['chest']
        reputation = actor_data['reputation']
        
        # Load the certificate from PEM format
        certificate = x509.load_pem_x509_certificate(certificate_pem.encode())
        blockchain.actors[actor_id] = (certificate, chest, reputation)

    return blockchain
