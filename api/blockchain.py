import json
from web3 import Web3

# In a real application, you would get this from your compiled smart contract
MOCKED_NFT_CONTRACT_ABI = json.dumps([
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
])

# A mocked address for the smart contract
MOCKED_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"

# A mocked Ethereum node provider URL
MOCKED_ETHEREUM_NODE_URL = "https://mainnet.infura.io/v3/your-infura-project-id"

class BlockchainManager:
    def __init__(self, node_url=MOCKED_ETHEREUM_NODE_URL, contract_address=MOCKED_CONTRACT_ADDRESS, contract_abi=MOCKED_NFT_CONTRACT_ABI):
        # In a real application, you would connect to a real node
        # self.w3 = Web3(Web3.HTTPProvider(node_url))
        # self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

        # For this PoC, we are mocking the connection and contract
        self.mocked_nfts = {
            1: {"owner": "0x1234567890123456789012345678901234567890", "uri": "https://example.com/nft/1.json"},
            2: {"owner": "0x0987654321098765432109876543210987654321", "uri": "https://example.com/nft/2.json"},
        }

    def get_nft_details(self, token_id: int):
        """
        Gets the details of an NFT.
        In a real application, this would interact with the smart contract.
        """
        # Real implementation would look something like this:
        # owner = self.contract.functions.ownerOf(token_id).call()
        # token_uri = self.contract.functions.tokenURI(token_id).call()
        # return {"owner": owner, "token_uri": token_uri}

        # Mocked implementation
        if token_id in self.mocked_nfts:
            return self.mocked_nfts[token_id]
        else:
            return None

# Example usage:
if __name__ == "__main__":
    blockchain_manager = BlockchainManager()

    nft_1_details = blockchain_manager.get_nft_details(1)
    print(f"Details for NFT #1: {nft_1_details}")

    nft_3_details = blockchain_manager.get_nft_details(3)
    print(f"Details for NFT #3: {nft_3_details}")
