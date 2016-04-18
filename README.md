# HUNTER_HUNTER_API

## 概要
週刊少年ジャンプ最新号での『HUNTER×HUNTER』掲載状況を確認できるWeb APIです。

## 使い方
APIエンドポイントにGETメソッドでリクエストすると、JSON形式で応答します。

### APIエンドポイント
以下のデモサイトURLにて実際に本APIを稼働させています。  
[http://ec2-54-187-190-118.us-west-2.compute.amazonaws.com/jump-api/1.0/](http://ec2-54-187-190-118.us-west-2.compute.amazonaws.com/jump-api/1.0/)


### レスポンス書式

レスポンスの例

```
{
  "date": "2016-04-18",
  "status": "True",
  "title": "HUNTER\u00d7HUNTER"
}
```

+   `date` :  
    掲載状況を確認した日付を"YYYY-MM-DD"形式で返します。  
    この日付情報を基に、API利用者が情報の新旧を判断できることを目的としています。  
    (掲載状況の確認処理は[app/web_scraping.py](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/app/web_scraping.py)で自動化されています)

+   `status` :  
    『HUNTER×HUNTER』のジャンプ掲載状況を返します。  
    掲載されている時は『True』、掲載されていない時は『False』を返します。

+   `title` :  
    確認対象の作品タイトルを返します。  
    Unicodeエスケープされた文字列ですので、マルチバイト文字の部分は「\u(コード番号)」となります。  
    上記の例ですと「×」の文字が[Unicode番号00d7](http://www.fileformat.info/info/unicode/char/00d7/index.htm)として表示されています。


## カスタマイズ
設定ファイル[config/config.ini](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/config/config.ini)内の
**[GetWebsite]**セクションの**title**値を編集することで、  
任意の作品を確認対象に変更することが可能です。  
ただし、対象は[今号のジャンプ情報](https://www.shonenjump.com/j/weeklyshonenjump/)ページの作品一覧に掲載されるものに限られます。

## デプロイ

自前の環境にて本APIを稼働させる場合の手順です。 

前提として以下のコンポーネントが必要です。(括弧内は確認済みバージョン)

- Nginx (1.4.6 (Ubuntu))
- Python3 (3.4.3)
- uWSGI (2.0.12)
- Flask (0.10.1)
- Beautifulsoup4 (4.4.1)

以下のOS環境にて動作確認済みです。

- Mac OS X(10.10.5)
- Ubuntu14.04 


### 各コンポーネントのインストール

```
sudo apt-get install nginx  
sudo pip3 install uwsgi  
sudo pip3 install flask  
sudo pip3 install bs4  

# uWSGIのログ出力先を作成
$ sudo mkdir /var/log/uwsgi
$ sudo touch /var/log/uwsgi/uwsgi.log
$ ls -ld /var/log/uwsgi/uwsgi.log
-rw-r--r-- 1 root root 0 Apr 16 14:55 /var/log/uwsgi/uwsgi.log
```

### スクリプト一式をclone

例として/data/配下に配置する場合を記載します。  

```
$ sudo mkdir /data
$ ls -ld /data/
drwxr-xr-x 5 root root 4096 Apr 16 14:51 /data/

$ cd /data/
$ pwd
/data

$ sudo git clone https://github.com/kowloon-dev/HUNTER_HUNTER_API.git
$ ls -l
drwxr-xr-x 5 root root 4096 Apr 16 14:51 HUNTER_HUNTER_API

$ ls -l HUNTER_HUNTER_API/
total 12
drwxr-xr-x 3 root root 4096 Apr 16 14:58 app
drwxr-xr-x 2 root root 4096 Apr 16 14:51 config
-rw-r--r-- 1 root root  142 Apr 16 14:51 README.md

# logディレクトリを作成
$ sudo mkdir HUNTER_HUNTER_API/log
$ ls -l
drwxr-xr-x 3 root root 4096 Apr 16 14:58 app
drwxr-xr-x 2 root root 4096 Apr 16 14:51 config
drwxr-xr-x 2 root root 4096 Apr 16 15:03 log
-rw-r--r-- 1 root root  142 Apr 16 14:51 README.md
```

### Nginxの設定ファイルを編集

nginxの設定ファイルに以下を追記。  
/etc/nginx/sites-available/default (Ubuntuの場合)

```
        location /jump-api {
                 uwsgi_pass     localhost:8000;
                 include        uwsgi_params;
        }
```

Webサーバの「/jump-api」パスへのアクセスはローカルホストの8000番に渡すように指定しています。  
8000番ではuWSGIが待ち受けており、Pythonに処理が渡ります。  
  
【重要】  
デプロイ先の環境で既にポート8000番が使用されている場合にはポート重複が発生します。  
その場合は[config/config_uwsig.ini](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/config/config_uwsgi.ini)内の
**socket = localhost:8000**のポート番号を変更して下さい。  
nginxの設定ファイルのポート番号部分も合わせて修正して下さい。


本当はポート番号を消費せずにsocketファイル渡しにしたかったのですが、  
どうしてもうまく動かず諦めた経緯があります。  

Nginxを再起動  
```
$ sudo /etc/ini.d/nginx restart
$ sudo /etc/init.d/nginx status
 * nginx is running
```

### uWSGIを起動

```
$ sudo uwsgi --ini /data/HUNTER_HUNTER_API/config/config_uwsgi.ini &
```

### テスト実行

Webのスクレイピングが成功するか確認  
```
sudo /data/HUNTER_HUNTER_API/app/python3 web_scraping.py  <--絶対パスで指定
ls ../log/check_result.txt
check_result.txt         <--- check.reslut.txtが生成されていること
cat ../log/check_result.txt
2016-04-18               <--- 結果が記入されていること
HUNTER×HUNTER
True
```

上記が確認できたらAPIエンドポイントにブラウザでアクセスします。  
http://(デプロイ先サーバのIP or FQDN)/jump-api/1.0/  

APIのレスポンスが表示されることを確認します。

```
{
  "date": "2016-04-18",
  "status": "True",
  "title": "HUNTER\u00d7HUNTER"
}
```

### 定期実行登録

週に1回、月曜日に[app/web_scraping.py](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/app/web_scraping.py)を
自動実行するようcronに登録します。

公式サイトが更新されるのは月曜の午前11時頃のように見受けられましたので、
本デモサイトでは毎週月曜12:00に実行するように指定しています。

```
sudo crontab -e

00 12 * * 1 python3 /data/HUNTER_HUNTER_API/app/web_scraping.py
```

---

## 他サービスでの利用例

『HUNTER×HUNTERの掲載状況』を本API層で抽象化できましたので、外部サービスからの利用が容易となりました。  
早速利用してみます。  

### HUNTER×HUNTER掲載通知メール

例として**本APIを叩いてTrueが返ってきたらメールで通知するサービス**を作りました。  


[app/mail_notify.py](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/app/mail_notify.py)をcron等で週1回定期実行することで、
**HUNTER×HUNTERのジャンプ掲載状況**がメール通知されます。


実際にメール通知された例  

![HUNTER_mail_notify](http://kowloonet.org/github-files/HUNTER_mail_notify.png)

### 使い方
[config/config_mail.ini](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/config/config_mail.ini)内の
**[Mail]**セクションに値を指定します。  
各利用者のメール環境に合わせて修正してください。  

[Mail]セクションの解説

+   `api_url` :  
    問い合わせを行うAPIエンドポイント。  
    サンプルではデモサイトのAPIエンドポイントURLを指定してあり、このまま変更しなくても利用可能です。

+   `smtp_host` :  
    SMTPホスト名を指定します。

+   `smtp_port` :  
    SMTPポート番号。  
    SMTP認証を使う想定でサブミッションポート"587"を指定してあります。

+   `local_host` :  
    SMTPサーバとの通信時に名乗るローカルホスト名。

+   `smtpauth_id` :  
    SMTPAUTHのユーザIDを指定します。

+   `smtpauth_pass` :  
    SMTPAUTHのパスワードを指定します。

+   `from_addr` :  
    通知メールの送信元アドレス。

+   `to_addr` :  
    通知メールの宛先アドレス。

+   `mail_title` :  
    メールのタイトルを指定します。
    サンプルでは「ジャンプ掲載通知」としてあります。


あとはcronで定期実行するように指定します。  
デモサイトの情報は毎週月曜12時に更新されるようにしてありますので、  
その少し後の時間を指定します。

```
sudo crontab -e

05 12 * * 1 python3 /data/HUNTER_HUNTER_API/app/mail_notify.py
```