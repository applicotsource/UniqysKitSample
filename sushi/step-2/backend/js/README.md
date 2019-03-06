backendディレクトリ作る
```
mkdir backend
mkdir backend/js
```

uniqys initする
```
cd backend
uniqys dev-init
```

dapp.jsonを編集する
```
"startApp": "node js/server.js"
```

npm init する
```
cd js
npm init

# enter enter enter...

npm install --save express body-parser memcached
```

`backend/js/server.js` を編集する
```
const express = require("express")
const bodyParser = require("body-parser")
const Memcached = require("memcached")

const APP_HOST = '0.0.0.0'
const APP_PORT = 5650
const DB_HOST = 'localhost'
const DB_PORT = 5652

const app = express()
const memcached = new Memcached(`${DB_HOST}:${DB_PORT}`)

app.use(bodyParser())

app.listen(APP_PORT, APP_HOST)
```

`POST '/api/generate'` を作る
```
npm install --save keccak

const keccak = require('keccak')

async function incrCount () {
  return new Promise((resolve, reject) => {
    memcached.incr('count', 1, (err, result) => {
      if (err) return reject(err)
      if (typeof result === 'number') return resolve(result)
      memcached.set('count', 1, 0, (err) => {
        if (err) return reject(err)
        resolve(1)
      })
    })
  })
}

app.post('/api/generate', async (req, res) => {
  const sender = req.header('uniqys-sender')
  const timestamp = req.header('uniqys-timestamp')
  const blockhash = req.header('uniqys-blockhash')

  const count = await incrCount()
  const newSushi = {
    id: count,
    status: 'normal',
    price: 0,
    owner: sender,
    dna: keccak('keccak256').update(count).digest('hex')
  }

  memcached.set(`messages:${count}`, {
    id: count,
    sender,
    timestamp,
    blockhash,
    sushi: newSushi
  }, 0, (err) => {
    if (err) {
      res.status(400).send(err)
    }
    else {
      res.sendStatus(200)
    }
  })
})
```

# 他
## データをけしたい
```
cd backend
rm -rf .data
uniqys init ./dapp.json
```