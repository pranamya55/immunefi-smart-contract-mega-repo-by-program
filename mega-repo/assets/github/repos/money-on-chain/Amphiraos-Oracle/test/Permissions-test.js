const { expectRevert, constants } = require("openzeppelin-test-helpers");

const MoCMedianizer = artifacts.require("./MoCMedianizer.sol");
const PriceFactory = artifacts.require("./price-feed/FeedFactory.sol");
const PriceFeed = artifacts.require("./price-feed/PriceFeed.sol");
const Authority = artifacts.require("./authority/MoCGovernedAuthority.sol");
const MoCGovernorMock = artifacts.require("./mocks/MoCGovernorMock.sol");

const { toContract } = require("../utils/numberHelper");

let priceFeeds = [];
let medianizer;

const { ZERO_ADDRESS } = constants;

const currentTimestamp = async () => {
  const lastBlock = await web3.eth.getBlock("latest");
  return lastBlock.timestamp;
};

const createPriceFeed = factory => async account => {
  const txReceipt = await factory.create({ from: account });
  const feed = await PriceFeed.at(txReceipt.logs[0].args.feed);

  return feed;
};

let createFeed;

contract("MoCAuthority", function([from, governorOwner, ...accounts]) {
  before(async function() {
    const governor = await MoCGovernorMock.new({ from: governorOwner });
    const factory = await PriceFactory.new({ from });
    createFeed = createPriceFeed(factory);
    const authority = await Authority.new(governor.address, { from });

    medianizer = await MoCMedianizer.new({ from });
    // From now there are two authorized users to modify Medianizer
    // from and governorOwner
    await medianizer.setAuthority(authority.address, { from });
    await medianizer.setOwner(ZERO_ADDRESS, { from });

    priceFeeds[0] = await createFeed(accounts[0]);
    priceFeeds[1] = await createFeed(accounts[1]);
    priceFeeds[2] = await createFeed(accounts[2]);
  });

  describe("GIVEN some users wants to set and remove PriceFeeds", function() {
    let testPriceFeed;
    before(async function() {
      testPriceFeed = await createFeed(accounts[3]);
    });
    it("WHEN an unauthorized user wants to set a PriceFeed THEN transaction reverts", async function() {
      const tx = medianizer.set(testPriceFeed.address, { from: accounts[0] });
      await expectRevert.unspecified(tx);
    });
    it("WHEN the original owner wants to set a PriceFeed THEN transaction reverts", async function() {
      const tx = medianizer.set(testPriceFeed.address, { from });
      await expectRevert.unspecified(tx);
    });
    describe("WHEN an authorized user tries to set a PriceFeed", function() {
      before(async function() {
        await medianizer.set(testPriceFeed.address, { from: governorOwner });
      });
      it("THEN the PriceFeed is set", async function() {
        const feedPosition = await medianizer.indexes(testPriceFeed.address);
        assert(Number(feedPosition) !== 0, "PriceFeed was not set");
      });
      describe("WHEN an unauthorized user tries to remove a PriceFeed", function() {
        it("THEN the transaction reverts", async function() {
          const tx = medianizer.unset(testPriceFeed.address, { from });
          await expectRevert.unspecified(tx);
        });
      });
      describe("WHEN an authorized user tries to unset a PriceFeed", function() {
        it("THEN the priceFeed is unset", async function() {
          const feedPosition = await medianizer.indexes(testPriceFeed.address);
          assert(Number(feedPosition), 0, "PriceFeed was not unset");
        });
      });
    });
  });

  describe("GIVEN a PriceFeed is set", function() {
    before(async function() {
      await medianizer.set(priceFeeds[0].address, { from: governorOwner });
    });
    describe("WHEN a price of 8000 USD and Expiration of 10 blocks is set for the first feed", async function() {
      const price = 8000 * 10 ** 18;
      before(async function() {
        // Set expiration date for 5 minutes from now
        const expiration = (await currentTimestamp()) + 5 * 60;
        await priceFeeds[0].post(
          toContract(price),
          toContract(expiration),
          medianizer.address,
          {
            from: accounts[0]
          }
        );
      });
      it("THEN the priceFeed have the value", async function() {
        const peekValue = await priceFeeds[0].peek();

        assert(
          Number(peekValue["0"]),
          price,
          "The Medianizer value is incorrect"
        );
        assert(peekValue["1"], true, "The Medianizer have no value");
      });
      it("THEN the medianizer have the value", async function() {
        const peekValue = await medianizer.peek();

        assert(
          Number(peekValue["0"]),
          price,
          "The Medianizer value is incorrect"
        );
        assert(peekValue["1"], true, "The Medianizer have no value");
      });
      describe("WHEN Governor set minimum feeders to 3", function() {
        before(async function() {
          await medianizer.setMin(3, { from: governorOwner });
        });
        it("THEN the Medianizer have no more price", async function() {
          const peekValue = await medianizer.peek();
          assert(peekValue["1"], false, "The Medianizer have value");
        });
        describe("WHEN 2 priceFeeders are set with prices", function() {
          before(async function() {
            await medianizer.set(priceFeeds[1].address, {
              from: governorOwner
            });
            await medianizer.set(priceFeeds[2].address, {
              from: governorOwner
            });

            // Set expiration date for 5 minutes from now
            const expiration = (await currentTimestamp()) + 5 * 60;
            await priceFeeds[1].post(
              toContract(10000 * 10 ** 18),
              toContract(expiration),
              medianizer.address,
              {
                from: accounts[1]
              }
            );

            await priceFeeds[2].post(
              toContract(9000 * 10 ** 18),
              toContract(expiration),
              medianizer.address,
              {
                from: accounts[2]
              }
            );
          });
          it("THEN the new price is set to 9000", async function() {
            const peekValue = await medianizer.peek();

            assert(
              Number(peekValue["0"]),
              9000 * 10 ** 18,
              "The Medianizer value is incorrect"
            );
            assert(peekValue["1"], true, "The Medianizer have no value");
          });
        });
      });
    });
  });
});
