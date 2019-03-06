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

