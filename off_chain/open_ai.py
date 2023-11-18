# coding:utf-8
"""

@time: 2023/11/17
"""

import openai
import os


# Configure OpenAI with your API key
openai.api_key = os.getenv('OPENAI_KEY')


def generate_text(score, is_compliant, is_human, usd_balance, age, nonce, worldcoin, lens, twitter, non_compliant=0):
    prompt = """
    Please write a short summary for a blockchain address, summarizing its information. For each address, you will be provided with a list of key information. Your job is to provide a English summary. 
    
    Here are some examples. 

    Address information:
    
    { 
        score: 55,
        isCompliant: true,
        isHuman: true,
        usdBalance: 134.5,
        age: 678,
        transactionCount: 120,
        worldcoinProved: true,
        lensConnections: 0,
        twitterFollowers: 120,
        noncompliantTxns: 0,
    }

    English summary:

    This account is highly trustworthy and compliant, likely operated by a human. It has been active for 678 days, executing 120 transactions. The current balance stands at a minimum of $134.5 USD. Verified by Worldcoin's proof of humanity, it also has 120 Twitter followers and a clean record with no non-compliant transactions detected.

    Address information:
    
    { 
        score: -100,
        isCompliant: false,
        isHuman: false,
        usdBalance: 19034.5,
        age: 23,
        transactionCount: 12,
        worldcoinProved: false,
        lensConnections: 0,
        twitterFollowers: 0,
        noncompliantTxns: 2,
    }

    English summary:

    Caution: This account is non-compliant, identified with 2 non-compliant transactions. We advise against interacting with this address to maintain compliance. If interaction is necessary, please proceed with extreme caution. The account, active for 23 days, has issued 12 transactions but lacks proof of humanity and any social media presence.

    Address information:
    
    { 
        score: 2,
        isCompliant: true,
        isHuman: false,
        usdBalance: 40,
        age: 3,
        transactionCount: 1,
        worldcoinProved: false,
        lensConnections: 1,
        twitterFollowers: 0,
        noncompliantTxns: 0,
    }

    English summary:

    This account is recent and lacks detailed background information. While compliant, its status as a human-operated account is uncertain. Active for only 3 days, it has conducted a single transaction with a minimum balance of $40 USD. There is no proof of humanity or social media activity except one connection on Lens protocol. Exercise caution to ensure you are not engaging with bot accounts.

    Now please give the English summary for the following Address information:

    {
    """+f"""score: {score},
        isCompliant: {is_compliant},
        isHuman: {is_human},
        usdBalance: {usd_balance},
        age: {age/24/60/60},
        transactionCount: {nonce},
        worldcoinProved: {worldcoin},
        lensConnections: {lens},
        twitterFollowers: {twitter},
        noncompliantTxns: {non_compliant},
    """ + "}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as error:
        print("Error in generating text:", error)
        return ""


if __name__ == '__main__':
    generate_text(20, True, True, 1340, 323*24*60*60, 42, True, 22 ,22, 0)
