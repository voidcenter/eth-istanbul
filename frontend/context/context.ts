
export interface Reputation {
    score: number;

    isCompliant: boolean;   // multi-chain
    isHuman: boolean;

    usdBalance: number;
    age: number;  // in days 
    transactionCount: number;
    worldcoinProved: boolean;
    lensConnections: number;
    twitterFollowers: number;
    noncompliantTxns: number;
    placeHolder: number;   // for ethicalStaking, etc.
}


export interface EventLog {
    msg: string;
    url?: string;
}


export enum State {
    Init,
    Requested,
    DataReady,
    AllDone
}

export enum Proof {
    Onchain,
    ZK,
    ZKAxoim,
    UMA,
    Default     // Rep-DAO
}


export interface OnChainEvidence {
    chainId: number;
    blockNumber: number;

    // For simplicity, we can also UMA these. these can be obtained from pools and tokens
    nativeBalance: number;
    wrappedNativeBalance: number;
    usdcBalance: number;
    usdtBalance: number;
    nativePrice: number;     
}


// UMA proofs should include these
export interface Twitter {
    handle: string;
    ens: string;    // most twitters links through a ENS. We ignore those that don't.
    nFollowers: number;
}


export interface Lens {
    nConenctions: number;
}


// Axiom proof should include this
// This pinpoints a log. The log should be a transfer log between this address and another address
// which is usually proved, through a different way, to be problematic 
export interface TransferZKEvidence {
    blockNumber: number;
    txnId: number;
    logId: number;
}



export interface RepDAOEvidence {
    noncompliantAddressesHash: string;      // we upload this list to IPFS with hashes

    // The IPFS files should have：list of addresses, address hash, timestamp 
    // Note that if an address is noncompliant on one chain, it is noncompliant on all chains。
    noncompliantAddressesIPFSHash: string;
}



export interface Evidence {
    // evidence
    onchain: OnChainEvidence;
    axiomQueryId?: string;
    umaAssertionId?: string;
    repDao: RepDAOEvidence;

    // Associating evidence with statements
    usdBalance: Proof;
    age: Proof;
    transactionCount: Proof;
    worldcoinProved: Proof;
    lensConnections: Proof;
    twitterFollowers: Proof;
    noncompliantTxns: Proof;
}


export interface ReputationProfile {
    address: string;
    ens: string;
    reputation?: Reputation;
    evidence: Evidence;
    summary: string;
}

// we also need to make it transparent the algorithm we used to summarize reputation 
// ignore it for now 


export interface Proofs {
    axiomQueryId?: string;
    axiomVerified?: boolean;
    umaAssertionId?: string;
    umaVerified?: boolean;
}



// export interface Context {
//     // input 
//     address?: string;
//     // setAddress?: any;

//     // chainName: string;
//     // chainId?: number;

//     // reputation: ReputationProfile;

//     fetched: any;

//     // IPFSHash?: string;
//     // proofs: Proofs;

//     // state: State;
//     // eventLogs?: string[];
// }



// evidences --> statements --> profile ---> score
// zkp, uma  --> age, nounce --> human, compliant --> 50


