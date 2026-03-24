// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IICNRegistryErrors} from "./IICNRegistryErrors.sol";

interface IICNRegistryStorage is IICNRegistryErrors {
    struct HWClass {
        uint256 creationDate;
        uint256 collateralReq;
        uint256 targetCapacity;
        uint256 totalCapacity;
        uint256 utilizedCapacity;
        uint256 releaseSchedule; // must not be a fixed point number
        uint256 maximumBootstrapRelease; // must not be a fixed point number
    }

    struct Region {
        bool status;
        uint256 creationDate;
        string[] hwClassIds;
        mapping(string hwClass => HWClass) hwClasses;
    }

    struct Cluster {
        bool status;
        uint256 creationDate;
        uint256 totalCapacity;
        uint256 utilizedCapacity;
        string regionId;
        uint256 maxPrice;
        string hwClass;
        uint256[] scalerNodeIds;
        mapping(uint256 => uint256) scalerNodeIndexes;
    }

    struct HP {
        bool status;
        address account;
        uint256 totalCapacity;
        uint256 utilizedCapacity;
    }

    struct Booking {
        uint256 bookingPrice;
        uint256 startBookingPeriod;
        uint256 bookingPeriod;
    }

    struct SP {
        bool status;
        address account;
    }

    struct ScalerNode {
        ScalerNodeStatus status;
        uint256 creationDate;
        string name;
        uint256 totalCapacity;
        uint256 utilizedCapacity;
        uint256 hpId;
        LocationCode location;
        string clusterId;
        uint256 reservationPrice;
        /// @dev DEPRECATED in v5.0.3: use `bookings[i].bookingPrice` instead, should not be used anymore
        uint256 bookingPrice;
        uint256 nodeRewardShare;
        string hwClass;
        address daemonAddress;
        uint256 collateralAmount;
        uint256 commitmentDuration;
        uint256 commitmentStart;
        /// @dev DEPRECATED in v5.0.3: use `spId` instead, should not be used anymore
        address spIdUnused;
        uint256 activationEra;
        /// @dev DEPRECATED in v5.0.3: use `bookings[i].startBookingPeriod` instead, should not be used anymore
        uint256 startBookingPeriod;
        /// @dev DEPRECATED in v5.0.3: use `bookings[i].bookingPeriod` instead, should not be used anymore
        uint256 bookingPeriod;
        Booking[2] bookings;
        uint256 spId;
    }

    struct HyperNode {
        bool status;
        address operator;
        address publicKey;
        LocationCode location;
    }

    struct ScalerNodeRegistrationParams {
        string regionId;
        string name;
        uint256 hpId;
        uint256 capacity;
        LocationCode location;
        uint256 reservationPrice;
        string hwClass;
        uint256 nodeRewardShare;
        uint256 collateralAmount;
        uint256 commitmentDuration;
    }

    enum ScalerNodeStatus {
        None,
        Registered,
        Validated,
        Rejected
    }

    enum ProtocolScalerNodeStatus {
        None,
        Registered,
        Active,
        Booked,
        Offboarded
    }

    enum LocationCode {
        AFG,
        ALA,
        ALB,
        DZA,
        ASM,
        AND,
        AGO,
        AIA,
        ATA,
        ATG,
        ARG,
        ARM,
        ABW,
        AUS,
        AUT,
        AZE,
        BHS,
        BHR,
        BGD,
        BRB,
        BLR,
        BEL,
        BLZ,
        BEN,
        BMU,
        BTN,
        BOL,
        BES,
        BIH,
        BWA,
        BVT,
        BRA,
        IOT,
        BRN,
        BGR,
        BFA,
        BDI,
        CPV,
        KHM,
        CMR,
        CAN,
        CYM,
        CAF,
        TCD,
        CHL,
        CHN,
        CXR,
        CCK,
        COL,
        COM,
        COG,
        COD,
        COK,
        CRI,
        CIV,
        HRV,
        CUB,
        CUW,
        CYP,
        CZE,
        DNK,
        DJI,
        DMA,
        DOM,
        ECU,
        EGY,
        SLV,
        GNQ,
        ERI,
        EST,
        SWZ,
        ETH,
        FLK,
        FRO,
        FJI,
        FIN,
        FRA,
        GUF,
        PYF,
        ATF,
        GAB,
        GMB,
        GEO,
        DEU,
        GHA,
        GIB,
        GRC,
        GRL,
        GRD,
        GLP,
        GUM,
        GTM,
        GGY,
        GIN,
        GNB,
        GUY,
        HTI,
        HMD,
        VAT,
        HND,
        HKG,
        HUN,
        ISL,
        IND,
        IDN,
        IRN,
        IRQ,
        IRL,
        IMN,
        ISR,
        ITA,
        JAM,
        JPN,
        JEY,
        JOR,
        KAZ,
        KEN,
        KIR,
        PRK,
        KOR,
        KWT,
        KGZ,
        LAO,
        LVA,
        LBN,
        LSO,
        LBR,
        LBY,
        LIE,
        LTU,
        LUX,
        MAC,
        MDG,
        MWI,
        MYS,
        MDV,
        MLI,
        MLT,
        MHL,
        MTQ,
        MRT,
        MUS,
        MYT,
        MEX,
        FSM,
        MDA,
        MCO,
        MNG,
        MNE,
        MSR,
        MAR,
        MOZ,
        MMR,
        NAM,
        NRU,
        NPL,
        NLD,
        NCL,
        NZL,
        NIC,
        NER,
        NGA,
        NIU,
        NFK,
        MKD,
        MNP,
        NOR,
        OMN,
        PAK,
        PLW,
        PSE,
        PAN,
        PNG,
        PRY,
        PER,
        PHL,
        PCN,
        POL,
        PRT,
        PRI,
        QAT,
        REU,
        ROU,
        RUS,
        RWA,
        BLM,
        SHN,
        KNA,
        LCA,
        MAF,
        SPM,
        VCT,
        WSM,
        SMR,
        STP,
        SAU,
        SEN,
        SRB,
        SYC,
        SLE,
        SGP,
        SXM,
        SVK,
        SVN,
        SLB,
        SOM,
        ZAF,
        SGS,
        SSD,
        ESP,
        LKA,
        SDN,
        SUR,
        SJM,
        SWE,
        CHE,
        SYR,
        TWN,
        TJK,
        TZA,
        THA,
        TLS,
        TGO,
        TKL,
        TON,
        TTO,
        TUN,
        TUR,
        TKM,
        TCA,
        TUV,
        UGA,
        UKR,
        ARE,
        GBR,
        USA,
        UMI,
        URY,
        UZB,
        VUT,
        VEN,
        VNM,
        VGB,
        VIR,
        WLF,
        ESH,
        YEM,
        ZMB,
        ZWE
    }
}
