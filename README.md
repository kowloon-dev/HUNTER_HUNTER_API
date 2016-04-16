# HUNTER_HUNTER_API

## 概要
週刊少年ジャンプ最新号に『HUNTER×HUNTER』が掲載されているか否か
を確認できるWeb APIです。

## 使い方
APIエンドポイントにGETメソッドでリクエストすると、JSON形式で応答します。


### API Endpoint
[http://goo.gl/CdcUIG](http://goo.gl/CdcUIG)

### レスポンス書式


{
  "date": "2016-04-16",
  "status": "True",
  "title": "\u80cc\u3059\u3058\u3092\u30d4\u30f3\uff01\u3068\u301c\u9e7f\u9ad8\u7af6\u6280\u30c0\u30f3\u30b9\u90e8\u3078\u3088\u3046\u3053\u305d\u301c"
}

+   `date` :  
    掲載情報を確認した日付を"YYYY-MM-DD"形式で示します。


+   `status` :  
    『HUNTER×HUNTER』のジャンプ掲載状況を示します。  
    掲載されている時は『True』、掲載されていない時は『False』を返します。

+   `title` :  
    確認対象の作品タイトルを示します。
    Unicodeエスケープされた文字列で応答します。

