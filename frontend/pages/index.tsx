import { useEffect, useRef, useState } from 'react';
import Layout from '@/components/layout';
import { AddressInput, getAxiomQueryId, getIPFSHash, getUMAAssertionId } from '@/components/header/AddressInput';
import { State } from '@/context/context';
import { Summary } from '@/components/profile/Summary';
import { useContractEvent, useContractRead } from 'wagmi';
import { REP_ORACLE_GOERLI, REP_USER_GOERLI, demoContractAbi, repOracleAbi } from '@/context/cosnts';
import { SumAndTerm } from '@/components/profile/SumAndTerm';
import { Evidence } from '@/components/profile/Evidence';


function goerliTxUrl(hash: string) {
    return `https://goerli.etherscan.io/tx/${hash}`;
}



async function fetch_data(setFetched, rid, proofs_ref, address, assertionId) {

    let ipfshash = await getIPFSHash(rid);

    // richerd 
    ipfshash = {
        '0xeb1c22baacafac7836f20f684c946228401ff01c': 'QmcsVNJuNQYAh26ytARtHar84ALNxmNRD2bnSfp9AUSb7A', // richerd
        '0xc1f2b71a502b551a65eee9c96318afdd5fd439fa': 'QmXJHigLsHiDVXv7U8G16nbtLBqP2nu1RViDEufUn7euCx', // bad guy
        '0xae2fc483527b8ef99eb5d9b44875f005ba1fae13': 'QmVNC8SEjpunQDpLaLeRhcBMpFMWBdcWrARoRPC6tgs5VM' // mev bot
    } [address.toLowerCase()];
    console.log('rid = ', rid, 'ipfshash = ', ipfshash);
    const url = `https://cloudflare-ipfs.com/ipfs/${ipfshash}`;


    fetch(url)
        .then((response) => response.json())
        .then(async (fetched) => {
            console.log('fetched ', fetched, JSON.stringify(fetched));

            proofs_ref.current = {
                umaAssertionId: assertionId,
                umaVerified: false,
            };

            setFetched(fetched);
        })
        .catch((error) => console.log(error));
} 


export default function Home() {


    const [eventLogs, setEventLogs] = useState([]);
    const [state, setState] = useState(State.Init);
    const [fetched, setFetched] = useState(null);
    const proofs_ref = useRef(null);
    const address_ref = useRef(null);

    const requestId = useRef(null);


    const pushLog = (log) => {
        if (state == State.AllDone) {
            return;
        }
        eventLogs.push(log);
        setEventLogs([...eventLogs]);
    }

    useContractEvent({
        address: REP_USER_GOERLI,
        chainId: 5,
        abi: demoContractAbi,
        eventName: "*",
        listener: async (events) => { 

            const event = events[0] as any;

            console.log('event = ', event, 'request_id = ', requestId.current, 'event_request_id = ', event.args.requestId); 

            // demo contract sent request 
            if (event.eventName == 'RequestSent'
                 ) {
                pushLog({ msg: '[User] Request sent to Oracle.', url: goerliTxUrl(event.transactionHash) });

            // demo contract got reputation profile
            } else if (event.eventName == 'ReputationScoreReceived' &&
                        event.args.requestId === requestId.current) {
                pushLog({ msg: '[User] Reputation profile received.', url: goerliTxUrl(event.transactionHash) });

            // reputation profile settled
            } else if (event.eventName == 'ReputationScoreCommitted' &&
                        event.args.requestId === requestId.current) {
                pushLog({ msg: '[User] Reputation profile finalized.', url: goerliTxUrl(event.transactionHash) });
                setState(State.AllDone);
            }
        }
    });

    useContractEvent({
        address: REP_ORACLE_GOERLI,
        chainId: 5,
        abi: repOracleAbi,
        eventName: "*",
        listener: (events) => { 
            
            const event = events[0] as any;

            console.log('event = ', event, 'request_id = ', requestId.current, 'event_request_id = ', event.args.requestId); 

            // oracle received request
            if (event.eventName == 'RequestReceived') {
                requestId.current = event.args.requestId;
                eventLogs.push({ msg: '[Oracle] Request received.', url: goerliTxUrl(event.transactionHash) });
                setEventLogs([...eventLogs]);

            // reputation profile ready at oracle 
            } else if (event.eventName == 'ReputationScoreSent' &&
                        event.args.requestId === requestId.current) {
                eventLogs.push({ msg: '[Oracle] Reputation profile sent to user.', url: goerliTxUrl(event.transactionHash) });
                setEventLogs([...eventLogs]);

                const rid = requestId.current;
                // intential promise
                fetch_data(setFetched, rid, proofs_ref, address_ref.current, event.args.assertionId);  

            // uma assertion settled
            } else if (event.eventName == 'UMAAssertionResolved' &&
                        event.args.requestId === requestId.current) {
                eventLogs.push({ msg: '[Oracle] UMA assertion settled.', url: goerliTxUrl(event.transactionHash) });
                console.log('- a');
                setEventLogs([...eventLogs]);
                console.log('- b');

                proofs_ref.current.umaVerified = true;

            // axiom proved
            } else if (event.eventName == 'AxiomVerificationSuccess' &&
                event.args.requestId === requestId.current) {
                eventLogs.push({ msg: '[Oracle] Axiom proof ready.', url: goerliTxUrl(event.transactionHash) });

                const queryId = event.args.queryId as string;                
                proofs_ref.current.axiomQueryId = queryId;
                proofs_ref.current.axiomVerified = true;
            }
        }
    });

    const [hoho, setHoho] = useState(0);
    const hohoRef = useRef(null);
    const hohoXDelta = Math.PI / 30;
    useEffect(() => {
        // Set up an interval to update the ticker value every second
        const interval = setInterval(() => {
            hohoRef.current = (hohoRef.current != null) ? (hohoRef.current + hohoXDelta) : 0;
            setHoho(Math.sin(hohoRef.current) * 2);
        }, 1000 / 20);
    
        return () => clearInterval(interval);
    }, [hohoXDelta]);


    const [loadingDots, setLoadingDots] = useState(0);
    const loadingDotRef = useRef(null);
    useEffect(() => {
        // Set up an interval to update the ticker value every second
        const interval = setInterval(() => {
            loadingDotRef.current = (loadingDotRef.current != null) ? (loadingDotRef.current + 1) % 4 : 0;
            setLoadingDots(loadingDotRef.current);
        }, 1000 / 4);
    
        return () => clearInterval(interval);
    }, []);


    return (
        <Layout
            input={<AddressInput logs={eventLogs} setLogs={setEventLogs} setState={setState} globalAddressRef={address_ref}/>}
            hoho={hoho}
        >
            <div>
                {state != State.Init && <Summary fetched={fetched} address={address_ref.current} />}
                {state != State.Init && <SumAndTerm fetched={fetched} loadingDots={loadingDots} logs={eventLogs} state={state}/>}

                {fetched && 
                 <div className="border-t-2 border-black mt-24 ml-10 mr-16 content-center">
                    <p className="text-3xl font-bold font-mono w-52 text-center -mt-5 mx-auto bg-yellow-50">Evidence</p>
                </div>}

                {fetched && <Evidence fetched={fetched} proofs={proofs_ref.current}/>}

                <div className='h-32' />
            </div>

        </Layout>
    )
}
