# Q&A
## データを消したい
uniqys initしたディレクトリで以下を実行してください

```sh
rm -rf .data
uniqys init ./dapp.json
```

## `Error: dialed to the wrong peer, Ids do not match` というエラーがでる
既知のバグで、原因不明です・・

何回か以下を試してみてください
```
ctrl-c
uniqys start
```

直していただけるひと[募集中](https://github.com/uniqys/UniqysKit)