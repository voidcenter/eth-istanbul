import { EventLog, State } from '@/context/context';


export function SumAndTerm({ fetched, loadingDots, logs, state }) {

    return (<div className="flex flex-column font-mono border-solid w-full">

        <div className="basis-2/3">
            <div className="pl-10 pt-14">
                {fetched && <p className="text-lg pr-20">{fetched.summary}</p>}
            </div>
        </div>

        <div className="basis-1/3">
            <div className="ml-5 pl-5 mt-14 mr-16 font-mono border-2 border-solid border-slate-500 bg-gray-300 h-44">
                <ul className="pt-2">
                    {logs.map((log: EventLog) => {

                        const msg = log.msg;
                        if (!log.url) {
                            return (
                                <li className="text-sm" key={msg}>{`→ ${msg}`}</li>
                            );
                        }

                        const ind_right_bracket = msg.indexOf(']')
                        const ctx_str = msg.substring(0, ind_right_bracket + 1);
                        const _msg = msg.substring(ind_right_bracket + 2, msg.length - 1);
                        return (
                            <li className="text-sm" key={msg}>
                                {`→ ${ctx_str} `}
                                <a className="underline text-blue-600" href={log.url} target="_blank">
                                    {_msg}
                                </a>
                                .
                            </li>
                        );
                    })}
                    { (state != State.AllDone && state != State.Init) && 
                     <span className="text-green-600">{'.'.repeat(loadingDots)}</span>}
                </ul>
            </div>
        </div>
    </div>);
}

