# Aderyn Analysis Report

This report was generated by [Aderyn](https://github.com/Cyfrin/aderyn), a static analysis tool built by [Cyfrin](https://cyfrin.io), a blockchain security company. This report is not a substitute for manual audit or security review. It should not be relied upon for any purpose other than to assist in the identification of potential security vulnerabilities.
# Table of Contents

- [Summary](#summary)
  - [Files Summary](#files-summary)
  - [Files Details](#files-details)
  - [Issue Summary](#issue-summary)
- [High Issues](#high-issues)
  - [H-1: Contract Name Reused in Different Files](#h-1-contract-name-reused-in-different-files)
- [Low Issues](#low-issues)
  - [L-1: Centralization Risk for trusted owners](#l-1-centralization-risk-for-trusted-owners)
  - [L-2: Solidity pragma should be specific, not wide](#l-2-solidity-pragma-should-be-specific-not-wide)
  - [L-3: Missing checks for `address(0)` when assigning values to address state variables](#l-3-missing-checks-for-address0-when-assigning-values-to-address-state-variables)
  - [L-4: `public` functions not used internally could be marked `external`](#l-4-public-functions-not-used-internally-could-be-marked-external)
  - [L-5: Define and use `constant` variables instead of using literals](#l-5-define-and-use-constant-variables-instead-of-using-literals)
  - [L-6: Event is missing `indexed` fields](#l-6-event-is-missing-indexed-fields)
  - [L-7: PUSH0 is not supported by all chains](#l-7-push0-is-not-supported-by-all-chains)
  - [L-8: Internal functions called only once can be inlined](#l-8-internal-functions-called-only-once-can-be-inlined)


# Summary

## Files Summary

| Key | Value |
| --- | --- |
| .sol Files | 14 |
| Total nSLOC | 1168 |


## Files Details

| Filepath | nSLOC |
| --- | --- |
| src/Counter.sol | 10 |
| src/DeployMetaMorpho.s.sol | 36 |
| src/EchidnaMorphoTest.sol | 72 |
| src/morph-contracts/MetaMorpho.sol | 743 |
| src/morph-contracts/MetaMorphoFactory.sol | 46 |
| src/morph-contracts/interfaces/IMetaMorpho.sol | 86 |
| src/morph-contracts/interfaces/IMetaMorphoFactory.sol | 14 |
| src/morph-contracts/libraries/ConstantsLib.sol | 7 |
| src/morph-contracts/libraries/ErrorsLib.sol | 33 |
| src/morph-contracts/libraries/EventsLib.sol | 48 |
| src/morph-contracts/libraries/PendingLib.sol | 24 |
| src/morph-contracts/mocks/ERC20Mock.sol | 18 |
| src/morph-contracts/mocks/IrmMock.sol | 23 |
| src/morph-contracts/mocks/OracleMock.sol | 8 |
| **Total** | **1168** |


## Issue Summary

| Category | No. of Issues |
| --- | --- |
| High | 1 |
| Low | 8 |


# High Issues

## H-1: Contract Name Reused in Different Files

When compiling contracts with certain development frameworks (for example: Truffle), having contracts with the same name across different files can lead to one being overwritten.

<details><summary>2 Found Instances</summary>


- Found in src/EchidnaMorphoTest.sol [Line: 9](src/EchidnaMorphoTest.sol#L9)

	```solidity
	contract ERC20Mock is ERC20 {
	```

- Found in src/morph-contracts/mocks/ERC20Mock.sol [Line: 6](src/morph-contracts/mocks/ERC20Mock.sol#L6)

	```solidity
	contract ERC20Mock is ERC20 {
	```

</details>



# Low Issues

## L-1: Centralization Risk for trusted owners

Contracts have owners with privileged rights to perform admin tasks and need to be trusted to not perform malicious updates or drain funds.

<details><summary>8 Found Instances</summary>


- Found in src/morph-contracts/MetaMorpho.sol [Line: 32](src/morph-contracts/MetaMorpho.sol#L32)

	```solidity
	    Ownable2Step,
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 193](src/morph-contracts/MetaMorpho.sol#L193)

	```solidity
	    function setCurator(address newCurator) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 205](src/morph-contracts/MetaMorpho.sol#L205)

	```solidity
	    ) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 215](src/morph-contracts/MetaMorpho.sol#L215)

	```solidity
	    function setSkimRecipient(address newSkimRecipient) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 224](src/morph-contracts/MetaMorpho.sol#L224)

	```solidity
	    function submitTimelock(uint256 newTimelock) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 240](src/morph-contracts/MetaMorpho.sol#L240)

	```solidity
	    function setFee(uint256 newFee) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 256](src/morph-contracts/MetaMorpho.sol#L256)

	```solidity
	    function setFeeRecipient(address newFeeRecipient) external onlyOwner {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 270](src/morph-contracts/MetaMorpho.sol#L270)

	```solidity
	    function submitGuardian(address newGuardian) external onlyOwner {
	```

</details>



## L-2: Solidity pragma should be specific, not wide

Consider using a specific version of Solidity in your contracts instead of a wide version. For example, instead of `pragma solidity ^0.8.0;`, use `pragma solidity 0.8.0;`

<details><summary>14 Found Instances</summary>


- Found in src/Counter.sol [Line: 2](src/Counter.sol#L2)

	```solidity
	pragma solidity ^0.8.13;
	```

- Found in src/DeployMetaMorpho.s.sol [Line: 2](src/DeployMetaMorpho.s.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/EchidnaMorphoTest.sol [Line: 2](src/EchidnaMorphoTest.sol#L2)

	```solidity
	pragma solidity ^0.8.7;
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 2](src/morph-contracts/MetaMorpho.sol#L2)

	```solidity
	pragma solidity ^0.8.21;
	```

- Found in src/morph-contracts/MetaMorphoFactory.sol [Line: 2](src/morph-contracts/MetaMorphoFactory.sol#L2)

	```solidity
	pragma solidity ^0.8.21;
	```

- Found in src/morph-contracts/interfaces/IMetaMorpho.sol [Line: 2](src/morph-contracts/interfaces/IMetaMorpho.sol#L2)

	```solidity
	pragma solidity >=0.5.0;
	```

- Found in src/morph-contracts/interfaces/IMetaMorphoFactory.sol [Line: 2](src/morph-contracts/interfaces/IMetaMorphoFactory.sol#L2)

	```solidity
	pragma solidity >=0.5.0;
	```

- Found in src/morph-contracts/libraries/ConstantsLib.sol [Line: 2](src/morph-contracts/libraries/ConstantsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/ErrorsLib.sol [Line: 2](src/morph-contracts/libraries/ErrorsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 2](src/morph-contracts/libraries/EventsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/PendingLib.sol [Line: 2](src/morph-contracts/libraries/PendingLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/ERC20Mock.sol [Line: 2](src/morph-contracts/mocks/ERC20Mock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/IrmMock.sol [Line: 2](src/morph-contracts/mocks/IrmMock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/OracleMock.sol [Line: 2](src/morph-contracts/mocks/OracleMock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

</details>



## L-3: Missing checks for `address(0)` when assigning values to address state variables

Check for `address(0)` when assigning values to address state variables.

<details><summary>1 Found Instances</summary>


- Found in src/morph-contracts/MetaMorpho.sol [Line: 891](src/morph-contracts/MetaMorpho.sol#L891)

	```solidity
	        guardian = newGuardian;
	```

</details>



## L-4: `public` functions not used internally could be marked `external`

Instead of marking a function as `public`, consider marking it as `external` if it is not used internally.

<details><summary>12 Found Instances</summary>


- Found in src/Counter.sol [Line: 8](src/Counter.sol#L8)

	```solidity
	    function increment() public {
	```

- Found in src/Counter.sol [Line: 14](src/Counter.sol#L14)

	```solidity
	    function setNumber(uint256 newNumber) public {
	```

- Found in src/EchidnaMorphoTest.sol [Line: 71](src/EchidnaMorphoTest.sol#L71)

	```solidity
	    function echidna_reallocate(
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 554](src/morph-contracts/MetaMorpho.sol#L554)

	```solidity
	    function decimals() public view override(ERC20, ERC4626) returns (uint8) {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 560](src/morph-contracts/MetaMorpho.sol#L560)

	```solidity
	    function maxDeposit(address) public view override returns (uint256) {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 566](src/morph-contracts/MetaMorpho.sol#L566)

	```solidity
	    function maxMint(address) public view override returns (uint256) {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 575](src/morph-contracts/MetaMorpho.sol#L575)

	```solidity
	    function maxWithdraw(
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 584](src/morph-contracts/MetaMorpho.sol#L584)

	```solidity
	    function maxRedeem(address owner) public view override returns (uint256) {
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 601](src/morph-contracts/MetaMorpho.sol#L601)

	```solidity
	    function deposit(
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 622](src/morph-contracts/MetaMorpho.sol#L622)

	```solidity
	    function mint(
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 643](src/morph-contracts/MetaMorpho.sol#L643)

	```solidity
	    function withdraw(
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 666](src/morph-contracts/MetaMorpho.sol#L666)

	```solidity
	    function redeem(
	```

</details>



## L-5: Define and use `constant` variables instead of using literals

If the same constant literal value is used multiple times, create a constant state variable and reference it throughout the contract.

<details><summary>6 Found Instances</summary>


- Found in src/EchidnaMorphoTest.sol [Line: 45](src/EchidnaMorphoTest.sol#L45)

	```solidity
	                oracle: address(uint160((seed % 100) + 1)),
	```

- Found in src/EchidnaMorphoTest.sol [Line: 46](src/EchidnaMorphoTest.sol#L46)

	```solidity
	                irm: address(uint160((seed % 100) + 101)),
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 458](src/morph-contracts/MetaMorpho.sol#L458)

	```solidity
	                    hex""
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 792](src/morph-contracts/MetaMorpho.sol#L792)

	```solidity
	                newTotalSupply + 10 ** _decimalsOffset(),
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 809](src/morph-contracts/MetaMorpho.sol#L809)

	```solidity
	                newTotalSupply + 10 ** _decimalsOffset(),
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 970](src/morph-contracts/MetaMorpho.sol#L970)

	```solidity
	                        hex""
	```

</details>



## L-6: Event is missing `indexed` fields

Index event fields make the field more quickly accessible to off-chain tools that parse events. However, note that each index field costs extra gas during emission, so it's not necessarily best to index the maximum allowed per event (three fields). Each event should use three indexed fields if there are three or more fields, and gas usage is not particularly of concern for the events in question. If there are fewer than three fields, all of the fields should be indexed.

<details><summary>13 Found Instances</summary>


- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 14](src/morph-contracts/libraries/EventsLib.sol#L14)

	```solidity
	    event SubmitTimelock(uint256 newTimelock);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 17](src/morph-contracts/libraries/EventsLib.sol#L17)

	```solidity
	    event SetTimelock(address indexed caller, uint256 newTimelock);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 23](src/morph-contracts/libraries/EventsLib.sol#L23)

	```solidity
	    event SetFee(address indexed caller, uint256 newFee);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 35](src/morph-contracts/libraries/EventsLib.sol#L35)

	```solidity
	    event SubmitCap(address indexed caller, Id indexed id, uint256 cap);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 38](src/morph-contracts/libraries/EventsLib.sol#L38)

	```solidity
	    event SetCap(address indexed caller, Id indexed id, uint256 cap);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 41](src/morph-contracts/libraries/EventsLib.sol#L41)

	```solidity
	    event UpdateLastTotalAssets(uint256 updatedTotalAssets);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 50](src/morph-contracts/libraries/EventsLib.sol#L50)

	```solidity
	    event SetIsAllocator(address indexed allocator, bool isAllocator);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 65](src/morph-contracts/libraries/EventsLib.sol#L65)

	```solidity
	    event SetSupplyQueue(address indexed caller, Id[] newSupplyQueue);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 68](src/morph-contracts/libraries/EventsLib.sol#L68)

	```solidity
	    event SetWithdrawQueue(address indexed caller, Id[] newWithdrawQueue);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 74](src/morph-contracts/libraries/EventsLib.sol#L74)

	```solidity
	    event ReallocateSupply(
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 85](src/morph-contracts/libraries/EventsLib.sol#L85)

	```solidity
	    event ReallocateWithdraw(
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 95](src/morph-contracts/libraries/EventsLib.sol#L95)

	```solidity
	    event AccrueInterest(uint256 newTotalAssets, uint256 feeShares);
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 98](src/morph-contracts/libraries/EventsLib.sol#L98)

	```solidity
	    event Skim(address indexed caller, address indexed token, uint256 amount);
	```

</details>



## L-7: PUSH0 is not supported by all chains

Solc compiler version 0.8.20 switches the default target EVM version to Shanghai, which means that the generated bytecode will include PUSH0 opcodes. Be sure to select the appropriate EVM version in case you intend to deploy on a chain other than mainnet like L2 chains that may not support PUSH0, otherwise deployment of your contracts will fail.

<details><summary>14 Found Instances</summary>


- Found in src/Counter.sol [Line: 2](src/Counter.sol#L2)

	```solidity
	pragma solidity ^0.8.13;
	```

- Found in src/DeployMetaMorpho.s.sol [Line: 2](src/DeployMetaMorpho.s.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/EchidnaMorphoTest.sol [Line: 2](src/EchidnaMorphoTest.sol#L2)

	```solidity
	pragma solidity ^0.8.7;
	```

- Found in src/morph-contracts/MetaMorpho.sol [Line: 2](src/morph-contracts/MetaMorpho.sol#L2)

	```solidity
	pragma solidity ^0.8.21;
	```

- Found in src/morph-contracts/MetaMorphoFactory.sol [Line: 2](src/morph-contracts/MetaMorphoFactory.sol#L2)

	```solidity
	pragma solidity ^0.8.21;
	```

- Found in src/morph-contracts/interfaces/IMetaMorpho.sol [Line: 2](src/morph-contracts/interfaces/IMetaMorpho.sol#L2)

	```solidity
	pragma solidity >=0.5.0;
	```

- Found in src/morph-contracts/interfaces/IMetaMorphoFactory.sol [Line: 2](src/morph-contracts/interfaces/IMetaMorphoFactory.sol#L2)

	```solidity
	pragma solidity >=0.5.0;
	```

- Found in src/morph-contracts/libraries/ConstantsLib.sol [Line: 2](src/morph-contracts/libraries/ConstantsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/ErrorsLib.sol [Line: 2](src/morph-contracts/libraries/ErrorsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/EventsLib.sol [Line: 2](src/morph-contracts/libraries/EventsLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/libraries/PendingLib.sol [Line: 2](src/morph-contracts/libraries/PendingLib.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/ERC20Mock.sol [Line: 2](src/morph-contracts/mocks/ERC20Mock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/IrmMock.sol [Line: 2](src/morph-contracts/mocks/IrmMock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

- Found in src/morph-contracts/mocks/OracleMock.sol [Line: 2](src/morph-contracts/mocks/OracleMock.sol#L2)

	```solidity
	pragma solidity ^0.8.0;
	```

</details>



## L-8: Internal functions called only once can be inlined

Instead of separating the logic into a separate function, consider inlining the logic into the calling function. This can reduce the number of function calls and improve readability.

<details><summary>2 Found Instances</summary>


- Found in src/EchidnaMorphoTest.sol [Line: 38](src/EchidnaMorphoTest.sol#L38)

	```solidity
	    function generateMarketParams(
	```

- Found in src/EchidnaMorphoTest.sol [Line: 52](src/EchidnaMorphoTest.sol#L52)

	```solidity
	    function generateAllocations(
	```

</details>



