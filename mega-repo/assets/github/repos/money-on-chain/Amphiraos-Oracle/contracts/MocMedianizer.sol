pragma solidity ^0.4.24;

import "./medianizer/medianizer.sol";

contract MoCMedianizer is Medianizer {
  constructor() public Medianizer() {
  }
}