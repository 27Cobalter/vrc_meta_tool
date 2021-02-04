# vrc_meta_tool
# 注意
- 4/2のアップデートでデフォルトで`OnPlayerJoined`, `OnPlayerLeft`などのログが出力されなくなったためSteamから`プロパティ->起動オプションを設定`を開いて`--enable-sdk-log-levels`を追加してください
- コマンドプロンプトの仕様で初期設定でテキスト部分クリックすると止まるので特に支障がなければ[これ](https://twitter.com/27Cobalter/status/1189919007555510272?s=20)もやっておくと良い
## これは何
- VRChatで写真を撮ったときにワールド，撮影者，インスタンスにいる人，撮影時刻をpngに埋め込んで記録するツール

## ダウンロード
- https://github.com/27Cobalter/vrc_meta_tool/releases

## 自分で色々やりたい人向け
### 依存パッケージ
- pyyaml
- psutil
```
$ pip install -r requirements.txt
```

### 実行方法
- 書き込むとき
  - VRChatを起動した状態でvrc_meta_writerを起動
- 画像についているメタデータを読むとき
  - `vrc_meta_reader.exe file` で画像に付与されている情報を出力
  - `vrc_meta_reader.exe dir user_name`で対象ディレクトリ内のユーザが含まれる画像のパスを出力
  - またはvrc_meta_reader.exeに画像をドラッグアンドドロップ
  - がとーしょこらさんの[VRCPhotoAlbum](https://github.com/gatosyocora/VRCPhotoAlbum)を使うと画像を見ながらメタ情報の検索，閲覧ができます

## 設定ファイル
- 例
- config.yml
```config.yml
# 読み込むログファイルの指定　過去のログファイルから画像にタグ付けする場合に使用
log_file: ""
# メタデータを付与した写真を保存するディレクトリ
out_dir: "meta_pic"
```

- user_list.yml
  - [自分の使ってるやつ](https://gist.github.com/27Cobalter/ddf341ba31395ab56bff82b4f0fc50b5)
```user_list.yml
# nameにVRChatのユーザ名，screen_nameをTwitterのスクリーンネームにしておくとTwitterのスクリーンネームも保存してくれる
- name: "27Cobalter"
  screen_name: "@27Cobalter"
- name: "bootjp／ぶーと"
  screen_name: "@bootjp"
```

- `user_list.yml`の編集後に`user_list_sorter.exe`にドラッグアンドドロップするとキー値の昇順にソートされます(必要はないけど気になる人向け)
