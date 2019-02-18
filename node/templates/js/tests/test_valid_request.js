
try {
  createCORSRequest('POST', 'http://127.0.0.1:5000/')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.0.1:5000/')
}
catch(err) {
  console.log(err.message)
}


try {
  createCORSRequest('POST', 'http://127.0.0.1:5000/chain')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.0.1:5000/chain')
}
catch(err) {
  console.log(err.message)
}


try {
  createCORSRequest('POST', 'http://127.0.0.1:5000/chain/length')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.0.1:5000/chain/length')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('POST', 'http://127.0.0.1:5000/block')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.0.1:5000/block')
}
catch(err) {
  console.log(err.message)
}


try {
  createCORSRequest('POST', 'http://127.0.0.1:5000/hash')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.0.1:5000/hash')
}
catch(err) {
  console.log(err.message)
}