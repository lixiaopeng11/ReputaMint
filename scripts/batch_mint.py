from web3 import Web3
from eth_account import Account
import json

def load_wallets(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def main():
    web3 = Web3(Web3.HTTPProvider("https://sepolia.era.zksync.dev"))

    with open("config/mint_abi.json") as f:
        abi = json.load(f)
    contract = web3.eth.contract(
        address="0xYourContractAddressHere",
        abi=abi
    )

    wallets = load_wallets("config/wallets.txt")
    for privkey in wallets:
        acct = Account.from_key(privkey)
        try:
            tx = contract.functions.mint().build_transaction({
                'from': acct.address,
                'nonce': web3.eth.get_transaction_count(acct.address),
                'gas': 200000,
                'gasPrice': web3.eth.gas_price
            })
            signed = acct.sign_transaction(tx)
            tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
            print(f"{acct.address[-6:]}... ✅ TX: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"{acct.address[-6:]} ❌ Error: {str(e)}")

if __name__ == "__main__":
    main()