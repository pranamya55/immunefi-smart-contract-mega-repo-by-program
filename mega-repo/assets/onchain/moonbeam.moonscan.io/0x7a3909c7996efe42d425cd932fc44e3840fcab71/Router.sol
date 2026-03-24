// File: contracts/core/interfaces/IFactory.sol



pragma solidity >=0.8.0;

interface IFactory {
    event PairCreated(
        address indexed token0,
        address indexed token1,
        address pair,
        uint256
    );
    event PairCreateLocked(
        address indexed caller
    );
    event PairCreateUnlocked(
        address indexed caller
    );
    event BootstrapSetted(
        address indexed tokenA,
        address indexed tokenB,
        address indexed bootstrap
    );
    event FeetoUpdated(
        address indexed feeto
    );
    event FeeBasePointUpdated(
        uint8 basePoint
    );

    function feeto() external view returns (address);

    function feeBasePoint() external view returns (uint8);

    function lockForPairCreate() external view returns (bool);

    function getPair(address tokenA, address tokenB)
        external
        view
        returns (address pair);
    
    function getBootstrap(address tokenA, address tokenB)
        external
        view
        returns (address bootstrap);

    function allPairs(uint256) external view returns (address pair);

    function allPairsLength() external view returns (uint256);

    function createPair(address tokenA, address tokenB)
        external
        returns (address pair);
}

// File: contracts/core/interfaces/IPair.sol



pragma solidity >=0.8.0;

interface IPair {
    event Mint(address indexed sender, uint256 amount0, uint256 amount1);
    event Burn(
        address indexed sender,
        uint256 amount0,
        uint256 amount1,
        address indexed to
    );
    event Swap(
        address indexed sender,
        uint256 amount0In,
        uint256 amount1In,
        uint256 amount0Out,
        uint256 amount1Out,
        address indexed to
    );

    event Sync(uint112 reserve0, uint112 reserve1);

    function MINIMUM_LIQUIDITY() external pure returns (uint256);

    function factory() external view returns (address);

    function token0() external view returns (address);

    function token1() external view returns (address);

    function getReserves()
        external
        view
        returns (uint112 reserve0, uint112 reserve1);

    function mint(address to) external returns (uint256 liquidity);

    function burn(address to)
        external
        returns (uint256 amount0, uint256 amount1);

    function swap(
        uint256 amount0Out,
        uint256 amount1Out,
        address to
    ) external;

    function initialize(address, address) external;
}

// File: contracts/libraries/Math.sol



pragma solidity >=0.8.0;

// a library for performing various math operations

library Math {
    function min(uint256 x, uint256 y) internal pure returns (uint256 z) {
        z = x < y ? x : y;
    }

    // babylonian method (https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method)
    function sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }

    function add(uint256 x, uint256 y) internal pure returns (uint256 z) {
        require((z = x + y) >= x, "ds-math-add-overflow");
    }

    function sub(uint256 x, uint256 y) internal pure returns (uint256 z) {
        require((z = x - y) <= x, "ds-math-sub-underflow");
    }

    function mul(uint256 x, uint256 y) internal pure returns (uint256 z) {
        require(y == 0 || (z = x * y) / y == x, "ds-math-mul-overflow");
    }
}

// File: contracts/libraries/Helper.sol



pragma solidity >=0.8.0;




library Helper {
    using Math for uint256;

    function sortTokens(address tokenA, address tokenB)
        internal
        pure
        returns (address token0, address token1)
    {
        require(tokenA != tokenB, "Helper: IDENTICAL_ADDRESSES");
        (token0, token1) = tokenA < tokenB
            ? (tokenA, tokenB)
            : (tokenB, tokenA);
        require(token0 != address(0), "Helper: ZERO_ADDRESS");
    }

    function pairFor(
        address factory,
        address tokenA,
        address tokenB
    ) internal view returns (address pair) {
        return IFactory(factory).getPair(tokenA, tokenB);
    }

    function quote(
        uint256 amountA,
        uint256 reserveA,
        uint256 reserveB
    ) internal pure returns (uint256 amountB) {
        require(amountA > 0, "INSUFFICIENT_AMOUNT");
        require(reserveA > 0 && reserveB > 0, "INSUFFICIENT_LIQUIDITY");
        amountB = amountA.mul(reserveB) / reserveA;
    }

    function getReserves(
        address factory,
        address tokenA,
        address tokenB
    ) internal view returns (uint256 reserveA, uint256 reserveB) {
        (address token0, ) = sortTokens(tokenA, tokenB);
        (uint256 reserve0, uint256 reserve1) = IPair(
            pairFor(factory, tokenA, tokenB)
        ).getReserves();
        (reserveA, reserveB) = tokenA == token0
            ? (reserve0, reserve1)
            : (reserve1, reserve0);
    }

    function safeTransferFrom(
        address token,
        address from,
        address to,
        uint256 value
    ) internal {
        // bytes4(keccak256(bytes('transferFrom(address,address,uint256)')));
        (bool success, bytes memory data) = token.call(
            abi.encodeWithSelector(0x23b872dd, from, to, value)
        );
        require(
            success && (data.length == 0 || abi.decode(data, (bool))),
            "TransferHelper::transferFrom: transferFrom failed"
        );
    }

    function safeTransfer(
        address token,
        address to,
        uint256 value
    ) internal {
        // bytes4(keccak256(bytes('transfer(address,uint256)')));
        (bool success, bytes memory data) = token.call(
            abi.encodeWithSelector(0xa9059cbb, to, value)
        );
        require(
            success && (data.length == 0 || abi.decode(data, (bool))),
            "TransferHelper::safeTransfer: transfer failed"
        );
    }

    function safeTransferNativeCurrency(address to, uint256 value) internal {
        (bool success, ) = to.call{value: value}(new bytes(0));
        require(
            success,
            "TransferHelper::safeTransferNativeCurrency: NativeCurrency transfer failed"
        );
    }

    // given an input amount of an asset and pair reserves, returns the maximum output amount of the other asset
    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) internal pure returns (uint256 amountOut) {
        require(amountIn > 0, "Helper: INSUFFICIENT_INPUT_AMOUNT");
        require(
            reserveIn > 0 && reserveOut > 0,
            "Helper: INSUFFICIENT_LIQUIDITY"
        );
        uint256 amountInWithFee = amountIn.mul(997);
        uint256 numerator = amountInWithFee.mul(reserveOut);
        uint256 denominator = reserveIn.mul(1000).add(amountInWithFee);
        amountOut = numerator / denominator;
    }

    // given an output amount of an asset and pair reserves, returns a required input amount of the other asset
    function getAmountIn(
        uint256 amountOut,
        uint256 reserveIn,
        uint256 reserveOut
    ) internal pure returns (uint256 amountIn) {
        require(amountOut > 0, "Helper: INSUFFICIENT_OUTPUT_AMOUNT");
        require(
            reserveIn > 0 && reserveOut > 0,
            "Helper: INSUFFICIENT_LIQUIDITY"
        );
        uint256 numerator = reserveIn.mul(amountOut).mul(1000);
        uint256 denominator = reserveOut.sub(amountOut).mul(997);
        amountIn = (numerator / denominator).add(1);
    }

    // performs chained getAmountOut calculations on any number of pairs
    function getAmountsOut(
        address factory,
        uint256 amountIn,
        address[] memory path
    ) internal view returns (uint256[] memory amounts) {
        require(path.length >= 2, "Helper: INVALID_PATH");
        amounts = new uint256[](path.length);
        amounts[0] = amountIn;
        for (uint256 i; i < path.length - 1; i++) {
            (uint256 reserveIn, uint256 reserveOut) = getReserves(
                factory,
                path[i],
                path[i + 1]
            );
            amounts[i + 1] = getAmountOut(amounts[i], reserveIn, reserveOut);
        }
    }

    function getAmountsIn(
        address factory,
        uint256 amountOut,
        address[] memory path
    ) internal view returns (uint256[] memory amounts) {
        require(path.length >= 2, "Helper: INVALID_PATH");
        amounts = new uint256[](path.length);
        amounts[amounts.length - 1] = amountOut;
        for (uint256 i = path.length - 1; i > 0; i--) {
            (uint256 reserveIn, uint256 reserveOut) = getReserves(
                factory,
                path[i - 1],
                path[i]
            );
            amounts[i - 1] = getAmountIn(amounts[i], reserveIn, reserveOut);
        }
    }
}

// File: contracts/periphery/interfaces/IWNativeCurrency.sol



pragma solidity >=0.8.0;

interface IWNativeCurrency {
    function deposit() external payable;

    function withdraw(uint256) external;
}

// File: contracts/periphery/interfaces/IRouter.sol



pragma solidity >=0.8.0;

interface IRouter {
    function factory() external view returns (address);

    function WNativeCurrency() external view returns (address);

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountADesired,
        uint256 amountBDesired,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    )
        external
        returns (
            uint256 amountA,
            uint256 amountB,
            uint256 liquidity
        );

    function addLiquiditySingleToken(
        address[] calldata path,
        uint256 amountIn,
        uint256 amountSwapIn,
        uint256 amountSwapOutMin,
        uint256 amountInReserveMin,
        address to,
        uint256 deadline
    )
        external
        returns (
            uint256 liquidity
        );

    function addLiquidityNativeCurrency(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountNativeCurrencyMin,
        address to,
        uint256 deadline
    )
        external
        payable
        returns (
            uint256 amountToken,
            uint256 amountNativeCurrency,
            uint256 liquidity
        );

    function addLiquiditySingleNativeCurrency(
        address[] calldata path,
        uint256 amountSwapOut,
        uint256 nativeCurrencySwapInMax,
        uint256 nativeCurrencyReserveMin,
        address to,
        uint256 deadline
    )
        external
        payable
        returns (
            uint256 amountToken,
            uint256 amountNativeCurrency,
            uint256 liquidity
        );

    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint256 liquidity,
        uint256 amountAMin,
        uint256 amountBMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountA, uint256 amountB);

    function removeLiquidityNativeCurrency(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountNativeCurrencyMin,
        address to,
        uint256 deadline
    ) external returns (uint256 amountToken, uint256 amountNativeCurrency);

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactNativeCurrencyForTokens(
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function swapTokensForExactNativeCurrency(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapExactTokensForNativeCurrency(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);

    function swapNativeCurrencyForExactTokens(
        uint256 amountOut,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external payable returns (uint256[] memory amounts);

    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) external pure returns (uint256 amountOut);

    function getAmountIn(
        uint256 amountOut,
        uint256 reserveIn,
        uint256 reserveOut
    ) external pure returns (uint256 amountIn);

    function getAmountsOut(uint256 amountIn, address[] calldata path)
        external
        view
        returns (uint256[] memory amounts);

    function getAmountsIn(uint256 amountOut, address[] calldata path)
        external
        view
        returns (uint256[] memory amounts);
}

// File: @openzeppelin/contracts/token/ERC20/IERC20.sol



pragma solidity ^0.8.0;

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
    /**
     * @dev Returns the amount of tokens in existence.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns the amount of tokens owned by `account`.
     */
    function balanceOf(address account) external view returns (uint256);

    /**
     * @dev Moves `amount` tokens from the caller's account to `recipient`.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transfer(address recipient, uint256 amount) external returns (bool);

    /**
     * @dev Returns the remaining number of tokens that `spender` will be
     * allowed to spend on behalf of `owner` through {transferFrom}. This is
     * zero by default.
     *
     * This value changes when {approve} or {transferFrom} are called.
     */
    function allowance(address owner, address spender) external view returns (uint256);

    /**
     * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * IMPORTANT: Beware that changing an allowance with this method brings the risk
     * that someone may use both the old and the new allowance by unfortunate
     * transaction ordering. One possible solution to mitigate this race
     * condition is to first reduce the spender's allowance to 0 and set the
     * desired value afterwards:
     * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
     *
     * Emits an {Approval} event.
     */
    function approve(address spender, uint256 amount) external returns (bool);

    /**
     * @dev Moves `amount` tokens from `sender` to `recipient` using the
     * allowance mechanism. `amount` is then deducted from the caller's
     * allowance.
     *
     * Returns a boolean value indicating whether the operation succeeded.
     *
     * Emits a {Transfer} event.
     */
    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);

    /**
     * @dev Emitted when `value` tokens are moved from one account (`from`) to
     * another (`to`).
     *
     * Note that `value` may be zero.
     */
    event Transfer(address indexed from, address indexed to, uint256 value);

    /**
     * @dev Emitted when the allowance of a `spender` for an `owner` is set by
     * a call to {approve}. `value` is the new allowance.
     */
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

// File: contracts/periphery/Router.sol



pragma solidity >=0.8.0;






contract Router is IRouter {
    using Math for uint256;

    address public override factory;
    address public override WNativeCurrency;

    constructor(address _factory, address _WNativeCurrency) {
        factory = _factory;
        WNativeCurrency = _WNativeCurrency;
    }

    modifier ensure(uint256 deadline) {
        require(deadline >= block.timestamp, "Router: EXPIRED");
        _;
    }

    receive() external payable {
        require(msg.sender == WNativeCurrency); // only accept Native Currency via fallback from the WNativeCurrency contract
    }

    function addLiquidity(
        address token0,
        address token1,
        uint256 amount0Desired,
        uint256 amount1Desired,
        uint256 amount0Min,
        uint256 amount1Min,
        address to,
        uint256 deadline
    )
        public
        override
        ensure(deadline)
        returns (
            uint256 amount0,
            uint256 amount1,
            uint256 liquidity
        )
    {
        (amount0, amount1) = _addLiquidity(
            token0,
            token1,
            amount0Desired,
            amount1Desired,
            amount0Min,
            amount1Min
        );
        address pair = Helper.pairFor(factory, token0, token1);
        Helper.safeTransferFrom(token0, msg.sender, pair, amount0);
        Helper.safeTransferFrom(token1, msg.sender, pair, amount1);
        liquidity = IPair(pair).mint(to);
    }

    function addLiquiditySingleToken(
        address[] calldata path,
        uint256 amountIn,
        uint256 amountSwapOut,
        uint256 amountSwapInMax,
        uint256 amountInReserveMin,
        address to,
        uint256 deadline
    ) external override ensure(deadline) returns (uint256 liquidity) {
        address token0 = path[0];
        address token1 = path[path.length - 1];

        uint256[] memory amounts = swapTokensForExactTokens(
            amountSwapOut,
            amountSwapInMax,
            path,
            to,
            deadline
        );

        uint256 amountInReserve = amountIn - amounts[0];
        (, , liquidity) = addLiquidity(
            token1,
            token0,
            amounts[amounts.length - 1],
            amountInReserve,
            amounts[amounts.length - 1],
            amountInReserveMin,
            to,
            deadline
        );
    }

    function addLiquidityNativeCurrency(
        address token,
        uint256 amountTokenDesired,
        uint256 amountTokenMin,
        uint256 amountNativeCurrencyMin,
        address to,
        uint256 deadline
    )
        external
        payable
        override
        ensure(deadline)
        returns (
            uint256 amountToken,
            uint256 amountNativeCurrency,
            uint256 liquidity
        )
    {
        (amountToken, amountNativeCurrency) = _addLiquidity(
            token,
            WNativeCurrency,
            amountTokenDesired,
            msg.value,
            amountTokenMin,
            amountNativeCurrencyMin
        );
        address pair = Helper.pairFor(factory, token, WNativeCurrency);
        Helper.safeTransferFrom(token, msg.sender, pair, amountToken);
        IWNativeCurrency(WNativeCurrency).deposit{
            value: amountNativeCurrency
        }();
        require(IERC20(WNativeCurrency).transfer(pair, amountNativeCurrency));
        liquidity = IPair(pair).mint(to);
        if (msg.value > amountNativeCurrency)
            Helper.safeTransferNativeCurrency(
                msg.sender,
                msg.value - amountNativeCurrency
            ); // refund dust native currency, if any
    }

    function addLiquiditySingleNativeCurrency(
        address[] memory path,
        uint256 amountSwapOut,
        uint256 nativeCurrencySwapInMax,
        uint256 nativeCurrencyReserveMin,
        address to,
        uint256 deadline
    )
        external
        payable
        override
        ensure(deadline)
        returns (
            uint256 amountToken,
            uint256 amountNativeCurrency,
            uint256 liquidity
        )
    {
        // Swap
        require(path[0] == WNativeCurrency, "Router: INVALID_PATH");
        uint256[] memory amounts = Helper.getAmountsIn(
            factory,
            amountSwapOut,
            path
        );

        require(amounts[0] <= msg.value, "Router: EXCESSIVE_INPUT_AMOUNT");
        IWNativeCurrency(WNativeCurrency).deposit{value: amounts[0]}();

        require(
            IERC20(WNativeCurrency).transfer(
                Helper.pairFor(factory, path[0], path[1]),
                amounts[0]
            )
        );

        _swap(amounts, path, to);

        require(
            amounts[0] <= nativeCurrencySwapInMax,
            "not allow bigger than nativeCurrencySwapInMax"
        );

        // Addliquidity
        address token = path[path.length - 1];
        uint256 nativeCurrencyReserve = msg.value - amounts[0];
        (amountToken, amountNativeCurrency) = _addLiquidity(
            token,
            WNativeCurrency,
            amounts[amounts.length - 1],
            nativeCurrencyReserve,
            amounts[amounts.length - 1],
            nativeCurrencyReserveMin
        );

        address pair = Helper.pairFor(factory, token, WNativeCurrency);

        Helper.safeTransferFrom(token, msg.sender, pair, amountToken);

        IWNativeCurrency(WNativeCurrency).deposit{
            value: amountNativeCurrency
        }();

        require(IERC20(WNativeCurrency).transfer(pair, amountNativeCurrency));

        liquidity = IPair(pair).mint(to);

        if (msg.value > (amountNativeCurrency + amounts[0]))
            Helper.safeTransferNativeCurrency(
                msg.sender,
                msg.value - (amountNativeCurrency + amounts[0])
            ); // refund dust native currency, if any
    }

    function _addLiquidity(
        address token0,
        address token1,
        uint256 amount0Desired,
        uint256 amount1Desired,
        uint256 amount0Min,
        uint256 amount1Min
    ) private returns (uint256 amount0, uint256 amount1) {
        if (IFactory(factory).getPair(token0, token1) == address(0)) {
            IFactory(factory).createPair(token0, token1);
        }
        (uint256 reserve0, uint256 reserve1) = Helper.getReserves(
            factory,
            token0,
            token1
        );
        if (reserve0 == 0 && reserve1 == 0) {
            (amount0, amount1) = (amount0Desired, amount1Desired);
        } else {
            uint256 amount1Optimal = Helper.quote(
                amount0Desired,
                reserve0,
                reserve1
            );
            if (amount1Optimal <= amount1Desired) {
                require(
                    amount1Optimal >= amount1Min,
                    "Router: INSUFFICIENT_1_AMOUNT"
                );
                (amount0, amount1) = (amount0Desired, amount1Optimal);
            } else {
                uint256 amount0Optimal = Helper.quote(
                    amount1Desired,
                    reserve1,
                    reserve0
                );
                require(amount0Optimal <= amount0Desired);
                require(
                    amount0Optimal >= amount0Min,
                    "Router: INSUFFICIENT_0_AMOUNT"
                );
                (amount0, amount1) = (amount0Optimal, amount1Desired);
            }
        }
    }

    function removeLiquidity(
        address token0,
        address token1,
        uint256 liquidity,
        uint256 amount0Min,
        uint256 amount1Min,
        address to,
        uint256 deadline
    )
        public
        override
        ensure(deadline)
        returns (uint256 amount0, uint256 amount1)
    {
        address pair = Helper.pairFor(factory, token0, token1);
        IERC20(pair).transferFrom(msg.sender, pair, liquidity);
        (uint256 amountA, uint256 amountB) = IPair(pair).burn(to);
        (address tokenA, ) = Helper.sortTokens(token0, token1);
        (amount0, amount1) = tokenA == token0
            ? (amountA, amountB)
            : (amountB, amountA);
        require(amount0 >= amount0Min, "Router: INSUFFICIENT_0_AMOUNT");
        require(amount1 >= amount1Min, "Router: INSUFFICIENT_1_AMOUNT");
    }

    function removeLiquidityNativeCurrency(
        address token,
        uint256 liquidity,
        uint256 amountTokenMin,
        uint256 amountNativeCurrencyMin,
        address to,
        uint256 deadline
    )
        public
        override
        ensure(deadline)
        returns (uint256 amountToken, uint256 amountNativeCurrency)
    {
        (amountToken, amountNativeCurrency) = removeLiquidity(
            token,
            WNativeCurrency,
            liquidity,
            amountTokenMin,
            amountNativeCurrencyMin,
            address(this),
            deadline
        );
        Helper.safeTransfer(token, to, amountToken);
        IWNativeCurrency(WNativeCurrency).withdraw(amountNativeCurrency);
        Helper.safeTransferNativeCurrency(to, amountNativeCurrency);
    }

    function _swap(
        uint256[] memory amounts,
        address[] memory path,
        address _to
    ) private {
        for (uint256 i; i < path.length - 1; i++) {
            (address input, address output) = (path[i], path[i + 1]);
            (address token0, ) = Helper.sortTokens(input, output);
            uint256 amountOut = amounts[i + 1];
            (uint256 amount0Out, uint256 amount1Out) = input == token0
                ? (uint256(0), amountOut)
                : (amountOut, uint256(0));
            address to = i < path.length - 2
                ? Helper.pairFor(factory, output, path[i + 2])
                : _to;
            IPair(Helper.pairFor(factory, input, output)).swap(
                amount0Out,
                amount1Out,
                to
            );
        }
    }

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) public override ensure(deadline) returns (uint256[] memory amounts) {
        amounts = Helper.getAmountsOut(factory, amountIn, path);
        require(
            amounts[amounts.length - 1] >= amountOutMin,
            "Router: INSUFFICIENT_OUTPUT_AMOUNT"
        );
        Helper.safeTransferFrom(
            path[0],
            msg.sender,
            Helper.pairFor(factory, path[0], path[1]),
            amounts[0]
        );
        _swap(amounts, path, to);
    }

    function swapTokensForExactTokens(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) public override ensure(deadline) returns (uint256[] memory amounts) {
        amounts = Helper.getAmountsIn(factory, amountOut, path);
        require(amounts[0] <= amountInMax, "Router: EXCESSIVE_INPUT_AMOUNT");
        Helper.safeTransferFrom(
            path[0],
            msg.sender,
            Helper.pairFor(factory, path[0], path[1]),
            amounts[0]
        );
        _swap(amounts, path, to);
    }

    function swapExactNativeCurrencyForTokens(
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    )
        external
        payable
        override
        ensure(deadline)
        returns (uint256[] memory amounts)
    {
        require(path[0] == WNativeCurrency, "Router: INVALID_PATH");
        amounts = Helper.getAmountsOut(factory, msg.value, path);
        require(
            amounts[amounts.length - 1] >= amountOutMin,
            "Router: INSUFFICIENT_OUTPUT_AMOUNT"
        );
        IWNativeCurrency(WNativeCurrency).deposit{value: amounts[0]}();
        require(
            IERC20(WNativeCurrency).transfer(
                Helper.pairFor(factory, path[0], path[1]),
                amounts[0]
            )
        );
        _swap(amounts, path, to);
    }

    function swapTokensForExactNativeCurrency(
        uint256 amountOut,
        uint256 amountInMax,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external override ensure(deadline) returns (uint256[] memory amounts) {
        require(
            path[path.length - 1] == WNativeCurrency,
            "Router: INVALID_PATH"
        );
        amounts = Helper.getAmountsIn(factory, amountOut, path);
        require(amounts[0] <= amountInMax, "Router: EXCESSIVE_INPUT_AMOUNT");
        Helper.safeTransferFrom(
            path[0],
            msg.sender,
            Helper.pairFor(factory, path[0], path[1]),
            amounts[0]
        );
        _swap(amounts, path, address(this));
        IWNativeCurrency(WNativeCurrency).withdraw(amounts[amounts.length - 1]);
        Helper.safeTransferNativeCurrency(to, amounts[amounts.length - 1]);
    }

    function swapExactTokensForNativeCurrency(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external override ensure(deadline) returns (uint256[] memory amounts) {
        require(
            path[path.length - 1] == WNativeCurrency,
            "Router: INVALID_PATH"
        );
        amounts = Helper.getAmountsOut(factory, amountIn, path);
        require(
            amounts[amounts.length - 1] >= amountOutMin,
            "Router: INSUFFICIENT_OUTPUT_AMOUNT"
        );
        Helper.safeTransferFrom(
            path[0],
            msg.sender,
            Helper.pairFor(factory, path[0], path[1]),
            amounts[0]
        );
        _swap(amounts, path, address(this));
        IWNativeCurrency(WNativeCurrency).withdraw(amounts[amounts.length - 1]);
        Helper.safeTransferNativeCurrency(to, amounts[amounts.length - 1]);
    }

    function swapNativeCurrencyForExactTokens(
        uint256 amountOut,
        address[] calldata path,
        address to,
        uint256 deadline
    )
        external
        payable
        override
        ensure(deadline)
        returns (uint256[] memory amounts)
    {
        require(path[0] == WNativeCurrency, "Router: INVALID_PATH");
        amounts = Helper.getAmountsIn(factory, amountOut, path);
        require(amounts[0] <= msg.value, "Router: EXCESSIVE_INPUT_AMOUNT");
        IWNativeCurrency(WNativeCurrency).deposit{value: amounts[0]}();
        require(
            IERC20(WNativeCurrency).transfer(
                Helper.pairFor(factory, path[0], path[1]),
                amounts[0]
            )
        );
        _swap(amounts, path, to);
        if (msg.value > amounts[0])
            Helper.safeTransferNativeCurrency(
                msg.sender,
                msg.value - amounts[0]
            ); // refund dust eth, if any
    }

    function getAmountOut(
        uint256 amountIn,
        uint256 reserveIn,
        uint256 reserveOut
    ) public pure override returns (uint256 amountOut) {
        return Helper.getAmountOut(amountIn, reserveIn, reserveOut);
    }

    function getAmountIn(
        uint256 amountOut,
        uint256 reserveIn,
        uint256 reserveOut
    ) public pure override returns (uint256 amountIn) {
        return Helper.getAmountOut(amountOut, reserveIn, reserveOut);
    }

    function getAmountsOut(uint256 amountIn, address[] memory path)
        public
        view
        override
        returns (uint256[] memory amounts)
    {
        return Helper.getAmountsOut(factory, amountIn, path);
    }

    function getAmountsIn(uint256 amountOut, address[] memory path)
        public
        view
        override
        returns (uint256[] memory amounts)
    {
        return Helper.getAmountsIn(factory, amountOut, path);
    }
}