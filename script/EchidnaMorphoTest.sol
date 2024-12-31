// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.7;

import "../lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";

import "./morph-contracts/MetaMorpho.sol";

// Mock ERC20 for testing
contract ERC20Mock is ERC20 {
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract EchidnaMorphoTest is MetaMorpho {
    // Test token contracts for simulation
    ERC20Mock public loanToken;
    ERC20Mock public collateralToken;

    constructor()
        MetaMorpho(
            address(this), // Owner
            address(1), // morpho
            1 days, // reallocation interval
            address(0), // placeholder for loanToken; it gets set dynamically
            "Test",
            "TEST"
        )
    {
        // Deploy two mock ERC20 tokens
        loanToken = new ERC20Mock("Loan Token", "LOAN");
        collateralToken = new ERC20Mock("Collateral Token", "COLL");
    }

    // Generate MarketParams, returning random addresses for oracle and irm, and a random lltv value
    function generateMarketParams(
        uint256 seed
    ) internal view returns (MarketParams memory) {
        return
            MarketParams({
                loanToken: address(loanToken),
                collateralToken: address(collateralToken),
                oracle: address(uint160((seed % 100) + 1)),
                irm: address(uint160((seed % 100) + 101)),
                lltv: seed % 1e18 // Random LLTV between 0 and 1e18
            });
    }

    // Convert arrays of seeds & amounts into MarketAllocation structs
    function generateAllocations(
        uint256[] calldata seeds,
        uint256[] calldata amounts
    ) internal view returns (MarketAllocation[] memory) {
        uint256 len = seeds.length < amounts.length
            ? seeds.length
            : amounts.length;
        MarketAllocation[] memory allocations = new MarketAllocation[](len);

        for (uint256 i = 0; i < len; i++) {
            allocations[i] = MarketAllocation({
                marketParams: generateMarketParams(seeds[i]),
                assets: amounts[i]
            });
        }
        return allocations;
    }

    // Echidna test function
    function echidna_reallocate(
        uint256[] calldata seeds,
        uint256[] calldata amounts
    ) public returns (bool) {
        require(seeds.length > 0 && amounts.length > 0, "Empty inputs");

        // Build allocations
        MarketAllocation[] memory allocations = generateAllocations(
            seeds,
            amounts
        );

        // Try to call reallocate
        try this.reallocate(allocations) {
            // If it succeeds, that's fine
            return true;
        } catch Error(string memory reason) {
            // If it reverts with "InconsistentReallocation", we treat that as an expected revert
            return
                keccak256(bytes(reason)) ==
                keccak256(bytes("InconsistentReallocation"));
        } catch {
            // Any other revert or low-level error is unexpected => false
            return false;
        }
    }
}
