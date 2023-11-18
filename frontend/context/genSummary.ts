// import * as dotenv from "dotenv";
// import OpenAI from 'openai';
const dotenv = require('dotenv');
const OpenAI = require('openai');

dotenv.config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_KEY,
});
  
// Function to generate text
async function generateText(prompt: string): Promise<void> {
    try {
      const response = await openai.chat.completions.create({
        model: "gpt-4", // or another model of your choice
        messages: [{role: 'user', content: prompt}],
        // prompt: prompt,
        max_tokens: 500,
      });
  
      console.log(response.choices[0].message.content);
    } catch (error) {
      console.error("Error in generating text:", error);
    }
}


const my_prompt = `
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
        score: -100,
        isCompliant: false,
        isHuman: true,
        usdBalance: 24639,
        age: 19672,
        transactionCount: 207,
        worldcoinProved: false,
        lensConnections: 0,
        twitterFollowers: 0,
        noncompliantTxns: 2,
    }


`;


// Example usage
// generateText("Write a poem about the sea");
// generateText(my_prompt);

const _s = '100157357636319927670444618802812115406879512317632484138301548510234534445102n'
const queryId = _s.substring(0, _s.length - 1);
console.log(_s, queryId)
