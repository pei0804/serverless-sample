# サーバーレス(主にAWS Lambda)

Lambda上では、任意のコードが動く。例えばMySQLのようなRDBMSとのやり取りも出来ますが、データベースはマネージとなサービスではないので、スケーリングする上でボトルネックになります。そもそも、管理が必要なものと組み合わせるのはサーバーレスの恩恵を得られにくい。管理不要なサービス同士組み合わせるのが理想。   

**RestfulAPIっぽいWebAPIの例**  

- API Gateway ユーザーとの通信部分
- Lambda アプリケーション固有のロジック
- DynamoDB データストア

アプリケーションを組む上で、中心となるLambdaのコードをどう書くか？  
というのも、突然サービスが終了したり、もっと価格が安いものが出てきたらどうするとか、Dockerでもっと便利に！とかがあるので、Lambdaでしか動かないコードにしていると移行コストが高いです。

## 互換性をもたせる

**WSGI互換**  

Pythonの場合、WSGI(Web Server Gateway Interface)というインタフェースに準拠することで、移行が簡単になります。ちなみにDjangoやFlaskで書いたアプリケーションは既にWSGI互換になっている。

**LambdaをWSGI互換にするには**

LambdaはWSGIに対応していません。なので、WSGIにへんかんしてしまうということをするのが１つです。AWSGIを使えばそれが出来ます。  
またAPI Gateway側でLambdaを指定するよりも、プロキシ統合と呼ばれるアプリケーション側、つまりLambda側でパスやメソッドをハンドリングした方が都合が良いです。プロキシ統合は、API Gatewayに来たリクエストをまるごとバックエンド側に送ることで実現可能です。こうすることで、動いている場所を気にせずアプリケーションを組むことが可能となります。

ちなみにGoの場合は、Lambdaの方が標準パッケージに準拠してくれている（神）  


## Apexを使ったデプロイ

関数をアップロードするには、関連するライブラリ全てを落としてきて、ZIPに圧縮し、出来上がったファイルを管理画面からアップロードという手順が必要です。それらをいい感じにしてくれるのが、Apexです。  

インストールコマンド  

```
$ curl https://raw.githubusercontent.com/apex/apex/master/install.sh | sh
```

.awsなどにクレデンシャルの設定とかやってる前提

```
~/go/src/github.com/pei0804/serverless-sample master*
❯ mkdir wsgiapp

~/go/src/github.com/pei0804/serverless-sample master*
❯ cd wsgiapp

~/go/src/github.com/pei0804/serverless-sample/wsgiapp master*
❯ apex init


             _    ____  _______  __
            / \  |  _ \| ____\ \/ /
           / _ \ | |_) |  _|  \  /
          / ___ \|  __/| |___ /  \
         /_/   \_\_|   |_____/_/\_\



  Enter the name of your project. It should be machine-friendly, as this
  is used to prefix your functions in Lambda.

    Project name: wsgiapp

  Enter an optional description of your project.

    Project description: wsgi app function

  [+] creating IAM wsgiapp_lambda_function role
  [+] creating IAM wsgiapp_lambda_logs policy
  [+] attaching policy to lambda_function role.
  [+] creating ./project.json
  [+] creating ./functions

  Setup complete, deploy those functions!

    $ apex deploy


~/go/src/github.com/pei0804/serverless-sample/wsgiapp master* 1m 47s
❯ ls
functions    project.json

~/go/src/github.com/pei0804/serverless-sample/wsgiapp master*
❯ cat project.json
{
  "name": "wsgiapp",
  "description": "wsgi app function",
  "memory": 128,
  "timeout": 5,
  "role": "arn:aws:iam::851669633371:role/wsgiapp_lambda_function",
  "environment": {}
}
```

タイムアウト時間とかメモリ料を設定ファイルで管理出来る。

```
~/go/src/github.com/pei0804/serverless-sample/wsgiapp/src master* 6s
❯ FLASK_APP=wsgiapp.main:app python3 -m flask run
 * Serving Flask app "wsgiapp.main:app"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

~/go/src/github.com/pei0804/serverless-sample master*
❯ curl http://127.0.0.1:5000/    {"message":"Hello serverless WSGI world!!"}
```

### ライブラリの管理

apex deployコマンドを実行すると、デプロイされますが、この時アップロードされるのは、functions/wsgiappの中身だけとなります。なので、自前で作成したパッケージやライブラリなどは取り込まれません。そのためには、合わせてアップロード出来るようにする必要があります。
pipには-tオプションがあり、これを使うことで任意の場所にライブラリをインストール出来ます。これとapexのhookを組み合わさることでアップロードが意図通り出来ます。

```
  "hooks": {
    "build": "cp -r ../../src/* . && pip install -r ../../requirements.txt -t ./vendor"
  }
```

## 参考

- WebDB vol104 サーバーレス
- [API GatewayとLambdaでAPI作成のチュートリアル](https://qiita.com/vankobe/items/ab5bc6487c7e07cb3aba)
