// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

interface IAuction {
    function getReserves() external view returns (uint dolaReserve, uint dbrReserve);
    function buyDbr(uint exactDolaIn, uint exactDbrOut, address to) external;
}

interface IERC20 {
    function approve(address,uint) external returns (bool);
    function transferFrom(address,address,uint) external returns (bool);
}

interface IERC4626 is IERC20 {
    function deposit(uint assets, address receiver) external returns(uint shares);
}

contract Helper {

    IAuction public immutable auction;
    IERC20 public immutable dola;
    IERC4626 public immutable sdola;

    constructor(
        address _auction,
        address _dola,
        address _sdola
    ) {
        auction = IAuction(_auction);
        dola = IERC20(_dola);
        sdola = IERC4626(_sdola);
        sdola.approve(_auction, type(uint).max);
    }
    
    function getDbrOut(uint sdolaIn) public view returns (uint dbrOut) {
        require(sdolaIn > 0, "sdolaIn must be positive");
        (uint sdolaReserve, uint dbrReserve) = auction.getReserves();
        uint numerator = sdolaIn * dbrReserve;
        uint denominator = sdolaReserve + sdolaIn;
        dbrOut = numerator / denominator;
    }

    function getsDolaIn(uint dbrOut) public view returns (uint sdolaIn) {
        require(dbrOut > 0, "dbrOut must be positive");
        (uint sdolaReserve, uint dbrReserve) = auction.getReserves();
        uint numerator = dbrOut * sdolaReserve;
        uint denominator = dbrReserve - dbrOut;
        sdolaIn = (numerator / denominator) + 1;
    }

    function depositDola(uint dolaAmount, uint minSharesOut) external returns (uint jrDolaOut) {
        dola.transferFrom(msg.sender, address(this), dolaAmount);
        dola.approve(address(sdola), dolaAmount);
        uint sDolaShares = sdola.deposit(dolaAmount, address(this));
        sdola.approve(address(auction), sDolaShares);
        jrDolaOut = IERC4626(address(auction)).deposit(sDolaShares, msg.sender);
        require(jrDolaOut >= minSharesOut, "Not enough jrDola shares received");
    }

    function swapExactsDolaForDbr(uint sdolaIn, uint dbrOutMin) external returns (uint dbrOut) {
        dbrOut = getDbrOut(sdolaIn);
        require(dbrOut >= dbrOutMin, "dbrOut must be greater than dbrOutMin");
        sdola.transferFrom(msg.sender, address(this), sdolaIn);
        auction.buyDbr(sdolaIn, dbrOut, msg.sender);
    }

    function swapsDolaForExactDbr(uint dbrOut, uint sdolaInMax) external returns (uint sdolaIn) {
        sdolaIn = getsDolaIn(dbrOut);
        require(sdolaIn <= sdolaInMax, "sdolaIn must be less than sdolaInMax");
        sdola.transferFrom(msg.sender, address(this), sdolaIn);
        auction.buyDbr(sdolaIn, dbrOut, msg.sender);
    }

}