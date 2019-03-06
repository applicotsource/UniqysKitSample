# 環境構築
## frontend
```sh
mkdir messages
cd messages

# vue-cliのインストール
npm install -g @vue/cli # すでに入ってたら不要です
exec $SHELL -l # 必要あれば

# vueのプロジェクト作成
vue create frontend
# 全部Enterでオッケーです
```

### 動かしてみる
```
cd frontend
```

`package.json` を編集して、ポート番号を変更しておきます
```js
"serve": "vue-cli-service serve --port 3000",
```

実行します
```
npm run serve
```

ブラウザで `http://localhost:8080/` にアクセスすると、vueの最初のページが表示されるはずです。

### まっさらなページにしてみる
`frontend/src/App.vue` をきれいにします

```html
<template>
  <div id="app">
    <p>あああ</p>
  </div>
</template>
```

不要なcomponentsとimportも消します

ブラウザで確認するときれいになっているはずです。

### メッセージ送信用のフォームを設置してみる

inputとbuttonを設置します

```html
<template>
  <div id="app">
    <input type="text">
    <button>送信</button>
  </div>
</template>
```

### 入力した値が表示されるようにする

dataの中に変数を定義します

```js
// ...
export default {
  name: 'app',
  data() {
    return {
      input: ''
    }
  },
  // ...
}
```

フォームに入力した値がinput変数に入るようにします。ついでに下にその内容を表示するようにしてみます

```html
<template>
  <div id="app">
    <input type="text" v-model="input">
    <button>送信</button>
    <p>{{ input }}</p>
  </div>
</template>
```

フォームに入力すると、下の文字が変わることが確認できます。

### 結果を表示できるようにする
message変数に結果が入るようにしてみます

```js
data() {
  return {
    input: '',
    message: '結果だよ'
  }
},
methods: {
  submit() {
    this.message = this.input
  }
}
```

```html
<div id="app">
  <input type="text" v-model="input">
  <button @click="submit()">送信</button>
  <p>{{ message }}</p>
</div>
```

inputに文字を入力して送信を押してみると、messageの内容が書き換わることが確認できます。

## backend
https://cdn-images-1.medium.com/max/2600/1*kRWJUnGUh-txwPFZMKkWig.png

まず、uniqysのセットアップをします

uniqys-cliのインストール
```
npm install -g @uniqys/cli
```

```sh
# messages/
uniqys dev-init
ls -a # .data dapp.json uniqys.json frontend/ validatorKey.json
```

これでuniqysを開発開始できます

<!-- ここjsとpythonで出し分ける -->

`uniqys start` で一緒にappサーバを立ち上げることができます。その設定を`dapp.json` に書くことができます。

```json
}
  "startApp": "node backend/server.js"
}
```

これから、 `backend/server.js` にappサーバを実装していきます

```sh
mkdir backend
cd backend
npm init
# enter, enter ...
```

expressを使ってWebサーバを実装します

```sh
# backend/
npm install --save express body-parser memcached
```

```js
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

app.get('/hello', async (_, res) => {
  res.send('hello');
});

app.listen(APP_PORT, APP_HOST)
```

uniqysを立ち上げてみましょう
```sh
# /
uniqys start
```

`http://localhost:8080/hello` にアクセスしてみましょう。helloと出力されるはずです

Gateway(8080)を経由して、app(5650)を叩いています

早速messageを書き込み/読み込みできるようにしてみます

Uniqysでは、ブロックチェーンの情報をmemcachedプロトコルで操作することができます。

server.js
```js
async function getMessage () {
  return new Promise((resolve, reject) => {
    memcached.get('message', (err, result) => {
      if (err) return reject(err)
      if (typeof result === 'string') return resolve(result)
      resolve(0)
    })
  })
}

// 読み込み
app.get('/api/message', async (_, res) => {
  const message = await getMessage()
  res.send({ message });
})

// 書き込み
app.post('/api/message', async (req, res) => {
  // const sender = req.header('uniqys-sender')
  const { message } = req.body

  memcached.set(`message`, message, 0, (err) => {
    if (err) {
      res.status(400).send(err)
    }
    else {
      res.sendStatus(200)
    }
  })
})
```

`message` というキーで、メッセージを保存できるようにしてみました

# frontendとbackendをつなげる

さきほどfrontendで作成したフォームで、実際にブロックチェーンの情報を操作できるようにしてみます

## frontend

CORS対策のために、proxyを設定します

`frontend/vue.config.js`を作成し、以下のように設定します
```js
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
};
```

フロントエンドからGatewayを叩くとき、easy-clientを利用すると便利です

```sh
# frontend/
npm install --save @uniqys/easy-client
```

`frontend/src/App.vue`
```js
import { EasyClientForBrowser } from '@uniqys/easy-client'


data() {
  return {
    client: new EasyClientForBrowser('http://localhost:3000'),
  }
},
created() {
  this.fetch()
},
methods: {
  fetch() {
    this.client.get('/api/message').then((res) => {
      const message = res.data.message;
      this.message = message
    });
  },
  submit() {
    this.client.post('/api/message', { message: this.input }, { sign: true }).then(() => {
      this.fetch();
    })
  }
}
```

いちどuniqysのノードを `ctrl-c` で止め、もういちど `uniqys start` してみましょう
frontendを `ctrl-c` で止め、もういちど `npm serve` してみましょう

ブラウザからフォームを送信すると、メッセージをブロックチェーン上に書き込めていることがわかります

シークレットウインド胃で試しに実行してみてください。ブラウザを更新すると書き換わることが確認できます

次のステップでは、複数のメッセージが書き込めるように修正してみます
