try {
  getBlockByHeight(createCORSRequest('GET','http://127.6.0.1:5000/block?heght=' + document.getElementById('myInputBlockHeight').value))
}
catch(err) {
  console.log(err.message)
}

try {
  getBalanceWallet(createCORSRequest('GET', 'http://127.5.0.1:5000/balance?adr=' + document.getElementById('myInputBalanceWallet').value))
}
catch(err) {
  console.log(err.message)
}

try {
  getChain(createCORSRequest('GET', 'http://127.4.0.1:5000/chai'))
}
catch(err) {
  console.log(err.message)
}

try {
  getChainLen(createCORSRequest('GET', 'http://127.3.0.1:5000/chain/lenth'))
}
catch(err) {
  console.log(err.message)
}

try {
  getBlockByHash(createCORSRequest('GET', 'http://127.0.1.1:5000/hash?hsh=' + document.getElementById('myInputBlockHash').value))
}
catch(err) {
  console.log(err.message)
}
