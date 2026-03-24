#!/usr/bin/env bash
echo "Starting to flatten our contracts"
node_modules/.bin/truffle-flattener contracts/MocMedianizer.sol > scripts/contract_flatten/MocMedianizer_flat.sol
echo "Finish successfully! Take a look in folder scripts/contract_flatten/..."