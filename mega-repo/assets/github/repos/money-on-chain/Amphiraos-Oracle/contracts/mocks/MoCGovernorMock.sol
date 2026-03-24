pragma solidity ^0.4.23;

/**
* @dev MoC Governor interface
 */
contract MoCGovernorMock {
  
  address owner;

  constructor() public {
    owner = msg.sender;
  }

  function isAuthorizedChanger(address user) external view returns(bool) {
    return user == owner;
  }
}