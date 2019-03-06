const express = require("express")
const bodyParser = require("body-parser")
const Memcached = require("memcached")
const keccak = require('keccak')

const APP_HOST = '0.0.0.0'
const APP_PORT = 5650
const DB_HOST = 'localhost'
const DB_PORT = 5652

const app = express()
const memcached = new Memcached(`${DB_HOST}:${DB_PORT}`)

app.use(bodyParser())

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

app.listen(APP_PORT, APP_HOST)