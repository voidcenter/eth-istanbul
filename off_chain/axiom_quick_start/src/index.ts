import {
  Axiom,
  AxiomV2Callback,
  QueryV2,
  buildTxSubquery,
  getEventSchema,
  bytes32,
  buildReceiptSubquery,
  AccountSubquery,
  buildAccountSubquery,
  AccountField
} from "@axiom-crypto/core";
import { ethers } from "ethers"; // we'll use ethers-js to make RPC calls
import dotenv from "dotenv";
dotenv.config();

const axiom = new Axiom({
  providerUri: process.env.PROVIDER_URI_GOERLI as string,
  privateKey: process.env.PRIVATE_KEY_GOERLI as string,
  version: "v2",
  chainId: 5, // Goerli
  mock: true // generate Mock proofs for faster development
});
const query = (axiom.query as QueryV2).new();


const txHash =
  "0x0a126c0e009e19af335e964de0cea513098c9efe290c269dee77ca9f10838e7b";
const swapEventSchema = getEventSchema(
  "Swap(address,uint256,uint256,uint256,uint256,address)"
);


// process.argv
console.log(process.argv);
// npx ts-node $latest-block $oracle $address $address-first-block

const latestBlock = parseInt(process.argv[2]);
const oracle = process.argv[3];
const address = process.argv[4];
const firstBlock = parseInt(process.argv[5]);
const requestId = process.argv[6]

// const latestBlock = 10060567;
// const oracle = '0x39a62Cd6B9d956D48c42B73D89a6319E3f3440cF';
// const address = '0xeB1c22baACAFac7836f20f684C946228401FF01C';   // richerd.eth
// const firstBlock = 8242852;


const age1: AccountSubquery = buildAccountSubquery(firstBlock)
    .address(address)
    .field(AccountField.Nonce)
console.log("Appending Account Subquery:", age1);
query.appendDataSubquery(age1);

const age0: AccountSubquery = buildAccountSubquery(firstBlock - 1)
    .address(address)
    .field(AccountField.Nonce);
console.log("Appending Account Subquery:", age0);
query.appendDataSubquery(age0);

const nonce: AccountSubquery = buildAccountSubquery(latestBlock)
    .address(address)
    .field(AccountField.Nonce);
console.log("Appending Account Subquery:", nonce);
query.appendDataSubquery(nonce);

// oracle 
const callback: AxiomV2Callback = {
  target: oracle,
  extraData: bytes32(requestId)
};
query.setCallback(callback);
async function main() {
  if (!(await query.validate())) {
    throw new Error("Query validation failed");
  }
  const builtQuery = await query.build();
  console.log("Query built with the following params:", builtQuery);

  const paymentAmt = await query.calculateFee();
  console.log(
    "Sending a Query to AxiomV2QueryMock with payment amount (wei):",
    paymentAmt
  );

  const queryId = await query.sendOnchainQuery(
    paymentAmt,
    (receipt: ethers.ContractTransactionReceipt) => {
      // You can do something here once you've received the receipt
      console.log("receipt", receipt);
    }
  );
  console.log(
    "View your Query on Axiom Explorer:",
    `https://explorer.axiom.xyz/v2/goerli/mock/query/${queryId}`
  );
}

main();
