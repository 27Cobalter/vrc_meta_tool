# vrc_meta_tool
# 注意
- 4/2のアップデートでデフォルトで`OnPlayerJoined`, `OnPlayerLeft`などのログが出力されなくなったためSteamから`プロパティ->起動オプションを設定`を開いて`--enable-sdk-log-levels`を追加してください
## これは何
- VRChatで写真を撮ったときにワールド，インスタンスにいる人，撮影時刻をpngに埋め込んで記録するツール

## ダウンロード
- まだ

## 自分で色々やりたい人向け
### 依存パッケージ
- pyyaml
```
$ pip install pyyaml
```

### 実行方法
- 書き込むとき
  - VRChatを起動した状態でvrc_meta_writerを起動
- 画像についているメタデータを読むとき
  - vrc_meta_readerの引数として画像ファイルのパスを与える
  - またはreader.batに画像をドラッグアンドドロップ

## 設定ファイル
- 例
```config.yml
# 読み込むログファイルの指定　過去のログファイルから画像にタグ付けする場合に使用
log_file: ""
# メタデータを付与した写真を保存するディレクトリ
out_dir: "meta_pic"
```
