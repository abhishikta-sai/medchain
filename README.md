# medchain

This project showcases the journey of Medicine on blockchain.

The Pharmaceutical supply chain is the sequence of activities and process to bring medicines from Manufacturer to Customer.

#### Problems in Existing System
---
- Slow Process and Error prone paper work
- Mutable and Invalid source
- Lack of coordination

#### What we are providing
---
- Accurate information across the entire chain at any point and at any location
- Instant access to real-time updates and alerts if issues are detected
- Visibility of all handovers in the supply chain
- Traceability back to source of all materials
- Seamless collaboration between all parties
- Reduce paper work and Speedup process

#### Contracts
---
1. Admin
2. Manufacturer
3. Wholesaler
4. Customer

**Admin :** Admin stores the records of all medicines manufactured and uses it to validate future transactions.

**Transporter :** Transporter are responsible for shipping packages/consignment form one stage to other.

**Manufacturer :** Manufacturer is responsible to manufacturer new medicine batches, by getting new batchIds from Admin that is used to manufacture new batch medicine and quantity.

**Wholesaler :** Wholesaler is reponsible to receive medicine from Manufacturer and validate medicine recieved, than sell it to the customer or other Wholesaler/Retailers. 

**Distrubuter :** Distributer is reponsible to distribute medicne to pharms and do varification on medicine quality and condition.

**Customer :** Customer can enquire the avalaibility of the medicine among different wholesaler, and also validate the purchased medicine genunity.

#### Tools and Technologies
---
- Solidity (Ethereum Smart Contract Language)
- Metamask (Ethereum wallet)
- Truffle
- Web3JS

#### Prerequisites
---
- Nodejs v8.12 or above
- Truffle v5.0.0 (core: 5.0.0) (http://truffleframework.com/docs/getting_started/installation)
- Solidity v0.5.0
- Metamask (https://metamask.io)
- Ganache (https://truffleframework.com/docs/ganache/quickstart)

#### Setup
---
**Local Deployment**
1. Ganache :
For first time setup :
- Run Ganache : ```ganache-cli```
- Store the mnemonics for future use

For repeated use:
- Run Ganache using the stored mnemonics : ```ganache-cli -m "mnemonics"```

2. Truffle :
- goto the project folder in terminal
- truffle compile and deployment : ```truffle migrate --restart```

**Remix.etheruem platform**

(the connection should be "http" and not "https")

Link : ```http://remix.ethereum.org/#optimize=false&evmVersion=null&version=soljson-v0.5.11+commit.c082d0b4.js```

1. upload the solidity file "SupplyChain.sol"

2. Compile it using compile button in the sidebar (it is the third symbol from top)

3. Click the run button in sidebar (fourth symbol from top), which will open a sidtab. In that select an account and deploy the Admin contract.

4. Then deploy the Manufacturer and Wholesaler contracts by passing the address of the deployed admin contract and their License numbers.

5. Then deploy Customer contract by passing the address of the deployed admin contract.
