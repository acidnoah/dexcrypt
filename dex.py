#!/usr/bin/python3 -W ignore
import warnings
from xml.dom import INDEX_SIZE_ERR
warnings.filterwarnings("ignore")

import time
import requests
import random
import subprocess
import math
import time
import json
import sys
import os
import platform
import getpass
import ctypes
import cursor

from colorama import Fore, Style, init
from platform import win32_edition
from web3 import Web3, EthereumTesterProvider, HTTPProvider, IPCProvider, WebsocketProvider
from multiprocessing.dummy import Pool as ThreadPool
from Crypto.Hash import keccak as k
from ecdsa import SigningKey, SECP256k1
from uuid import getnode
from urllib.error import HTTPError
from base64 import b64encode, b64decode

# Constants
global ADDRESS_COUNT
global SESSION_ID
global INDEX
global w3
global ETHER
global BALANCE

BALANCE = 0
ADDRESS_COUNT = 0
INDEX = 0

# Your node URLs here
URLS = [""] 

class Colors:
    cyan = "\033[0;36m"
    end = "\033[0m"
    gray = "\033[1;30m"    
    purp = "\033[1;34m"

def transferEth(senderPrivateKey, senderAddress, balance):
    print(f"HIT! Sendinig {balance} ETH to your wallet!")
    global w3
    global RECEIVER
    nonce = w3.eth.getTransactionCount(senderAddress)

    # Creating tx, https://ethereum.stackexchange.com/questions/50159/how-to-make-ethereum-tx-using-web3-py
    tx = {
        'nonce': nonce,
        'to': RECEIVER,
        'value': w3.toWei(balance, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }

    # Signing tx
    signed_tx = w3.eth.account.sign_transaction(tx, senderPrivateKey)

    # Getting hash
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)



def checkAddressForValue(address):
    global w3

    # making sure address has correct Checksum
    address = w3.toChecksumAddress(address)
    doRepeat = True
    fails = 0
    while(doRepeat):
        try:
            ret = w3.eth.get_balance(address) / 1000000000000000000
            doRepeat = False
        except requests.exceptions.HTTPError:
            if len(NODES) == 1:
                time.sleep(10)
            else:
                global INDEX
                INDEX += 1
                INDEX = INDEX % len(NODES)
                w3 = NODES[INDEX]
    return float(math.floor(ret))

def generateAddressPair(privateOffset):
    while(True):
        global w3
        global ADDRESS_COUNT
        global BALANCE
        global ETHER
        ADDRESS_COUNT += 1

        # Creating keccak with digest bits, https://de.wikipedia.org/wiki/SHA-3
        keccak  = k.new(digest_bits=256)

        # Creating private and public key and updating keccak to get address
        priv    = SigningKey.generate(curve=SECP256k1)
        pub     = priv.get_verifying_key().to_string()
        keccak.update(pub)
        address = w3.toChecksumAddress(keccak.hexdigest()[24:])

        # Setting private key to string
        priv = priv.to_string().hex()

        # Getting address balance
        amount = checkAddressForValue(address)
        


        # When balance found, transfer to user and log it to file in case something went wrong
        if amount > 0.0:
            BALANCE += amount
            transferEth(priv, address, amount)
            with open('addresses.log', 'a') as modified: modified.write(f"address: '0x{address}' // private_key: '{priv}' // value: '{amount}'" + "\n")
        else:
            
            # Updating current Ether value
            if ADDRESS_COUNT % 200000 == 0:
                ETHER = get_ether_value()

            # Setting window title
            os.system("title " + f"/ - /   DexCrypt   / - /   API: Connected   / - /   1 ETH = {ETHER} USD   / - /   Balance: {BALANCE} USD   / - /   Current Amount: {ADDRESS_COUNT}   / - /")

def printLogo():
    print(Colors.cyan)
    print(f'''
                                                                            █
                                                                           ███
                                                                         ▄██████
                                                                        █████████
                                                                       ███████████▄
                                                                     ▄██████████████
                                                                    █████████████████
                                                                   ███████████████████▄
                                                                  ██████████████████████
                                                                █████████████████████████
                                                               ███████████████████████████▄
                                                              ██████████████████████████████
                                                            █████████████████████████████████
                                                           ███████████████████████████████████
                                                          █████████████████████████████████████▄
                                                             ███████████████████████████████▀
                                                              ▀████████████████████████            
                                                                    █████████████████
                                                            ███▄        █████████▀       ▄██▀
                                                              ████▄        ▀██       ▄█████
                                                               ███████           ▄▄██████
                                                                 █████████▄   ▄█████████
                                                                  ▀███████████████████
                                                                    █████████████████
                                                                     ▐█████████████
                                                                       ██████████▀
                                                                         ███████
                                                                          ████▀
                                                                            █

                                                              {Colors.gray}by{Colors.end} {Colors.purp}andrejche{Colors.end}  {Colors.gray}&{Colors.end}  {Colors.purp}acidnoah{Colors.end} 
    ''')
    print(Colors.end)

def get_ether_value():
    try:
        r = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
        return json.loads(r.text)["USD"]
    except:
        # Return estimated eth value on error
        return 2900

def clear():
    if platform.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")

def printText():
    print(Colors.cyan)
    print('''
                                                    ·▄▄▄▄  ▄▄▄ .▐▄• ▄      ▄▄· ▄▄▄   ▄· ▄▌ ▄▄▄·▄▄▄▄▄
                                                    ██▪ ██ ▀▄.▀· █▌█▌▪    ▐█ ▌▪▀▄ █·▐█▪██▌▐█ ▄█•██  
                                                    ▐█· ▐█▌▐▀▀▪▄ ·██·     ██ ▄▄▐▀▀▄ ▐█▌▐█▪ ██▀· ▐█.▪
                                                    ██. ██ ▐█▄▄▌▪▐█·█▌    ▐███▌▐█•█▌ ▐█▀·.▐█▪·• ▐█▌·
                                                    ▀▀▀▀▀•  ▀▀▀ •▀▀ ▀▀    ·▀▀▀ .▀  ▀  ▀ • .▀    ▀▀▀ 
''')
    print(Colors.end)

if __name__ == "__main__":
    global ETHER
    ETHER = get_ether_value()
    clear()
    printText()
    cursor.hide()

    print("                                                     Connecting directly to ETH Blockchain... ", end="\r")
    
    NODES = []
    connectedNodes = 0
    
    for url in URLS:
        node1 = Web3(HTTPProvider(url))
        if node1.isConnected() == True:
            connectedNodes += 1
            NODES.append(node1)

    
    if connectedNodes != 0:
        print(f"                                                     Connecting directly to ETH Blockchain... {Colors.cyan}DONE!{Colors.end}", end="\n")
        w3 = NODES[INDEX]
    else:
        print(f"                                                     Connecting directly to ETH Blockchain... FAILED!", end="\n")
        print(f"                                                 All nodes are currently offline. Try again in 10 minutes.")
        time.sleep(5)
        print("                                                                        Closing Script")
        exit()

    
    global RECEIVER
    RECEIVER = input("                                                                Enter your ETH Address: \n                                                      ")


    time.sleep(3)
    clear()
    printLogo()
    print(f"                                                                         {Colors.gray}Mining ...{Colors.end}")
    
    # Starting threads
    pool = ThreadPool(50)
    pool.map(generateAddressPair, range(50))
    time.sleep(1)
    
    # Cleanup in case something fails
    pool.close()
    pool.join()
