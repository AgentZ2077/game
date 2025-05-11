
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction, AccountMeta
from solana.system_program import SYS_PROGRAM_ID
from base64 import b64decode
import hashlib

ZK_PROGRAM_ID = PublicKey("ZkMemVer1111111111111111111111111111111111")

def derive_memory_pda(signer_pubkey: PublicKey) -> PublicKey:
    seeds = [b"memory", bytes(signer_pubkey)]
    return PublicKey.find_program_address(seeds, ZK_PROGRAM_ID)[0]

def hash_memory(memory_data: str) -> bytes:
    return hashlib.sha256(memory_data.encode()).digest()

def build_store_tx(client: Client, signer: Keypair, memory_data: str):
    hash_bytes = hash_memory(memory_data)
    pda = derive_memory_pda(signer.public_key)
    ix_data = b"\x00" + hash_bytes  # store_memory_hash discriminator
    keys = [
        AccountMeta(pubkey=pda, is_signer=False, is_writable=True),
        AccountMeta(pubkey=signer.public_key, is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    tx = Transaction()
    tx.add(Transaction().add_instruction(
        program_id=ZK_PROGRAM_ID,
        data=ix_data,
        keys=keys
    ))
    return tx

def build_verify_tx(client: Client, signer: Keypair, memory_data: str):
    hash_bytes = hash_memory(memory_data)
    pda = derive_memory_pda(signer.public_key)
    ix_data = b"\x01" + hash_bytes  # verify_proof discriminator
    keys = [
        AccountMeta(pubkey=pda, is_signer=False, is_writable=False),
        AccountMeta(pubkey=signer.public_key, is_signer=True, is_writable=False),
    ]
    tx = Transaction()
    tx.add(Transaction().add_instruction(
        program_id=ZK_PROGRAM_ID,
        data=ix_data,
        keys=keys
    ))
    return tx
