pragma solidity ^0.4.23;

/**
* @dev MoC Governor interface
 */
interface MoCGovernor {
  function isAuthorizedChanger(address user) external view returns(bool);
}

contract DSAuthority {
    function canCall(
        address src, address dst, bytes4 sig
    ) public view returns (bool);
}

/**
* @dev MoC governance implementing DSAuthority for Dappsys Auth
* https://github.com/dapphub/ds-auth
*/
contract MoCGovernedAuthority is DSAuthority{
  MoCGovernor public governor;

  constructor(address governorAddress) public {
    governor = MoCGovernor(governorAddress);
  }

  // Second and third parameters not used
  // only to comply DSAuthority Interface
  function canCall(address user, address, bytes4) public view returns (bool) {
    return governor.isAuthorizedChanger(user);
  }
}
