# Quant Assignment: Optimized Fund Allocation and MetaMorpho Interaction

## Overview

This repository contains an optimized workflow for data retrieval, fund allocation, and interaction with the MetaMorpho Protocol. It comprises Python scripts and Solidity files to fetch on-chain data, simulate vault allocations, deploy smart contracts on a mainnet fork, and securely interact with the blockchain.

---

## Components

### 1. **Data Pipeline and Allocation Optimization**
**File**: `main.py`

This script:
- Fetches data from the Morpho API.
- Stores data in a local SQL server.
- Simulates fund allocation (starting with 1 million USD).
- Uses linear programming to optimize fund distribution across vaults.
- Integrates risk management strategies to avoid high-risk allocations.

**Setup and Execution**:
1. Create a Python virtual environment:
   ```bash
   python -m venv myenv
   ```
2. Activate the environment:
   ```bash
   source myenv/bin/activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the script:
   ```bash
   python script/main.py
   ```

---

### 2. **Deploying MetaMorpho Smart Contract**
**File**: `DeployMetaMorpho.s.sol`

This script uses Foundry to:
- Deploy a simulated vault on a forked mainnet.
- Interact with the deployed MetaMorpho Factory using USDC.
- Display transaction logs and details.

**Setup and Execution**:
1. Fork the mainnet using your RPC URL:
   ```bash
   anvil --fork-url https://mainnet.infura.io/v3/$INFURA_KEY
   ```
2. Deploy the script:
   ```bash
   forge script script/DeployMetaMorpho.s.sol:DeployMetaMorpho 
      --fork-url https://mainnet.infura.io/v3/$INFURA_KEY        
      --broadcast
   ```

---

### 3. **Web3 Interaction with Deployed Contract**
**File**: `Scripter.py`

This script connects to the forked chain via Web3.py to:
1. Ensure the chain is ready for transactions.
2. Simulate a transaction to verify functionality.
3. Send a signed transaction to the forked mainnet.

**Setup and Execution**:
1. Complete the deployment step above.
2. Run the script:
   ```bash
   python script/Scripter.py
   ```

---

## Security Enhancements
- **Echidna Fuzz Testing**:
  - `EchidnaMorphoTest.sol` ensures the `reallocate` function in MetaMorpho.sol is secure.
- **Static Analysis**:
  - Security report generated using Cyfrin Aderyn static analyzer to validate contract security (see `report.md`).

---

## Structure of the Repository
- `script/main.py`: Python-based data pipeline and fund allocation.
- `script/DeployMetaMorpho.s.sol`: Solidity script for mainnet fork deployment.
- `script/Scripter.py`: Python script for Web3 interaction.
- `script/EchidnaMorphoTest.sol`: Echidna test file for contract security.
- `report.md`: Security analysis report.
- `requirements.txt`: Python dependencies.

---

## Requirements and Dependencies
- Python 3.x
- Foundry (for mainnet fork and deployment)
- Morpho API
- Web3.py
- PuLP (for linear programming)

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Running Tests and Simulation
1. Setup the local environment or fork the mainnet as described above.
2. Run the Python scripts and Foundry commands to simulate transactions.
3. Review logs and transaction outputs to verify success.

---

## Notes
- Make sure to replace `$INFURA_KEY` with your actual Infura API key.
- The project has been tested with dummy data for demonstration purposes.
- Refer to the security report for detailed contract analysis.

---

## Optional Enhancements
- Advanced reallocation strategies.
- Frontend for visualization.
- Additional Foundry unit tests with coverage reports.


```shell
$ forge --help
$ anvil --help
$ cast --help
```
