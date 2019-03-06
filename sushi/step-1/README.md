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