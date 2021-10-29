# -*- Coding:utf-8 -*-
import datetime as _dt
import hashlib as _hashlib
import json as _json
from time import sleep


class Blockchain:
    """Blockchain class"""

    def __init__(self) -> None:
        print("List creation")
        self.chain = list()
        print("List creation done !!")
        genesis_block = self._create_block(index=0, data="Welcome in Genesis block",
                                           proof=100, previous_hash="0")
        print("genesis block creation done !!")
        self.chain.append(genesis_block)

    def _create_block(self, index: int, data: str, proof: int,
                      previous_hash: str) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash
        }
        return block

    def _to_digest(self, new_proof: int, previous_proof: int,
                   index: int, data: str) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proofs = 1
        check_proof = False
        print(new_proofs)
        while not check_proof:
            to_digest = self._to_digest(new_proof=new_proofs,
                                        previous_proof=previous_proof,
                                        index=index, data=data)
            hash_values = _hashlib.sha256(to_digest).hexdigest()
            if hash_values[:4] == "0000":
                check_proof = True
                print("\n\nProof computation done with success !!!")
                print("Proofs N°: {} | hash: {}\n\n".format(new_proofs, hash_values))
            else:
                new_proofs += 1
                print("Proofs N°: {} | hash: {}".format(new_proofs, hash_values))
            del hash_values

        return new_proofs

    def mine_block(self, data: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(previous_proof, index, data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(data=data, proof=proof,
                                   previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block

    def _hash(self, block: dict) -> str:
        """
            hash a block abd return the cryptographic hash of the block
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()
    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def is_chain_valid(self) -> bool:
        current_block = self.chain[0]
        block_index = current_block.get("index")

        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block["previous_hash"] != self._hash(current_block):
                return False
            current_proof = current_block["proof"]
            next_index, next_data, next_proof = (next_block["index"], next_block["data"],
                                  next_block["proof"])
            hash_value = _hashlib.sha256(self._to_digest(new_proof=next_proof,
                                                         previous_proof=current_proof, index=next_index,
                                                         data=next_data)).hexdigest()
            if hash_value[:4] != "0000":
                return False
            current_block = next_block
            block_index += 1
            
        return True


if __name__ == "__main__":
    bc = Blockchain()
    sleep(3)
    print(bc.chain)
    sleep(3)
    bc.mine_block("Hello World")

# Copyright Zeus-Security @2021
