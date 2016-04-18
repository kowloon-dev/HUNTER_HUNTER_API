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
- uwsgi (2.0.12)
- Flask (0.10.1)
- Beautifulsoup4 (4.4.1)


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

$ git clone https://github.com/kowloon-dev/HUNTER_HUNTER_API.git
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
cd (デプロイ先ディレクトリ)/app
sudo python3 web_scraping.py
ls ../log/check_result.txt
check_result.txt   <--- check.reslut.txtが生成されていること
cat ../log/check_result.txt
2016-04-18        <--- 結果が記入されていること
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


