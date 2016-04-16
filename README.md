# HUNTER_HUNTER_API

## 概要
週刊少年ジャンプ最新号での『HUNTER×HUNTER』掲載状況を確認できるWeb APIです。

## 使い方
APIエンドポイントにGETメソッドでリクエストすると、JSON形式で応答します。


### APIエンドポイント
[http://goo.gl/CdcUIG](http://goo.gl/CdcUIG)

### レスポンス書式

レスポンスの例

```
{
  "date": "2016-04-16",
  "status": "True",
  "title": "\u80cc\u3059\u3058\u3092\u30d4\u30f3\uff01\u3068\u301c\u9e7f\u9ad8\u7af6\u6280\u30c0\u30f3\u30b9\u90e8\u3078\u3088\u3046\u3053\u305d\u301c"
}
```

+   `date` :  
    掲載状況を確認した日付を"YYYY-MM-DD"形式で返します。  
    API利用者はこの日付を基に、情報の新旧を判断します。  
    (掲載状況の確認処理は[app/web_scraping.py](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/app/web_scraping.py)で自動化されています)

+   `status` :  
    『HUNTER×HUNTER』のジャンプ掲載状況を返します。  
    掲載されている時は『True』、掲載されていない時は『False』を返します。

+   `title` :  
    確認対象の作品タイトルを返します。  
    Unicodeエスケープされた文字列で応答します。


## 補足
設定ファイル[config/config.ini](https://github.com/kowloon-dev/HUNTER_HUNTER_API/blob/master/config/config.ini)内の
**[GetWebsite]**セクションの**title**値を編集することで、  
任意の作品を確認対象に変更することが可能です。  
ただし、対象は[今号のジャンプ情報](https://www.shonenjump.com/j/weeklyshonenjump/)ページの作品一覧に掲載されるものに限られます。
