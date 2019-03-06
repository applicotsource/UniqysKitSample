```
vue create frontend
cd frontend
npm run serve
```

App.vueのコンポーネントを消す

自分のアドレスを作ってみる
```
myAddress: '0xhogehoge'
```

おすしのデータを作ってみる
```
data() {
  return {
    sushiList: [
      {
        status: 'sell' | 'normal',
        price: number,
        owner: string,
        dna: string
      },
      ...
    ]
  }
}
```

おすしの枠を表示してみる

```
<div v-for="sushi in sushiList" :key="sushi.id">
      <p>{{ sushi.status }}</p>
      <p>{{ sushi.price }}</p>
      <p>{{ sushi.owner }}</p>
      <p>{{ sushi.dna }}</p>
    </div>
    ```

styleを当ててみる
```
    <div class="sushi-wrapper">
      <div class="sushi-box" v-for="sushi in sushiList" :key="sushi.id">
        <p>{{ sushi.status }}</p>
        <p>{{ sushi.price }}</p>
        <p>{{ sushi.owner }}</p>
        <p>{{ sushi.dna }}</p>
      </div>
    </div>

.sushi-wrapper {
  flex-wrap: wrap;
  display: flex;
}
.sushi-box {
  border: 1px solid black;
}
```

表示を整えてみる
```
<div class="sushi-box" v-for="sushi in sushiList" :key="sushi.id">
  <p>{{ myAddress === sushi.owner ? '私のおすし' : 'だれかのおすし' }}</p>
  <p>{{ sushi.dna }}</p>
  <p v-if="sushi.status === 'sell'">販売中</p>
  <p v-if="sushi.status === 'sell'">{{ sushi.price }} Gari</p>
</div>
```

DNAからおすしの表示パターンを計算してみる
```
<p>{{ code(sushi) }}</p>

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
```

Gariの概念を導入していく

```
<div>
  <p>address: {{ myAddress }}</p>
  <p>{{ myGari }} Gari</p>
</div>

myGari: 10000,

```

おすしをにぎってみる（仮）
```
<button @click="generate()">にぎる</button>

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

おすしを売ってみる（仮）
```
price: [],

sell(sushi, price) {
  sushi.status = 'sell'
  sushi.price = price
},

<div v-if="myAddress === sushi.owner && sushi.status === 'normal'">
  <input type="text" v-model="price[sushi.id]">
  <button @click="sell(sushi, price[sushi.id])">売る！</button>
</div>
```

おすしを買ってみる（仮）
```
price: 5000,

buy(sushi) {
  this.myGari -= sushi.price
  sushi.status = 'normal'
  sushi.price = 0
  sushi.owner = this.myAddress
},

<div v-if="myAddress !== sushi.owner && sushi.status === 'sell'">
  <button @click="buy(sushi)">買う！</button>
</div>

```
