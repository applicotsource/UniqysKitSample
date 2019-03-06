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
```

# 他
## データをけしたい
```
cd backend
rm -rf .data
uniqys init ./dapp.json
```