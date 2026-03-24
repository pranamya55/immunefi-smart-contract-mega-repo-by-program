// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IICNRegistryStorage} from "./interfaces/IICNRegistryStorage.sol";

import {EraManagerStorage} from "../EraManager/EraManagerStorage.sol";

import {ProtocolConstants} from "../../common/ProtocolConstants.sol";

contract ICNRegistryStorage is IICNRegistryStorage, EraManagerStorage {
    /// @custom:storage-location erc7201:registry.storage
    struct ICNRegistryStorageData {
        uint64 version;
        uint256 _scalerNodeIdCounter;
        uint256 _hyperNodeIdCounter;
        uint256 _hpIdCounter;
        address foundationAddress;
        uint256 minCollateralPercent;
        uint256 marketAdjustmentFactor; // Must be a fixed point number
        mapping(string => Region) regions;
        mapping(string => Cluster) clusters;
        mapping(uint256 => HP) hps;
        mapping(uint256 => ScalerNode) scalerNodes;
        mapping(uint256 => HyperNode) hyperNodes;
        /// @dev DEPRECATED in v5.0.3: sps are now identified by uint256, should not be used anymore
        mapping(address => bool) sps;
        /// @dev DEPRECATED in v5.0.3: hps are now identified by uint256, should not be used anymore
        mapping(address => bool) hpAccounts;
        string[] regionIds;
        mapping(uint256 => uint256) grantedCollateral;
        mapping(address => bool) registeredPublicKeys;
        uint256 _spIdCounter;
        mapping(uint256 => SP) spInfos;
        mapping(address => uint256) hpAccountsIds;
        mapping(address => uint256) spAccountsIds;
        uint64 versionGetters;
        mapping(string => mapping(string => uint256)) protocolMargin; // regionId => hwClass => protocolMargin
    }

    // keccak256(abi.encode(uint256(keccak256("icnregistry.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant ICN_REGISTRY_STORAGE_SLOT = 0xe32462c3d0235542581986c483958675ee491e3e4515282b8d0df00d74e47200;
    uint256 internal constant MAX_NODE_NAME_LENGTH = 30;

    modifier hasRegionAndHwClass(string memory regionId, string memory hwClass) {
        require(bytes(regionId).length != 0, InvalidRegion());
        require(bytes(hwClass).length != 0, InvalidHwClass());
        ICNRegistryStorageData storage ds = getICNRegistryStorage();
        require(ds.regions[regionId].status, InvalidRegion());
        require(ds.regions[regionId].hwClasses[hwClass].creationDate != 0, InvalidHwClass());
        _;
    }

    function _registerBooking(uint256 scalerNodeId, uint256 capacity, uint256 spId, uint256 bookingPriceNoMargin, uint256 period)
        internal
    {
        ICNRegistryStorageData storage $ = getICNRegistryStorage();
        ICNRegistryStorage.ScalerNode storage scalerNode = $.scalerNodes[scalerNodeId];
        require(scalerNode.utilizedCapacity == 0, UtilizedCapacityNotNull());

        $.regions[$.clusters[scalerNode.clusterId].regionId].hwClasses[scalerNode.hwClass].utilizedCapacity += capacity;
        $.clusters[scalerNode.clusterId].utilizedCapacity += capacity;
        $.hps[scalerNode.hpId].utilizedCapacity += capacity;

        // Set the utilized capacity, spId and activation era of the scaler node to mark it as booked
        scalerNode.utilizedCapacity = capacity;
        scalerNode.spId = spId;
        scalerNode.activationEra = _getEraManagerCurrentEra() + 1;

        // This function can only be called if the utilized capacity is 0, which means that this is either the first booking
        // or expireCapacity has been called before, which ensures that firstBooking and secondBooking are null
        scalerNode.bookings[0] =
            Booking({bookingPrice: bookingPriceNoMargin, startBookingPeriod: block.timestamp, bookingPeriod: period});
    }

    function _eraseBooking(uint256 scalerNodeId, uint256 expiredCapacity) internal {
        ICNRegistryStorageData storage $ = getICNRegistryStorage();
        ICNRegistryStorage.ScalerNode storage scalerNode = $.scalerNodes[scalerNodeId];

        // Update global state
        $.regions[$.clusters[scalerNode.clusterId].regionId].hwClasses[scalerNode.hwClass].utilizedCapacity -= expiredCapacity;
        $.clusters[scalerNode.clusterId].utilizedCapacity -= expiredCapacity;
        $.hps[scalerNode.hpId].utilizedCapacity -= expiredCapacity;

        // Update scaler node state
        delete scalerNode.utilizedCapacity;
        delete scalerNode.spId;
        delete scalerNode.activationEra;
        delete scalerNode.bookings[0];
        delete scalerNode.bookings[1];
    }

    function _getMarketAdjustedAmount(uint256 amount) internal view returns (uint256 marketAdjustedAmount) {
        ICNRegistryStorageData storage $ = getICNRegistryStorage();
        return amount * $.marketAdjustmentFactor;
    }

    function _requiredNodeCollateralAmount(
        ICNRegistryStorageData storage ds,
        string memory regionId,
        string memory hwClass,
        uint256 capacity
    ) internal view returns (uint256) {
        return _getMarketAdjustedAmount(ds.regions[regionId].hwClasses[hwClass].collateralReq) * capacity
            * ds.minCollateralPercent / ProtocolConstants.ONE_HUNDRED_PERCENT;
    }

    function _checkNodeCollateralAmount(
        ICNRegistryStorageData storage ds,
        string memory regionId,
        string memory hwClass,
        uint256 capacity,
        uint256 collateralAmount
    ) internal view returns (bool) {
        return collateralAmount * ProtocolConstants.DEFAULT_PRECISION
            >= _requiredNodeCollateralAmount(ds, regionId, hwClass, capacity);
    }

    function getICNRegistryStorage() internal pure returns (ICNRegistryStorageData storage $) {
        bytes32 slot = ICN_REGISTRY_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
