const hardhat = require("hardhat");

async function main() {
    const CrowdFunding = await hardhat.ethers.getContractFactory("CrowdFunding");
    
    console.log("Deploying CrowdFunding...");

    const contract = await CrowdFunding.deploy();

    console.log(contract.target)
}

main();