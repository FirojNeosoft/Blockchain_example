import sys
import time
import pprint
import datetime

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from solc import compile_source


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    new_contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])
    tx_hash = new_contract.constructor(1,"https://example.com",'0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF',50).transact()
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)


w3 = Web3(EthereumTesterProvider())

compiled_sol = compile_source_file('crowd_funding.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))

crowd_funding_contract = w3.eth.contract(
   address=address,
   abi=contract_interface['abi'])

list_contributors = []
print("Creator={} \n".format(crowd_funding_contract.functions.getCreator().call()))
print("Receiver={} \n".format(crowd_funding_contract.functions.getReceiver().call()))
print("Target={} \n".format(crowd_funding_contract.functions.getTarget().call()))
print("Expiry={}\n".format(datetime.datetime.fromtimestamp(crowd_funding_contract.functions.getExpiry().call()).strftime('%c')))
print("Current state={} \n".format(crowd_funding_contract.functions.getState().call()))
print("Current Balance={} \n".format(crowd_funding_contract.functions.getBalance().call()))
tx_hash = crowd_funding_contract.functions.contribute('0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69',30).transact()
w3.eth.waitForTransactionReceipt(tx_hash)
list_contributors.append({'contributor':'0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69','amount':30})
tx_hash = crowd_funding_contract.functions.contribute('0x1efF47bc3a10a45D4B230B5d10E37751FE6AA718',20).transact()
receipt = wait_for_receipt(w3, tx_hash, 1)
list_contributors.append({'contributor':'0x1efF47bc3a10a45D4B230B5d10E37751FE6AA718','amount':20})
pprint.pprint(dict(receipt))
print("Current Balance={} \n".format(crowd_funding_contract.functions.getBalance().call()))
tx_hash = crowd_funding_contract.functions.getRefund('0x1efF47bc3a10a45D4B230B5d10E37751FE6AA718').transact()
w3.eth.waitForTransactionReceipt(tx_hash)
print("Current Balance={} \n".format(crowd_funding_contract.functions.getBalance().call()))
print("Current state={} \n".format(crowd_funding_contract.functions.getState().call()))
tx_hash = crowd_funding_contract.functions.payOut().transact()
w3.eth.waitForTransactionReceipt(tx_hash)
print("contributors=", list_contributors,"\n")
print("Payout done \n")
print("Current state={} \n".format(crowd_funding_contract.functions.getState().call()))
print("Current Balance={} \n".format(crowd_funding_contract.functions.getBalance().call()))

