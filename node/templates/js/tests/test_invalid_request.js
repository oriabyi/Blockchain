try {
  createCORSRequest('POST', 'http://127.0.2.1:5000')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GET', 'http://127.0.2.1:5000')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('POSTR', 'http://127.0.0.1:5000')
}
catch(err) {
  console.log(err.message)
}

try {
  createCORSRequest('GETR', 'http://127.0.0.1:5000')
}
catch(err) {
  console.log(err.message)
}
