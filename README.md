# HUNTER_HUNTER_API

## 概要
週刊少年ジャンプ最新号での『HUNTER×HUNTER』掲載状況を確認できるWeb APIです。

## 使い方
APIエンドポイントにGETメソッドでリクエストすると、JSON形式で応答します。

### APIエンドポイント
以下のデモサイトURLにてAPIを稼働させています。  
[http://ec2-54-187-190-118.us-west-2.compute.amazonaws.com/api/jump/1.0/](http://ec2-54-187-190-118.us-west-2.compute.amazonaws.com/api/jump/1.0/)

短縮URL:  
[http://goo.gl/CdcUIG](http://goo.gl/CdcUIG)

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
