EasyMTask
=========
![Development status: Inactive](https://img.shields.io/badge/Development%20status-Inactive-red.svg)
![Progress: Alpha](https://img.shields.io/badge/Progress-Alpha-orange.svg)

やりたいこと
------------
* 空メール送信でタスク一覧取得
* メール送信でタスク追加/変更/完了動作
* cronでタスク一覧を朝/夜に自動送信
* ~~cronで期日が近づいたら警告送信~~
* ~~cronで重要タスクの定期的な送信~~

Usage
-----
* Google App Engineにデプロイ
* `/admin`にアクセスし、許可するメールアドレスを登録
* 許可されたメールアドレスからメールを送信
  * 本文に`追加 <用件>`で追加
  * 空メールを送ることでタスクリストが帰ってくる
    * 現在、「完了」の動作のみ可能
  * 件名に`削除 完了`と入力して送ることで完了したタスクをDBから全削除
* `/cron/list`にcronを登録することで定時配信可能
