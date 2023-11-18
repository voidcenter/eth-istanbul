import { Proof, ReputationProfile } from "./context";



// a normal account, with world coin verification, twitter 
// ens 
export const FakeNormal: ReputationProfile = {
    address: "0x89Ef4E13963d8c85b4e7419508209c1Df4991fab".toLowerCase(),
    ens: "zhunping.eth",
    reputation: {
        score: 20,

        isCompliant: true,   // multi-chain
        isHuman: true,

        usdBalance: 1340.5,
        age: 323,
        transactionCount: 42,
        worldcoinProved: true,
        lensConnections: 22,
        twitterFollowers: 32,
        noncompliantTxns: 0,
        placeHolder: 0
    },
    evidence: {
        onchain: {
            chainId: 5,
            blockNumber: 10047996,
            nativeBalance: 0.04,
            wrappedNativeBalance: 0,
            usdcBalance: 0,
            usdtBalance: 0,
            nativePrice: 0.5,
        },
        axiomQueryId: 'test',
        umaAssertionId: 'test',
        repDao: {
            noncompliantAddressesHash: '7f500d886e9e3c983fde9c01de7a7f266522f512e9f4f81fdbd6bf76582aece1',
            noncompliantAddressesIPFSHash: '4d0d17d3e85620efea81f99eab63970a69b20c32b4189ac03948eb9edc581c38',
        },

        usdBalance: Proof.Onchain,
        age: Proof.ZK,
        transactionCount: Proof.ZK,
        worldcoinProved: Proof.Onchain,
        lensConnections: Proof.UMA,
        twitterFollowers: Proof.UMA,
        noncompliantTxns: Proof.UMA,
    },
    summary: 'This account has a fair level of trust and is compliant. Operated by a human, it has been active for 323 days and has engaged in 42 transactions. Its minimum USD balance stands at $1340.5. The account is verified by Worldcoin and also shows some social engagement with 32 Twitter followers and 22 connections on Lens protocol. No non-compliant transactions are associated with this account to date, proving its reliability.'
}; 


