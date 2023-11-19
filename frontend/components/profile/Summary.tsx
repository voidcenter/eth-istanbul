
import { useNetwork } from 'wagmi';


function tfSummary(title: string, bool?: boolean) {
    return (
        <div className="flex flex-column">
            <pre>{title}</pre>
            <span className={bool ? "text-green-600": "text-red-600"}>
                {bool == undefined ? "" : (bool ? "True" : "False")}
            </span>
        </div>
    );
}


export function Summary({ fetched, address }) {
    const { chain, chains } = useNetwork()
    const ens = fetched?.ens;

    return (<div className="flex flex-column font-mono border-solid w-full basis-1 pt-10">

        <div className="basis-2/3">
            <div className="pl-10 pt-10">
                <p className="text-3xl font-bold">{address}</p>
                <p className="text-lg pt-5">{`@${chain.name} (Chain Id : ${chain.id})`}</p>
                {ens && <a href={`https://app.ens.domains/${ens}`}>
                            <p className="text-lg underline text-blue-600">{ens}</p>
                        </a>}
            </div>
        </div>

        <div className="basis-1/3">
            <div className="pl-5 pt-10 font-mono">
                <div className="text-3xl font-bold flex flex-column">
                    <pre>Reputation: </pre>
                    {fetched && <span className={fetched?.score >= 0 ? "text-green-600" : "text-red-600"}>{fetched?.score}</span>}
                </div>

                <div className="text-lg pt-5">
                    {tfSummary('Human     : ', fetched?.is_human)}
                    {tfSummary('Compliant : ', fetched?.is_compliant)}
                </div>
            </div>
        </div>
    </div>);
}

