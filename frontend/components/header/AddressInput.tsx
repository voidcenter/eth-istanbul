import { EventLog, State } from '@/context/context';
import styles from './AddressInput.module.css';
import { useEffect, useState } from 'react';
import { readContract, writeContract } from 'wagmi/actions';
import { REP_ORACLE_GOERLI, REP_USER_GOERLI, demoContractAbi, repOracleAbi } from '@/context/cosnts';


export async function getAxiomQueryId(requestId: string) {

    const data = await readContract({
        address: REP_ORACLE_GOERLI,
        abi: repOracleAbi,
        functionName: 'requestId_to_axiom_query_id',
        args: [requestId],
    });

    return data;
}


export async function getIPFSHash(requestId: string) {

    const data = await readContract({
        address: REP_ORACLE_GOERLI,
        abi: repOracleAbi,
        functionName: 'evidence',
        args: [requestId],
    });

    let ipfshash = Buffer.from((data as string).substring(2), 'hex').toString();
    return ipfshash;
}



export function AddressInput({ logs, setLogs, setState, globalAddressRef }) {

    const [address, setAddress] = useState("");

    const handleAddressInputKeyDown = async (e) => {
        if (e.key === 'Enter') {
    
            if (address.endsWith('.eth')) {
                console.log('ENS not supported yet')

            } else {

                const { hash } = await writeContract({
                    address: REP_USER_GOERLI,
                    abi: demoContractAbi,
                    functionName: 'requestReputationScore',
                    args: [address, true, 0],
                });
                console.log('request hash = ', hash);

                setState(State.Requested);
                logs.push({ msg: '[Browser] Request sent to user contract.' })
                setLogs([...logs]);  // create new reference to force update
                globalAddressRef.current = address;

            }

        }
      }
    
      return (<input 
        className={styles.addressInputBox}
        name="myInput" 
        placeholder='enter address to profile reputation'
        onChange={(e) => { setAddress(e.target.value.toLowerCase())}}
        onKeyDown={(e) => handleAddressInputKeyDown(e)} 
      />);
}

