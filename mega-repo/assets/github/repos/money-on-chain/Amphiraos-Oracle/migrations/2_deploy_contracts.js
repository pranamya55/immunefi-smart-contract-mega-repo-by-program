/* eslint-disable no-console */
const MoCMedianizer = artifacts.require("./MoCMedianizer.sol");
const PriceFactory = artifacts.require("./price-feed/FeedFactory.sol");
const PriceFeed = artifacts.require("./price-feed/PriceFeed.sol");
const Authority = artifacts.require("./authority/MoCGovernedAuthority.sol");
const MoCGovernorMock = artifacts.require("./mocks/MoCGovernorMock.sol");

const { getConfig, saveConfig } = require('./helper');

const { toContract } = require("../utils/numberHelper");
const NULL_ADDRESS = "0x0000000000000000000000000000000000000000";

let medianizer;
let priceFactory;

module.exports = async (deployer, network) => {

  const configPath = `${__dirname}/configs/${network}.json`;
  const config = getConfig(network, configPath);

  // Deploy main contracts
  await deployer.deploy(MoCMedianizer);
  await deployer.deploy(PriceFactory);
  medianizer = await MoCMedianizer.deployed();
  priceFactory = await PriceFactory.deployed();

  // Save deployed address to config file
  config.MoCMedianizer = medianizer.address;
  config.PriceFactory = priceFactory.address;
  saveConfig(config, configPath);

  // Minimum values from PriceFeeders for the Medianizer
  // to return a value
  await medianizer.setMin(config.minValues);
  // Add PriceFeed to Medianizer
  const priceFeed = await createAndSetPriceFeed();

  // Save deployed address to config file
  config.PriceFeed = priceFeed.address;
  saveConfig(config, configPath);

  // Renounce owner and set Governance Authority
  await configureGovernance(deployer, network);
  // Set initial price
  await postPrice(
    priceFeed,
    config.initialPrice,
    config.expirationTime,
    medianizer.address
  );
};

const currentTimestamp = async () => {
  const lastBlock = await web3.eth.getBlock("latest");
  return lastBlock.timestamp;
};

const deployGovernorMock = async deployer => {
  await deployer.deploy(MoCGovernorMock);
  const governorInstance = await MoCGovernorMock.deployed();

  return governorInstance.address;
};

const createAndSetPriceFeed = async () => {
  // Create first Feed
  const creationRcpt = await priceFactory.create();
  const feedAddress = creationRcpt.logs[0].args.feed;
  console.log(`Price Feed: ${feedAddress}`);
  // Add first PriceFeed to Medianizer
  await medianizer.set(feedAddress);

  return new PriceFeed(feedAddress);
};

const postPrice = async (priceFeed, price, expirationTime, medAddress) => {
  // Set expiration date for 5 minutes from now
  const expiration = (await currentTimestamp()) + expirationTime;
  await priceFeed.post(
    toContract(price * 10 ** 18),
    toContract(expiration),
    medAddress
  );
};

const configureGovernance = async (deployer, network) => {

  const configPath = `${__dirname}/configs/${network}.json`;
  const config = getConfig(network, configPath);

  let governor = config.governor;
  // Governor should be already deployed and set in config
  // for testnet and mainnet deploys
  if (network === "development") {
    governor = deployGovernorMock(deployer);
  }

  await deployer.deploy(Authority, governor);
  authority = await Authority.deployed();
  // Setting Governance Authority to Medianizer
  await medianizer.setAuthority(authority.address);
  // Removing owner. Now the only Authority is the Governor contract
  return medianizer.setOwner(NULL_ADDRESS);
};
