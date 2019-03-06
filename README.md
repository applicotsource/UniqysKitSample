# Get Started

**start backend**
```
cd messages/step-1
uniqys init ./dapp.json
uniqys start
```

**start frontend**
```
cd messages/step-1/frontend
npm install
npm run serve
```

# Backend
## 言語の変更
`uniqys start` でアプリケーションを同時に開始することができる

`dapp.json` の `startApp` に記載されたコマンドが実行される

コマンドを変更すれば、実行される言語を切替できる

**javascript**
```dapp.json:json
{
  "startApp": "node backend/js/server.js"
}
```

**python**
```dapp.json:json
{
  "startApp": "python backend/python/server.py"
}
```