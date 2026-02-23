import json
import base64
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

    def mint_reward(self, owner_address: str, metadata_uri: str):
        """
        Mints a reward NFT for a player.
        In a real application, this would send a transaction to the smart contract.
        """
        # Real implementation would look something like this:
        # tx_hash = self.contract.functions.mint(owner_address, metadata_uri).transact()
        # return tx_hash

        # Mocked implementation
        token_id = max(self.mocked_nfts.keys()) + 1 if self.mocked_nfts else 1

        # Enhanced metadata for Shovel Master
        if "shovel_master" in metadata_uri:
             metadata = {
                 "name": "Shovel Master Achievement",
                 "description": "Awarded for successfully filling a dump truck with a shovel.",
                 "image": "https://games-universe.com/assets/shovel_nft.png",
                 "attributes": [
                     {"trait_type": "Skill", "value": "Master Shoveler"},
                     {"trait_type": "Trucks Filled", "value": 1}
                 ]
             }
             metadata_json = json.dumps(metadata)
             metadata_base64 = base64.b64encode(metadata_json.encode()).decode()
             metadata_uri = f"data:application/json;base64,{metadata_base64}"

        # Enhanced metadata for Money Climbing
        if "money_climbing" in metadata_uri:
             metadata = {
                 "name": "Money Climbing Master",
                 "description": "Awarded for reaching extreme heights and collecting treasure.",
                 "image": "https://games-universe.com/assets/climbing_nft.png",
                 "attributes": [
                     {"trait_type": "Skill", "value": "Elite Climber"},
                     {"trait_type": "Achievement", "value": "Summit Reached"}
                 ]
             }
             metadata_json = json.dumps(metadata)
             metadata_base64 = base64.b64encode(metadata_json.encode()).decode()
             metadata_uri = f"data:application/json;base64,{metadata_base64}"

        # Enhanced metadata for Animal Fighting
        if "animal_fighting" in metadata_uri:
             metadata = {
                 "name": "Animal Fighting Champion",
                 "description": "Awarded for victorious combat in the Animal Fighting AR arena.",
                 "image": "https://games-universe.com/assets/fighting_nft.png",
                 "attributes": [
                     {"trait_type": "Skill", "value": "Elite Combatant"},
                     {"trait_type": "Victory", "value": "Supreme Champion"}
                 ]
             }
             metadata_json = json.dumps(metadata)
             metadata_base64 = base64.b64encode(metadata_json.encode()).decode()
             metadata_uri = f"data:application/json;base64,{metadata_base64}"

        self.mocked_nfts[token_id] = {"owner": owner_address, "uri": metadata_uri}
        return {"status": "success", "token_id": token_id, "owner": owner_address}

# Example usage:
if __name__ == "__main__":
    blockchain_manager = BlockchainManager()

    nft_1_details = blockchain_manager.get_nft_details(1)
    print(f"Details for NFT #1: {nft_1_details}")

    nft_3_details = blockchain_manager.get_nft_details(3)
    print(f"Details for NFT #3: {nft_3_details}")
