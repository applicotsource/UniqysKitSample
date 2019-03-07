# Step 1
# 準備
frontendディレクトリを作成します

vue-cliがインストールされていない場合はインストールしてください
```sh
npm install -g @vue/cli # すでに入ってたら不要です
exec $SHELL -l # 必要あれば
```

vueが動くか確認してみます
```sh
mkdir sushi
cd sushi
vue create frontend # ぜんぶEnterでオッケーです
cd frontend
npm run serve
```

ブラウザで `http://localhost:8080/` にアクセスすると、vueの最初のページが表示されるはずです。

# おすしのモックを作っていく

## まっさらなページにしてみる
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

## 自分のアドレスを作ってみる
```js
data() {
  return {
    myAddress: '0xhogehoge',
  }
}

```

## おすしのデータを作ってみる
```js
data() {
  return {
    sushiList: [
      { // 自分の販売中じゃないおすし
        id: 1,
        status: 'normal',
        price: 0,
        owner: '0xhogehoge',
        dna: 'irjiorgoiwegjioergj'
      },
      { // 自分の販売中のおすし
        id: 2,
        status: 'sell',
        price: 0,
        owner: '0xhogehoge',
        dna: '0rtihij6i45h4jgioijerf'
      },
      { // 他の人の販売中じゃないおすし
        id: 3,
        status: 'normal',
        price: 0,
        owner: '0xhugahuga',
        dna: 'x3igwegjsij5gjj35p4hi45h'
      },
      { // 他の人の販売中のおすし
        id: 4,
        status: 'sell',
        price: 5000,
        owner: '0xhugahuga',
        dna: 'irjiorgoiwegjioergj'
      },
    ]
  }
}
```

## おすしの枠を表示してみる

```html
<div v-for="sushi in sushiList" :key="sushi.id">
  <p>{{ sushi.status }}</p>
  <p>{{ sushi.price }}</p>
  <p>{{ sushi.owner }}</p>
  <p>{{ sushi.dna }}</p>
</div>
```

## styleを当ててみる
```html
<div class="sushi-wrapper">
  <div class="sushi-box" v-for="sushi in sushiList" :key="sushi.id">
    <p>{{ sushi.status }}</p>
    <p>{{ sushi.price }}</p>
    <p>{{ sushi.owner }}</p>
    <p>{{ sushi.dna }}</p>
  </div>
</div>
```

```css
.sushi-wrapper {
  flex-wrap: wrap;
  display: flex;
}
.sushi-box {
  width: 200px;
  height: 300px;
  margin: 8px;
  border: 1px solid black;
}
```

## 表示を整えてみる
```html
<div class="sushi-box" v-for="sushi in sushiList" :key="sushi.id">
  <p>{{ myAddress === sushi.owner ? '私のおすし' : 'だれかのおすし' }}</p>
  <p>{{ sushi.dna }}</p>
  <p v-if="sushi.status === 'sell'">販売中</p>
  <p v-if="sushi.status === 'sell'">{{ sushi.price }} Gari</p>
</div>
```

## DNAからおすしの表示パターンを計算してみる
```html
<div class="sushi-box" v-for="sushi in sushiList" :key="sushi.id">
  <p>{{ myAddress === sushi.owner ? '私のおすし' : 'だれかのおすし' }}</p>
  <p>{{ code(sushi) }}</p>
  <p v-if="sushi.status === 'sell'">販売中</p>
  <p v-if="sushi.status === 'sell'">{{ sushi.price }} Gari</p>
</div>
```

```js
export default {
  methods: {
    code(sushi) {
      const dna = new Buffer(sushi.dna)
      return {
        dish: dna.readUInt16BE(0) % 10,
        neta: dna.readUInt16BE(4) % 10,
        spice: dna.readUInt16BE(8) % 10,
      }
    }
  },
}
```

## Gariの概念を導入していく

```html
<div>
  <p>address: {{ myAddress }}</p>
  <p>{{ myGari }} Gari</p>
</div>
```

```js
data() {
  return {
    myGari: 10000,
  }
}
```

## おすしをにぎってみる（仮）
```html
<button @click="generate()">にぎる</button>
```

```js
generate() {
  const newId = this.sushiList.length + 1
  this.myGari -= 100
  this.sushiList.unshift({
    id: newId,
    status: 'normal',
    price: 0,
    owner: this.myAddress,
    dna: Math.random().toString(36) // ランダムな文字列を生成
  })
},
```

## おすしを売ってみる（仮）
```html
<div v-if="myAddress === sushi.owner && sushi.status === 'normal'">
  <input type="text" placeholder="販売額" v-model="price[sushi.id]">
  <button @click="sell(sushi, price[sushi.id])">売る！</button>
</div>
```

```js
data() {
  return {
    price: [],
  }
}
methods: {
  sell(sushi, price) {
    sushi.status = 'sell'
    sushi.price = price
  },
}
```

## おすしを買ってみる（仮）
```html
<div v-if="myAddress !== sushi.owner && sushi.status === 'sell'">
  <button @click="buy(sushi)">買う！</button>
</div>
```

```js
buy(sushi) {
  this.myGari -= sushi.price
  sushi.status = 'normal'
  sushi.price = 0
  sushi.owner = this.myAddress
},
```

## おすし画像を作ってみる
いまcode(sushi)してるとこ
```html
<div class="sushi-image-box">
  <img :src="`/img/sushi/dish/dish-0${code(sushi).dish}.png`" alt="">
  <img :src="`/img/sushi/syari/syari.png`" alt="">
  <img :src="`/img/sushi/neta/neta-0${code(sushi).neta}.png`" alt="">
  <img :src="`/img/sushi/spice/spice-0${code(sushi).spice}.png`" alt="">
</div>
```

```css
.sushi-image-box {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto;
}
.sushi-image-box img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100px;
  height: 100px;
}
```
