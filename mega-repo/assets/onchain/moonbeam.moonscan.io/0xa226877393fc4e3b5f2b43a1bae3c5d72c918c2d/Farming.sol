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

// File: contracts/libraries/AdminUpgradeable.sol



pragma solidity >=0.8.0;

abstract contract AdminUpgradeable {
    address public admin;
    address public adminCandidate;

    function _initializeAdmin(address _admin) internal {
        require(admin == address(0), "admin already set");

        admin = _admin;
    }

    function candidateConfirm() external {
        require(msg.sender == adminCandidate, "not Candidate");
        emit AdminChanged(admin, adminCandidate);

        admin = adminCandidate;
        adminCandidate = address(0);
    }

    function setAdminCandidate(address _candidate) external onlyAdmin {
        adminCandidate = _candidate;
        emit Candidate(_candidate);
    }

    modifier onlyAdmin {
        require(msg.sender == admin, "not admin");
        _;
    }

    event Candidate(address indexed newAdmin);
    event AdminChanged(address indexed oldAdmin, address indexed newAdmin);
}
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

// File: contracts/periphery/Farming.sol


pragma solidity >=0.8.0;





contract Farming is AdminUpgradeable {
    using Math for uint256;
    // Info of each user.
    struct UserInfo {
        uint256 amount; // How many farming tokens that user has provided.
        uint256[] rewardDebt; // Reward debt. See explanation below.
        // pending reward = (user.amount * pool.accRewardPerShare) - user.rewardDebt
        // Whenever a user stakes or redeems farming tokens to a pool. Here's what happens:
        //   1. The pool's `accRewardPerShare` (and `lastRewardBlock`) gets updated.
        //   2. User add pending reward to his/her info.
        //   3. User's `amount` gets updated.
        //   4. User's `rewardDebt` gets updated.
        uint256[] pending; // Pending rewards.
        uint256 nextClaimableBlock; // Next Block user can claim rewards.
    }
    // Info of each pool.
    struct PoolInfo {
        address farmingToken; // Address of farming token contract.
        address[] rewardTokens; // Reward tokens.
        uint256[] rewardPerBlock; // Reward tokens created per block.
        uint256[] accRewardPerShare; // Accumulated rewards per share, times 1e12.
        uint256[] remainingRewards; // remaining rewards in the pool.
        uint256 amount; // amount of farming token.
        uint256 lastRewardBlock; // Last block number that pools updated.
        uint256 startBlock; // Start block of pools.
        uint256 claimableInterval; // How many blocks of rewards can be claimed.
    }
    // Info of each pool.
    PoolInfo[] private poolInfo;
    // Info of each user that stakes farming tokens.
    mapping(uint256 => mapping(address => UserInfo)) private userInfo;

    event PoolAdded(address indexed farmingToken);
    event Charged(uint256 indexed pid, address[] rewards, uint256[] amounts);
    event WithdrawRewards(uint256 indexed pid, address[] rewards, uint256[] amounts);
    event Stake(address indexed user, uint256 indexed pid, uint256 amount);
    event Redeem(address indexed user, uint256 indexed pid, uint256 amount);
    event Claim(
        address indexed user, 
        uint256 indexed pid, 
        address[] rewards,
        uint256[] amounts
    );
    event EmergencyWithdraw(
        address indexed user,
        uint256 indexed pid,
        uint256 amount
    );

    constructor() {
        _initializeAdmin(msg.sender);
    }

    function poolLength() external view returns (uint256) {
        return poolInfo.length;
    }

    // Add a new farming token to the pool. Can only be called by the admin.
    // XXX DO NOT add the same farming token more than once. Rewards will be messed up if you do.
    function add(
        address _farmingToken,
        address[] memory _rewardTokens,
        uint256[] memory _rewardPerBlock,
        uint256 _startBlock,
        uint256 _claimableInterval
    ) external onlyAdmin {
        require(_rewardTokens.length == _rewardPerBlock.length, 'INVALID_REWARDS');
        uint256 lastRewardBlock =
            block.number > _startBlock ? block.number : _startBlock;
        uint256[] memory accRewardPerShare = new uint256[](_rewardTokens.length);
        uint256[] memory remainingRewards = new uint256[](_rewardTokens.length);
        poolInfo.push(
            PoolInfo({
                farmingToken: _farmingToken,
                rewardTokens: _rewardTokens,
                rewardPerBlock: _rewardPerBlock,
                accRewardPerShare: accRewardPerShare,
                remainingRewards: remainingRewards,
                amount: 0,
                lastRewardBlock: lastRewardBlock,
                startBlock: _startBlock,
                claimableInterval: _claimableInterval
            })
        );
        emit PoolAdded(_farmingToken);
    }

    // Update the given pool's rewardPerBlock. Can only be called by the admin.
    function set(
        uint256 _pid,
        uint256[] memory _rewardPerBlock,
        bool _withUpdate
    ) external onlyAdmin {
        if (_withUpdate) {
            updatePool(_pid);
        }
        PoolInfo storage pool = poolInfo[_pid];
        require(_rewardPerBlock.length == pool.rewardPerBlock.length, 'INVALID_REWARDS');
        pool.rewardPerBlock = _rewardPerBlock;
    }

    // Charge the given pool's rewards. Can only be called by the admin.
    function charge(
        uint256 _pid,
        uint256[] memory _amounts
    ) external onlyAdmin {
        PoolInfo storage pool = poolInfo[_pid];
        require(_amounts.length == pool.rewardTokens.length, 'INVALID_AMOUNTS');
        for (uint256 i = 0; i < _amounts.length; i++) {
            if (_amounts[i] > 0) {
                Helper.safeTransferFrom(
                    pool.rewardTokens[i], 
                    msg.sender, 
                    address(this), 
                    _amounts[i]
                );
                pool.remainingRewards[i] = pool.remainingRewards[i].add(_amounts[i]);
            }
        }
        emit Charged(_pid, pool.rewardTokens, _amounts);
    }

    // Withdraw the given pool's rewards. Can only be called by the admin.
    function withdrawRewards(
        uint256 _pid,
        uint256[] memory _amounts
    ) external onlyAdmin {
        PoolInfo storage pool = poolInfo[_pid];
        require(_amounts.length == pool.rewardTokens.length, 'INVALID_AMOUNTS');
        for (uint256 i = 0; i < _amounts.length; i++) {
            require(_amounts[i] <= pool.remainingRewards[i], 'INVALID_AMOUNT');
            if (_amounts[i] > 0) {
                Helper.safeTransfer(
                    pool.rewardTokens[i], 
                    msg.sender, 
                    _amounts[i]
                );
                pool.remainingRewards[i] = pool.remainingRewards[i].sub(_amounts[i]);
            }
        }
        emit WithdrawRewards(_pid, pool.rewardTokens, _amounts);
    }

    // View function to see the given pool's info.
    function getPoolInfo(uint256 _pid) 
        external 
        view
        returns(
            address farmingToken,
            uint256 amount,
            address[] memory rewardTokens,
            uint256[] memory rewardPerBlock,
            uint256[] memory accRewardPerShare,
            uint256 lastRewardBlock,
            uint256 startBlock,
            uint256 claimableInterval
        )
    {
        PoolInfo memory pool = poolInfo[_pid];
        farmingToken = pool.farmingToken;
        amount = pool.amount;
        rewardTokens = pool.rewardTokens;
        rewardPerBlock = pool.rewardPerBlock;
        accRewardPerShare = pool.accRewardPerShare;
        lastRewardBlock = pool.lastRewardBlock;
        startBlock = pool.startBlock;
        claimableInterval = pool.claimableInterval;
    }

    // View function to see the remaing rewards of the given pool.
    function getRemaingRewards(uint256 _pid) 
        external
        view
        returns(uint256[] memory remainingRewards)
    {
        PoolInfo memory pool = poolInfo[_pid];
        remainingRewards = pool.remainingRewards;
    }

    // View function to see the given pool's info of user.
    function getUserInfo(uint256 _pid, address _user)
        external 
        view
        returns(
            uint256 amount,
            uint256[] memory pending,
            uint256[] memory rewardDebt,
            uint256 nextClaimableBlock
        )
    {
        UserInfo memory user = userInfo[_pid][_user];
        amount = user.amount;
        pending = user.pending;
        rewardDebt= user.rewardDebt;
        nextClaimableBlock = user.nextClaimableBlock;
    }

    // View function to see pending rewards.
    function pendingRewards(uint256 _pid, address _user) 
        public 
        view 
        returns(uint256[] memory rewards, uint256 nextClaimableBlock)
    {
        PoolInfo memory pool = poolInfo[_pid];
        UserInfo memory user = userInfo[_pid][_user];
        uint256 farmingTokenSupply = pool.amount;
        rewards = user.pending;
        if (block.number >= pool.lastRewardBlock && user.pending.length > 0 && farmingTokenSupply != 0) {
            for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
                uint256 reward = pool.rewardPerBlock[i].mul(
                    block.number.sub(pool.lastRewardBlock)
                );
                uint256 accRewardPerShare = pool.accRewardPerShare[i].add(
                    reward.mul(1e12) / farmingTokenSupply
                );
                rewards[i] = user.pending[i].add(
                    (user.amount.mul(accRewardPerShare) / 1e12).sub(user.rewardDebt[i])
                );
            }
        }
        nextClaimableBlock = user.nextClaimableBlock;
    }

    // View function to see current periods.
    function getPeriodsSinceStart(uint256 _pid) 
        public 
        view 
        returns(uint256 periods) 
    {
        PoolInfo memory pool = poolInfo[_pid];
        if (block.number <= pool.startBlock) return 0;
        uint256 blocksSinceStart = block.number.sub(pool.startBlock);
        periods = (blocksSinceStart / pool.claimableInterval).add(1);
        if (blocksSinceStart % pool.claimableInterval == 0) {
            periods = periods - 1;
        }
    }

    // Update reward variables of the given pool to be up-to-date.
    function updatePool(uint256 _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        if (block.number <= pool.lastRewardBlock) {
            return;
        }
        uint256 farmingTokenSupply = pool.amount;
        if (farmingTokenSupply == 0) {
            pool.lastRewardBlock = block.number;
            return;
        }
        for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
            uint256 reward = pool.rewardPerBlock[i].mul(
                block.number.sub(pool.lastRewardBlock)
            );
            if (pool.remainingRewards[i] >= reward) {
                pool.remainingRewards[i] = pool.remainingRewards[i].sub(reward);
            } else {
                pool.remainingRewards[i] = 0;
            }
            pool.accRewardPerShare[i] = pool.accRewardPerShare[i].add(
                reward.mul(1e12) / farmingTokenSupply
            );
        }
        pool.lastRewardBlock = block.number;
    }

    // Stake farming tokens to the given pool.
    function stake(
        uint256 _pid,
        address _farmingToken, 
        uint256 _amount
    ) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(pool.farmingToken == _farmingToken, 'FARMING_TOKEN_SAFETY_CHECK');
        updatePool(_pid);
        if (user.amount > 0) {
            for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
                uint256 pending = (
                    user.amount.mul(pool.accRewardPerShare[i]) / 1e12
                ).sub(user.rewardDebt[i]);
                user.pending[i] = user.pending[i].add(pending);
            }
        }
        if (user.nextClaimableBlock == 0 && user.amount == 0) {
            if (block.number <= pool.startBlock) {
                user.nextClaimableBlock = pool.startBlock.add(pool.claimableInterval);
            } else {
                uint256 periods = getPeriodsSinceStart(_pid);
                user.nextClaimableBlock = pool.startBlock.add(
                    periods.mul(pool.claimableInterval)
                );
            }
            user.rewardDebt = new uint256[](pool.rewardTokens.length);
            user.pending = new uint256[](pool.rewardTokens.length);
        }
        Helper.safeTransferFrom(
            pool.farmingToken, 
            msg.sender, 
            address(this), 
            _amount
        );
        user.amount = user.amount.add(_amount);
        pool.amount = pool.amount.add(_amount);
        for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
            user.rewardDebt[i] = user.amount.mul(pool.accRewardPerShare[i]) / 1e12;
        }
        emit Stake(msg.sender, _pid, _amount);
    }

    // Redeem farming tokens from the given pool.
    function redeem(
        uint256 _pid, 
        address _farmingToken, 
        uint256 _amount
    ) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(pool.farmingToken == _farmingToken, 'FARMING_TOKEN_SAFETY_CHECK');
        require(user.amount >= _amount, 'INSUFFICIENT_AMOUNT');
        updatePool(_pid);
        for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
            uint256 pending = (
                user.amount.mul(pool.accRewardPerShare[i]) / 1e12
            ).sub(user.rewardDebt[i]);
            user.pending[i] = user.pending[i].add(pending);
            user.rewardDebt[i] = user.amount.sub(_amount).mul(pool.accRewardPerShare[i]) / 1e12;
        }
        Helper.safeTransfer(pool.farmingToken, msg.sender, _amount);
        user.amount = user.amount.sub(_amount);
        pool.amount = pool.amount.sub(_amount);
        emit Redeem(msg.sender, _pid, _amount);
    }

    // Claim rewards when block number larger than user's nextClaimableBlock.
    function claim(uint256 _pid) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(block.number > user.nextClaimableBlock, 'NOT_CLAIMABLE');
        (uint256[] memory rewards, ) = pendingRewards(_pid, msg.sender);
        updatePool(_pid);
        for (uint256 i = 0; i < pool.accRewardPerShare.length; i++) {
            user.pending[i] = 0;
            user.rewardDebt[i] = user.amount.mul(pool.accRewardPerShare[i]) / 1e12;
            if (rewards[i] > 0) {
                Helper.safeTransfer(pool.rewardTokens[i], msg.sender, rewards[i]);
            }
        }
        uint256 periods = getPeriodsSinceStart(_pid);
        user.nextClaimableBlock = pool.startBlock.add(
            periods.mul(pool.claimableInterval)
        );
        emit Claim(msg.sender, _pid, pool.rewardTokens, rewards);
    }

    // Withdraw without caring about rewards. EMERGENCY ONLY.
    function emergencyWithdraw(uint256 _pid) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        Helper.safeTransfer(pool.farmingToken, msg.sender, user.amount);
        emit EmergencyWithdraw(msg.sender, _pid, user.amount);
        pool.amount = pool.amount.sub(user.amount);
        user.amount = 0;
        user.pending = new uint256[](pool.accRewardPerShare.length);
        user.rewardDebt = new uint256[](pool.accRewardPerShare.length);
        user.nextClaimableBlock = 0;
    }
}