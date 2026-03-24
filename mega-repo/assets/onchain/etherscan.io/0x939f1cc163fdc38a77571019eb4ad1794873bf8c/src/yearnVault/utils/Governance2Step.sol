
// SPDX-License-Identifier: GNU AGPLv3
pragma solidity >=0.8.18;


contract Governance {
    /// @notice Emitted when the governance address is updated.
    event GovernanceTransferred(
        address indexed previousGovernance,
        address indexed newGovernance
    );

    modifier onlyGovernance() {
        _checkGovernance();
        _;
    }

    /// @notice Checks if the msg sender is the governance.
    function _checkGovernance() internal view virtual {
        require(governance == msg.sender, "!governance");
    }

    /// @notice Address that can set the default base fee and provider
    address public governance;

    constructor(address _governance) {
        governance = _governance;

        emit GovernanceTransferred(address(0), _governance);
    }

    /**
     * @notice Sets a new address as the governance of the contract.
     * @dev Throws if the caller is not current governance.
     * @param _newGovernance The new governance address.
     */
    function transferGovernance(
        address _newGovernance
    ) external virtual onlyGovernance {
        require(_newGovernance != address(0), "ZERO ADDRESS");
        address oldGovernance = governance;
        governance = _newGovernance;

        emit GovernanceTransferred(oldGovernance, _newGovernance);
    }
}

contract Governance2Step is Governance {
    /// @notice Emitted when the pending governance address is set.
    event UpdatePendingGovernance(address indexed newPendingGovernance);

    /// @notice Address that is set to take over governance.
    address public pendingGovernance;

    constructor(address _governance) Governance(_governance) {}

    /**
     * @notice Sets a new address as the `pendingGovernance` of the contract.
     * @dev Throws if the caller is not current governance.
     * @param _newGovernance The new governance address.
     */
    function transferGovernance(
        address _newGovernance
    ) external virtual override onlyGovernance {
        require(_newGovernance != address(0), "ZERO ADDRESS");
        pendingGovernance = _newGovernance;

        emit UpdatePendingGovernance(_newGovernance);
    }

    /**
     * @notice Allows the `pendingGovernance` to accept the role.
     */
    function acceptGovernance() external virtual {
        require(msg.sender == pendingGovernance, "!pending governance");

        emit GovernanceTransferred(governance, msg.sender);

        governance = msg.sender;
        pendingGovernance = address(0);
    }
}