from web3 import Web3


def get_publics(path: str):
    with open(path, 'r') as f:
        data = f.read().splitlines()
    return data


def get_nonces(publics: list, chains: dict) -> dict:
    nonces = dict()
    for chain_name, rpc in chains.items():
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            chain_nonces = list()
            for wallet in publics:
                try:
                    chain_nonces.append(w3.eth.get_transaction_count(Web3.to_checksum_address(wallet)))
                except Exception as err:
                    print(err)
                    chain_nonces.append(None)
            nonces[chain_name] = chain_nonces
        except Exception as err:
            print(err)
            nonces[chain_name] = None
    return nonces
