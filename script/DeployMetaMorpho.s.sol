// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./lib/forge-std/src/Script.sol";
import "./lib/forge-std/src/console2.sol";
import {IMetaMorphoFactory} from "./morph-contracts/interfaces/IMetaMorphoFactory.sol";
import {IMetaMorpho} from "./morph-contracts/interfaces/IMetaMorpho.sol";

contract DeployMetaMorpho is Script {
    // Factory address on mainnet
    address constant FACTORY = 0xA9c3D3a366466Fa809d1Ae982Fb2c46E5fC41101;
    // USDC address on mainnet
    address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    function run() external {
        // Create and select the fork
        uint256 mainnetFork = vm.createFork(vm.envString("MAINNET_RPC_URL"));
        vm.selectFork(mainnetFork);

        // Start broadcasting transactions
        vm.startBroadcast();

        // Parameters for new MetaMorpho vault
        address owner = msg.sender;
        uint256 timelock = 1 days; // Example timelock period
        string memory name = "My MetaMorpho Vault";
        string memory symbol = "MMV";
        bytes32 salt = bytes32(uint256(1)); // Example salt

        // Create new MetaMorpho vault
        IMetaMorphoFactory factory = IMetaMorphoFactory(FACTORY);
        IMetaMorpho newVault = factory.createMetaMorpho(
            owner,
            timelock,
            USDC, // Using USDC as the asset
            name,
            symbol,
            salt
        );

        // Log the deployment information
        console2.log("New MetaMorpho vault deployed:");
        console2.log("Vault address:", address(newVault));
        console2.log("Total supply:", newVault.totalSupply());
        console2.log("Owner:", owner);
        console2.log("Asset (USDC):", USDC);
        console2.log("Name:", name);
        console2.log("Symbol:", symbol);

        vm.stopBroadcast();
    }
}
