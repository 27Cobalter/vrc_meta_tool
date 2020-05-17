# vrc_meta_tool
# 注意
- 4/2のアップデートでデフォルトで`OnPlayerJoined`, `OnPlayerLeft`などのログが出力されなくなったためSteamから`プロパティ->起動オプションを設定`を開いて`--enable-sdk-log-levels`を追加してください
- コマンドプロンプトの仕様で初期設定でテキスト部分クリックすると止まるので特に支障がなければ[これ](https://twitter.com/27Cobalter/status/1189919007555510272?s=20)もやっておくと良い
## これは何
- VRChatで写真を撮ったときにワールド，インスタンスにいる人，撮影時刻をpngに埋め込んで記録するツール

## ダウンロード
- https://github.com/27Cobalter/vrc_meta_tool/releases

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
  - `vrc_meta_reader.exe file` で画像に付与されている情報を出力
  - `vrc_meta_reader.exe dir user_name`で対象ディレクトリ内のユーザが含まれる画像のパスを出力
  - またはreader.batに画像をドラッグアンドドロップ

## 設定ファイル
- 例
```config.yml
# 読み込むログファイルの指定　過去のログファイルから画像にタグ付けする場合に使用
log_file: ""
# メタデータを付与した写真を保存するディレクトリ
out_dir: "meta_pic"
```
