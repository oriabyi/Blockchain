try {
  getBlockByHeight(createCORSRequest('GET','http://127.0.0.1:5000/block?height=' + document.getElementById('myInputBlockHeight').value))
}
catch(err) {
  console.log(err.message)
}

try {
  getBalanceWallet(createCORSRequest('GET', 'http://127.0.0.1:5000/balance?addr=' + document.getElementById('myInputBalanceWallet').value))
}
catch(err) {
  console.log(err.message)
}

try {
  getChain(createCORSRequest('GET', 'http://127.0.0.1:5000/chain'))
}
catch(err) {
  console.log(err.message)
}

try {
  getChainLen(createCORSRequest('GET', 'http://127.0.0.1:5000/chain/length'))
}
catch(err) {
  console.log(err.message)
}

try {
  getBlockByHash(createCORSRequest('GET', 'http://127.0.0.1:5000/hash?hash=' + document.getElementById('myInputBlockHash').value))
}
catch(err) {
  console.log(err.message)
}
