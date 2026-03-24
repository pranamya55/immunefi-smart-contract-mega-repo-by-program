import { setup } from "../lib";

const deployer = await setup("mainnet");

const singletonV2ClassHash = await deployer.declareCached("SingletonV2");
const extensionPOV2ClassHash = await deployer.declareCached("DefaultExtensionPOV2");

console.log("SingletonV2 class hash:", singletonV2ClassHash);
console.log("DefaultExtensionPOV2 class hash:", extensionPOV2ClassHash);
