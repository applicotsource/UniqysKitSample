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
    dna: keccak('keccak256').update(count.toString()).digest('hex'),
    timestamp,
    blockhash
  }

  memcached.set(`sushi:${count}`, newSushi, 0, (err) => {
    if (err) {
      res.status(400).send(err)
    }
    else {
      res.sendStatus(200)
    }
  })
})
```

`GET /api/sushiList` を作る
```
async function getCount () {
  return new Promise((resolve, reject) => {
    memcached.get('count', (err, result) => {
      if (err) return reject(err)
      if (typeof result === 'number') return resolve(result)
      resolve(0)
    })
  })
}

async function getSushiList (count) {
  return new Promise((resolve, reject) => {
    if (!count) return resolve([])
    const ids = new Array(count).fill(0).map((_, i) => i + 1) // XXX: fill(0)いる？
    memcached.getMulti(ids.map(id => `sushi:${id}`), (err, results) => {
      if (err) return reject(err)
      resolve(ids.map(id => results[`sushi:${id}`]))
    })
  })
}

app.get('/api/sushiList', async (_, res) => {
  const count = await getCount()
  const sushiList = await getSushiList(count)
  res.send({ sushiList });
});
```

frontendを修正してgenerateとsushiListを叩けるようにする
```
cd frontend
npm install --save @uniqys/easy-client
```

`frontend/package.json` を修正
```
"serve": "vue-cli-service serve --port 3000",
```

`frontend/vue.config.js` を作成
CORS対策です
```
module.exports = {
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
      "/uniqys": {
        target: "http://localhost:8080",
        changeOrigin: true,
      }
    }
  }
}
```

**こっから難しいかも**

`frontend/src/App.vue`
```
import { EasyClientForBrowser } from '@uniqys/easy-client'
```

dataを修正 デフォルトはなにもなし
```
client: new EasyClientForBrowser('http://localhost:3000'),
myGari: 0,
myAddress: '',
sushiList: []
```

アドレスを取得
```
async fetchMyAddress() {
  this.myAddress = this.client.address.toString()
},
```

おすしリストを取得
```
async fetchSushiList() {
  const response = await this.client.get('/api/sushiList')
  const { sushiList } = response.data
  this.sushiList = sushiList
},
```

ページ更新時に取得してくる
```
created() {
  this.fetchMyAddress()
  this.fetchSushiList()
},
```

# Gari対応
## gariを取得できるようにする
```
cd backend/js
npm install --save axios
``` 

```js
app.get('/api/gari', async (req, res) => {
  const { address } = req.query
  const uri = `http://${INNER_API_HOST}:${INNER_API_PORT}/accounts/${address}/balance`
  const response = await axios.get(uri)
  const balance = response.data[0]
  res.send({ balance })
})
```

```js
created() {
  this.fetchMyAddress()
  this.fetchMyGari()
  this.fetchSushiList()
},

async fetchMyGari() {
  const response = await this.client.get('/api/gari', { params: { address: this.myAddress } })
  const { balance } = response.data
  this.myGari = balance
},
```

## Gariをもらうボタンを作る
```html
<button @click="tap()">Gariをもらう</button>
```
```js
async tap() {
  await this.client.post('/api/tap', {}, { sign: true })
  this.fetchMyGari()
},
```

backend
```js
app.post('/api/tap', async (req, res) => {
  const sender = req.header('uniqys-sender')

  const uri = `http://${INNER_API_HOST}:${INNER_API_PORT}/accounts/${sender}/balance`
  await axios.put(uri, JSON.stringify([10000]), { headers: { 'Content-Type': 'application/json' } })
  res.send()
})
```

## にぎるときにGariを減らしてみる

frontend
```js
async generate() {
  await this.client.post('/api/generate', {}, { sign: true })
  this.fetchSushiList()
  this.fetchMyGari()
},
```

backend
```js
const OPERATOR_ADDRESS = 'b8e6493bf64cae685095b162c4a4ee0645cde586'

async function transferGari(from, to, gari) {
  return new Promise(async (resolve) => {
    const uri = `http://${INNER_API_HOST}:${INNER_API_PORT}/accounts/${from}/transfer`
    await axios.post(uri, JSON.stringify({ to, value: parseInt(gari) }), { headers: { 'Content-Type': 'application/json' } })
    resolve()
  })
}

app.post('/api/generate', async (req, res) => {

  // ...

  await transferGari(sender, OPERATOR_ADDRESS, 100)
  res.send()
})
```

## 売ってみる

frontend
```js
async sell(sushi, price) {
  await this.client.post('/api/sell', { sushi, price }, { sign: true })
  this.fetchSushiList()
  this.fetchMyGari()
},
```

backend
```
app.post('/api/sell', async (req, res) => {
  const { sushi, price } = req.body

  const newSushi = Object.assign({}, sushi, {
    status: 'sell',
    price: price
  })

  memcached.set(`sushi:${sushi.id}`, newSushi, 0, (err) => {
    if (err) {
      res.status(400).send(err)
    }
    else {
      res.sendStatus(200)
    }
  })
})
```
*他の人のおすしも販売できちゃう・・*

## 買ってみる

frontend
```
async buy(sushi) {
  await this.client.post('/api/buy', { sushi }, { sign: true })
  this.fetchSushiList()
  this.fetchMyGari()
},
```

backend
```js
app.post('/api/buy', async (req, res) => {
  const sender = req.header('uniqys-sender')
  const { sushi } = req.body

  const newSushi = Object.assign({}, sushi, {
    status: 'normal',
    owner: sender,
    price: 0
  })

  await memcached.set(`sushi:${sushi.id}`, newSushi, 0, (err) => {
    if (err) {
      res.status(400).send(err)
    }
    else {
      res.sendStatus(200)
    }
  })
  await transferGari(sender, sushi.owner, sushi.price)
  res.send()
})
```
*売ってないおすしも、自分のおすしも買えちゃう・・*

# 追加課題
- にぎったとき、あたらしいおすしが後ろの方に追加されてしまい微妙です。いい感じにしてみましょう
- Gariがなくてもにぎったり購入したりができてしまいます。できないようにしてみましょう
- 他の人のおすしも販売できてしまいます。backendを修正してみましょう
- 売ってないおすしも、自分のおすしも買えてしまいます。backendを修正してみましょう
- 一回販売すると、キャンセルすることができません。キャンセルできるようにしてみましょう

# 他
## データをけしたい
```sh
cd backend
rm -rf .data
uniqys init ./dapp.json
```

## Error: dialed to the wrong peer, Ids do not match
何回か
```
Ctrl-c
uniqys start
```
を試してみてください