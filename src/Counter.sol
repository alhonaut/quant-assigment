// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Counter {
    uint256 public number;

    /// @notice Increments the counter by 1
    function increment() public {
        number++;
    }

    /// @notice Sets the counter to a new number
    /// @param newNumber The new value to set
    function setNumber(uint256 newNumber) public {
        number = newNumber;
    }
}
