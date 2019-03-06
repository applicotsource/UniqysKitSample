```
mkdir backend
mkdir backend/js
cd backend/js
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

`POST '/api/sushi'` を作る
```