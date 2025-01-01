from web3 import Web3
from dataclasses import dataclass
from typing import List

# -------------------------------------------------------------------------
# 1. Connect to your local Foundry (or Hardhat) fork
# -------------------------------------------------------------------------
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
if not w3.is_connected():
    print("❌ Not connected to local fork! Ensure anvil/HardHat is running.")
    exit(1)

# -------------------------------------------------------------------------
# 2. Replace with the NEW MetaMorph Vault Address
# -------------------------------------------------------------------------
NEW_METAMORPH_VAULT_ADDRESS = "0xf26f466633d7597192D7989a9e951B4B9725d1c1"

# -------------------------------------------------------------------------
# 3. Use an account with enough test ETH & correct roles
# -------------------------------------------------------------------------
TEST_ACCOUNT = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
PRIVATE_KEY = "PRIVATE_KEY(its anyways tested one, but still good to not have it in repo)"

# -------------------------------------------------------------------------
# 4. Data Structures (Same as your original code)
# -------------------------------------------------------------------------
@dataclass
class MarketParams:
    loan_token: str
    collateral_token: str
    oracle: str
    irm: str
    lltv: int

@dataclass
class MarketAllocation:
    market_params: MarketParams
    assets: int

# -------------------------------------------------------------------------
# 5. ABI for the `reallocate(MarketAllocation[] allocations)` in the **vault**
# -------------------------------------------------------------------------
REALLOCATE_ABI = [{
    "inputs": [{
        "components": [{
            "components": [
                {"internalType": "address", "name": "loanToken",       "type": "address"},
                {"internalType": "address", "name": "collateralToken", "type": "address"},
                {"internalType": "address", "name": "oracle",          "type": "address"},
                {"internalType": "address", "name": "irm",             "type": "address"},
                {"internalType": "uint256", "name": "lltv",            "type": "uint256"}
            ],
            "internalType": "struct MarketParams",
            "name": "marketParams",
            "type": "tuple"
        }, {
            "internalType": "uint256",
            "name": "assets",
            "type": "uint256"
        }],
        "internalType": "struct MarketAllocation[]",
        "name": "allocations",
        "type": "tuple[]"
    }],
    "name": "reallocate",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}]

# -------------------------------------------------------------------------
# 6. Helper: Format allocations for the `reallocate` call
# -------------------------------------------------------------------------
def format_allocations(allocations: List[MarketAllocation]):
    formatted = []
    for allocation in allocations:
        mp = allocation.market_params
        formatted.append({
            'marketParams': {
                'loanToken':       mp.loan_token,
                'collateralToken': mp.collateral_token,
                'oracle':          mp.oracle,
                'irm':             mp.irm,
                'lltv':            mp.lltv
            },
            'assets': allocation.assets
        })
    return formatted

# -------------------------------------------------------------------------
# 7. Simulate & Send Transaction (with build_transaction() in Web3.py 7.x)
# -------------------------------------------------------------------------
def simulate_and_send_reallocate(allocations: List[MarketAllocation]):
    """
    1. Create a contract instance using the NEW MetaMorph Vault address.
    2. Simulate (call) the reallocate function with your allocations.
    3. Build the transaction, estimate gas, sign & send.
    4. Wait for receipt.
    """
    contract = w3.eth.contract(address=NEW_METAMORPH_VAULT_ADDRESS, abi=REALLOCATE_ABI)

    # Prepare the data structures
    formatted_allocs = format_allocations(allocations)

    # ---------------------------
    # Step 1: Simulation (static call)
    # ---------------------------
    print("Step 1: Simulation (static call)...")
    try:
        contract.functions.reallocate(formatted_allocs).call({"from": TEST_ACCOUNT})
        print("✔ Simulation successful (no revert).")
    except Exception as exc:
        print(f"✘ Simulation failed: {exc}")
        return None

    # ---------------------------
    # Step 2: Build & Send TX
    # ---------------------------
    print("\nStep 2: Sending Transaction (using build_transaction + estimate_gas)...")
    try:
        # (a) Build a partial transaction that includes 'data'
        #     but do NOT set 'nonce', 'gas', 'gasPrice', 'chainId' yet.
        #     Then we can extract 'data' from it for gas estimation.
        partial_tx = contract.functions.reallocate(formatted_allocs).build_transaction({
            "from": TEST_ACCOUNT
        })

        # (b) Estimate gas using the 'data' & 'to'
        gas_estimate = w3.eth.estimate_gas({
            "from": TEST_ACCOUNT,
            "to":   partial_tx['to'],
            "data": partial_tx['data']
        })

        # (c) Build the final transaction with all fields
        final_tx = {
            "from":      TEST_ACCOUNT,
            "to":        partial_tx['to'],
            "nonce":     w3.eth.get_transaction_count(TEST_ACCOUNT),
            "gas":       gas_estimate + 50000,  # buffer
            "gasPrice":  w3.eth.gas_price,
            "chainId":   w3.eth.chain_id,
            "data":      partial_tx['data']  # same data
        }

        # (d) Sign & send
        signed_tx = w3.eth.account.sign_transaction(final_tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✔ Transaction sent! Hash = {tx_hash.hex()}")

        # (e) Wait for receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("✔ Transaction confirmed!")
        print(f"Gas Used: {receipt.gasUsed}")
        return receipt

    except Exception as exc:
        print(f"✘ Transaction failed: {exc}")
        return None

# -------------------------------------------------------------------------
# 8. Example: Using the newly created vault
# -------------------------------------------------------------------------
def main():
    print("✓ Connected to local fork.\n")

    # Example MarketParams
    market_params1 = MarketParams(
        loan_token="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",    # USDC
        collateral_token="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        oracle="0x986b5E1e1755e3C2440e960477f25201B0a8bbD4",          # example chainlink aggregator
        irm="0x46415998764C29aB2a25CbeA6254146D50D22687",             # example IRM
        lltv=860000000000000000  # 86% in 1e18
    )

    allocation1 = MarketAllocation(
        market_params=market_params1,
        assets=Web3.to_wei(1, 'ether')
    )
    allocations = [allocation1]

    print("---- Allocation Setup ----")
    print(f"Vault Address    : {NEW_METAMORPH_VAULT_ADDRESS}")
    print(f"Loan Token       : {allocation1.market_params.loan_token}")
    print(f"Collateral Token : {allocation1.market_params.collateral_token}")
    print(f"Assets           : {allocation1.assets}")
    print(f"Sender Account   : {TEST_ACCOUNT}")
    print("-------------------------\n")

    # Execute the function
    receipt = simulate_and_send_reallocate(allocations)
    if receipt:
        print("Reallocate transaction completed successfully.")
    else:
        print("Reallocate transaction not sent or failed.")

# -------------------------------------------------------------------------
# 9. Run if called directly
# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()
