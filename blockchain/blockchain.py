import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """ Create a new Block in the Blockchain """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = [] # Reset pending list
        self.chain.append(block)
        return block

    def new_transaction(self, news_content, prediction, confidence):
        """ Adds a new verification record to the next block """
        self.current_transactions.append({
            'news': news_content,
            'prediction': prediction,
            'confidence': f"{confidence:.2f}%",
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """ Hashes a Block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]