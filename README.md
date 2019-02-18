# Pitcoin

Simple implementation of bitcoin.

Bitcoin: A Peer-to-Peer Electronic Cash System

## Getting Started

You need python 3.6.2 and pip 19.0.1 versions

```
python3 --version
Python 3.6.2
```

```
pip --version
pip 19.0.1
```

### Prerequisites

First of all download you need to download project from git repository:

```
git clone https://xteams-gitlab.unit.ua/xteams/module-3-ariabyi.git ariabyi && cd ariabyi
```
Go to the created folder
```
cd ariabyi
```

Second of all you its desirable to have a virtual env to download all pip packages, to use them in future
# How to install virtualenv:

### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Now create a virtual environment
   You can go faster way just write
   
   ```
   alias virtualenv='$HOME/bin/virtualenv' ;
   alias activ="source venv/bin/activate" ;
   alias pipr="pip install -r requirements.txt";
   alias prepenv="cvenv && activ && pipr"; prepenv
   ```
   Or go a little bit longer way
    
    virtualenv venv 

>you can use any name instead of **venv**

### You can also use a Python interpreter of your choice

    virtualenv -p /usr/bin/python3 venv
  
### Active your virtual environment:    
    
    source venv/bin/activate
    

### To deactivate:

    deactivate


To install all packages you need to run this cash system use:
```
pip install -r requirements.txt
```

# Using The Pitcoin

Okay, now you have all the conditions so you can use this node.
First of all you need to activate env.
```
activ
```
Now you need to start server
```
(activ) python server.py
```

Open a new terminal window and go to the curent directory.
Launch the command line interface to create you private key:
```
(activ) python wallet_cli.py
```
Use the new command to generate a new private key and public address.
The public key are saved in Public_key.txt, private key will not be save anywhere, because
it could declassify your data, just wrote private key in any save place

![ScreenShot](https://imgur.com/XxfwnDM.png)

The send command in wallet cli with two parameters - sender address
and amount (Example of bitcoin address -  17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1).
Then broadcast transaction to the network:

Open a new terminal window and go to the curent directory.
Run miner-cli to start mining.
```
(activ) python miner_cli.py
```
At first we need to connect with our server:
```
add node ip
```
To mine one block use command `mine`:

![ScreenShot](https://imgur.com/qAWchbk.png)


### Routes

/transaction/new - creates a new pending transaction

/transaction/pendings - return pendings transactions

/chain - return all blockchain in JSON format

/chain/length - return length of blockchain

/balance?addr=\<address\> - return the balance of given address


# UnitTestS

```
python -m tests/unit_test.py
```


