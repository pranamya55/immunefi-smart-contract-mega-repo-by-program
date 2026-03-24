import hre from "hardhat";
import * as fs from "fs";
import { parseEther } from "ethers";

const VESTED_ZERO_NFT_ADDRESS = "0x9FA72ea96591e486FF065E7C8A89282dEDfA6C12";
const ZERO_ADDRESS = "0x78354f8dccb269a615a7e0a24f9b0718fdc3c7a7";

async function main() {
  if (!VESTED_ZERO_NFT_ADDRESS.length) {
    throw new Error("Invalid Vest Address");
  }
  const [deployer] = await hre.ethers.getSigners();
  console.log("I am", deployer.address);

  const vest = await hre.ethers.getContractAt(
    "VestedZeroNFT",
    VESTED_ZERO_NFT_ADDRESS
  );

  // const zero = await hre.ethers.getContractAt("ZeroLend", ZERO_ADDRESS);
  // await zero.approve(vest, parseEther("1000000000000000000"));

  // Initialize an empty array to store the parsed data
  const parsedData: any[] = [];

  // Read the CSV file
  console.log("reading file");
  fs.readFile(
    "scripts/vestList.csv",
    "utf8",
    async (err: any, data: string) => {
      if (err) {
        console.error("Error reading file:", err);
        return;
      }

      // Split the CSV data into rows
      const rows = data.trim().split("\n");

      // Iterate over the rows starting from index 1 (skipping the header)
      for (let i = 1; i < rows.length; i++) {
        const [
          address, // Address,
          total, // Total,
          upfront_perc, // Upfront %,
          cliff_days, // Cliff days,
          vesting_days, // Vesting days,
          upfront_tokens, // Upfront tokens
        ] = rows[i].split(",");

        // const startDate = Math.floor(
        //   new Date("06 May 2024 07:30:00 UTC").getTime() / 1000
        // );

        const rowData = {
          who: address,
          pending: parseEther(
            (parseInt(total) - parseInt(upfront_tokens)).toString()
          ),
          upfront: parseEther(upfront_tokens),
          linearDuration: parseInt(vesting_days) * 86400,
          cliffDuration: parseInt(cliff_days) * 86400,
          unlockDate: 0,
          hasPenalty: false,
          category: 0,
        };

        parsedData.push(rowData);
      }

      console.log("working on", parsedData.length);
      for (let i = 0; i < parsedData.length; i++) {
        const {
          who,
          pending,
          upfront,
          linearDuration,
          cliffDuration,
          unlockDate,
          hasPenalty,
          category,
        } = parsedData[i];

        console.log(
          i,
          who,
          pending,
          upfront,
          linearDuration,
          cliffDuration,
          unlockDate,
          hasPenalty,
          category
        );

        const tx = await vest.mint(
          who,
          pending,
          upfront,
          linearDuration,
          cliffDuration,
          unlockDate,
          hasPenalty,
          category
        );
        // console.log("Vest minted for: ", tx);
        console.log("Vest minted for: ", tx.hash);
        await tx.wait(1);
      }
    }
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
