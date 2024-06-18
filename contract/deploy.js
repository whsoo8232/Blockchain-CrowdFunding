const hardhat = require("hardhat");

async function main() {
    const Token_Funding = await hardhat.ethers.getContractFactory("Token_Funding");
    
    console.log("Deploying Token_Funding...");

    const contract = await Token_Funding.deploy();

    console.log(contract.target)
}

main();