const hardhat = require("hardhat");

async function main() {
    const ARTC_Funding = await hardhat.ethers.getContractFactory("ARTC_Funding");
    
    console.log("Deploying ARTC_Funding...");

    const contract = await ARTC_Funding.deploy();

    console.log(contract.target)
}

main();