import { Proofs, State } from '@/context/context';
import styles from './Summary.module.css';
import { useNetwork } from 'wagmi';



function item(title: string, val, proof) {
    return (
        <div className="flex flex-column w-full">
            <pre className="basis-2/5 pl-10">{title}</pre>
            <div className="basis-1/5">{val}</div>
            {proof}
        </div>
    );
}

function link(text, url) {
    return (
        <a className="underline text-blue-600" href={url}>{text}</a>
    );
}

function tableHeada(colNames: string[]) {
    return (
        <thead className="text-base text-gray-700 uppercase bg-blue-100 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                {colNames.map(colName => (
                    <th scope="col" className="px-6 py-3" key={colName}>
                        {colName}
                    </th>
                ))}
            </tr>
        </thead>
    );
}

function zkpStamp(proofs) {
    if (!proofs?.axiomQueryId || !proofs?.axiomVerified) {
        return (<></>);
    }

    const url = `https://explorer.axiom.xyz/v2/goerli/mock/query/${proofs.axiomQueryId}`  

    return (
        <span className='p-1 px-2 bg-black text-white'>
            <span className='mr-1 bg-black text-white'>Axiom ZKP</span> 
            (
            <a className='ml-1 underline' href={url} target="_blank">Proof</a>
            ,
            <span className='ml-1'>{'\u2705'} Verified</span>
            )
        </span>
    );
}

const CHAIN_NAMES = {
    '1': 'Ethereum',
    '5': 'Goerli Testnet',
    '100': 'Gnosis',
    '137': 'Polygon'
};

const GOERLI_CHAIN_ID = 5;   // this is the only chain we support for Axiom ZKP for now


function basics(fetched: any, currentChainId: number, proofs: Proofs) {
    return (
        <div className="relative overflow-x-auto sm:rounded-lg ml-10 mr-16 mt-6">
            <table className="w-full text-base text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <caption className="p-5 text-2xl font-semibold text-left rtl:text-right text-gray-900 dark:text-white dark:bg-gray-800">
                    On-chain Basics
                    {/* <p className="mt-1 text-sm font-normal text-gray-500 dark:text-gray-400">The address's basic stats from all monitored chains. A zero-knowledge proof is provided whenever possible. Otherwise they are optimistically proved: </p> */}
                </caption>
                {tableHeada(['Chain', 'Age', '#Transactions', 'USD Balance'])}
                <tbody>
                    {Object.keys(fetched.chain_stats).map(key => {
                        const stat = fetched.chain_stats[key];
                        return (
                            <tr className="border-b dark:bg-gray-800 dark:border-gray-700" key={key}>
                                <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                    {CHAIN_NAMES[key]}
                                    {key === currentChainId.toString() && 
                                        <span className='ml-5 text-blue-600'>(Current chain)</span>}
                                </th>
                                <td className="px-6 py-4">
                                    {`${Math.round(stat['age'] / 86400).toLocaleString()} days`}
                                    <span className='ml-5' />
                                    {(currentChainId == GOERLI_CHAIN_ID && key === currentChainId.toString() && proofs.axiomQueryId && proofs.axiomVerified) && 
                                        zkpStamp(proofs)}
                                </td>
                                <td className="px-6 py-4">
                                    {stat['nonce'].toLocaleString()}
                                    <span className='ml-5' />
                                    {(currentChainId == GOERLI_CHAIN_ID && key === currentChainId.toString() && proofs.axiomQueryId && proofs.axiomVerified) && 
                                        zkpStamp(proofs)}
                                </td>
                                <td className="px-6 py-4">
                                    {'$' + stat['usd_balance'].toLocaleString()}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}



function social(fetched: any) {
    return (
        <div className="relative overflow-x-auto sm:rounded-lg ml-10 mr-16 mt-8">
            <table className="w-full text-base text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <caption className="p-5 text-2xl font-semibold text-left rtl:text-right text-gray-900 dark:text-white dark:bg-gray-800">
                    Social and Humanity Proof
                    {/* <p className="mt-1 text-sm font-normal text-gray-500 dark:text-gray-400">The address's basic stats from all monitored chains. A zero-knowledge proof is provided whenever possible. Otherwise they are optimistically proved: </p> */}
                </caption>
                {tableHeada(['Source of verification', 'Value'])}
                <tbody>
                <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            Worldcoin proof of humanity
                        </th>
                        <td className="px-6 py-4">
                            {fetched.world_coin_confirmed ? 'True' : 'False'}
                        </td>
                    </tr>
                    <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            Lens protocol
                        </th>
                        <td className="px-6 py-4">
                            {fetched.lens_followers.toLocaleString() + ' followers'}
                        </td>
                    </tr>
                    <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            Twitter 
                            {fetched.twitter_account && <a className="underline text-blue-600 ml-2" href={`https://twitter.com/${fetched.twitter_account}`} target="_blank">
                                {'@' + fetched.twitter_account}</a>}
                        </th>
                        <td className="px-6 py-4">
                            {fetched.twitter_followers.toLocaleString() + ' followers'}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}





function secomp(fetched: any) {
    if (fetched.non_compliant_txns === 0) {
        return (
            <div className="relative overflow-x-auto sm:rounded-lg ml-10 mr-16 mt-8">
                <table className="w-full text-base text-left rtl:text-right text-gray-500 dark:text-gray-400">
                    <caption className="p-5 text-2xl font-semibold text-left rtl:text-right text-gray-900 dark:text-white dark:bg-gray-800">
                        Security and Compliance
                        <p className="pt-1 mt-1 text-base font-normal text-green-600 dark:text-gray-400 font-bold">All actions found to be compliant.</p>
                    </caption>
                </table>
            </div>
        );
    }

    return (
        <div className="relative overflow-x-auto sm:rounded-lg ml-10 mr-16 mt-8">
            <table className="w-full text-base text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <caption className="p-5 text-2xl font-semibold text-left rtl:text-right text-gray-900 dark:text-white dark:bg-gray-800">
                    Security and Compliance
                    {/* <p className="mt-1 text-sm font-normal text-gray-500 dark:text-gray-400">The address's basic stats from all monitored chains. A zero-knowledge proof is provided whenever possible. Otherwise they are optimistically proved: </p> */}
                </caption>
                {tableHeada(['Chain', 'Transaction', 'Non-compliance'])}
                <tbody>
                    {fetched.non_compliant_txn_list.map(nct => {
                        return (<tr className="border-b dark:bg-gray-800 dark:border-gray-700" key={nct.url}>
                            <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                {CHAIN_NAMES[nct.chain_id]}
                            </th>
                            <td className="px-6 py-4">
                                <a className='text-blue-600 underline' href={nct.url}>Transaction</a>
                            </td>
                            <td className="px-6 py-4">
                                {nct.attack_analysis ? 
                                    <span className='text-red-600'>
                                        Attack transaction according to <a className="underline" href={nct.attack_analysis}>{nct.attack_analysis}</a>
                                    </span>
                                    : 
                                    <span className='text-red-600'>
                                        Interaction with <a className="underline" href={nct.interaction_with_mixer_url}>{nct.interaction_with_mixer_name}</a>
                                    </span>    
                                }       
                            </td>
                        </tr>);
                    })}
                </tbody>
            </table>
        </div>
    );
}



function proof(fetched: any, currentChainId: number, proofs: Proofs) {
    return (
        <div className="relative overflow-x-auto sm:rounded-lg ml-10 mr-16 mt-8">
            <table className="w-full text-base text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <caption className="p-5 text-2xl font-semibold text-left rtl:text-right text-gray-900 dark:text-white dark:bg-gray-800">
                    Proofs
                    <p className="mt-1 text-base font-normal text-gray-500 dark:text-gray-400">
                        To substantiate the reputation profile, zero-knowledge proofs via 
                        <a className="underline text-blue-600" href="https://www.axiom.xyz/" target="_blank"> Axiom </a> 
                        are employed for all evidence whenever feasible. Commonsense evidence, like Twitter follower counts, 
                        is validated optimistically using the 
                        <a className="underline text-blue-600" href="https://uma.xyz/" target="_blank"> UMA </a> protocol. 
                        For evidence needing specialized assessment, such as compliance verification of an address,
                        <a className="underline text-blue-600" href="https://thumbs.dreamstime.com/b/silly-foolish-face-vector-cartoon-white-background-201168746.jpg" target="_blank"> Rep-DAO </a> 
                        provides optimistic validation.</p>
                </caption>
                {tableHeada(['Proof Type', 'Value'])}
                <tbody>
                    {(currentChainId == GOERLI_CHAIN_ID && (GOERLI_CHAIN_ID.toString() in fetched.chain_stats) 
                        && proofs.axiomQueryId && proofs.axiomVerified) && 
                        <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                            <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                Zero-knowledge Proof
                            </th>
                            <td className="px-6 py-4">
                                <div>{zkpStamp(proofs)}</div>
                            </td>
                        </tr>
                    }
                    <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            Optimistic Proof
                        </th>
                        <td className="px-6 py-4">
                            <a className='underline p-1 px-2 bg-pink-300 text-black' href={`https://testnet.oracle.umaproject.org/settled?search=${proofs.umaAssertionId}`} target="_blank">
                                {proofs.umaVerified ? 'UMA proof (settled)' : 'UMA proof (pending)'}
                            </a>
                        </td>
                    </tr>
                    <tr className="border-b dark:bg-gray-800 dark:border-gray-700">
                        <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                            Rep-DAO Proof
                        </th>
                        <td className="px-6 py-4">
                            <a className='p-1 px-2 bg-gray-300 text-black' href={`https://testnet.oracle.umaproject.org/settled?search=${proofs.umaAssertionId}`} target="_blank">
                                Coming soon
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}


export function Evidence({ fetched, proofs }) {
    const { chain, chains } = useNetwork()
    
    const zkp = link('zero-knowledge proof', '');
    const opp = link('optimistic proof', '');

    return (
        <div>
            {basics(fetched, chain.id, proofs)}
            {social(fetched)}
            {secomp(fetched)}
            {proof(fetched, chain.id, proofs)}
        </div>
    );
}
