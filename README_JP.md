# kogi2ics

[中文](README.md) | 日本語 | [English](README_EN.md)

`kogi2ics` は、KCG.EDU(京都コンピュータ学院・京都情報大学院大学) の授業データを `.ics` カレンダーファイルとして書き出すための小さなツールです。

このプロジェクトは主に次の 2 つの Python ファイルで構成されています。

- [getkogi.py](/e:/京都情报/getkogi/getkogi.py): メインファイル。KCGI Portal API から授業データを取得し、`kogi.json` と `kogi.ics` を生成します
- [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py): 変換モジュール。授業 JSON を `.ics` に変換します

### 処理の流れ

1. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) が KCGI Portal API を呼び出す
2. レスポンスを `kogi.json` として保存する
3. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) が [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py) の `write_ics(...)` を呼び出す
4. `kogi.ics` を出力する

### 機能

- KCGI の授業予定 JSON を取得
- `tooltip` から授業名、日付、`時限`、教室を抽出
- `時限` を実際の授業時間へ変換
- 教室の校舎名を自動補完
  - `M` = `KCGI百万遍キャンパス南校舎`
  - `H` = `KCGI百万遍キャンパス本部棟`
- `Asia/Tokyo` タイムゾーンの標準 `.ics` ファイルを生成

### 動作環境

- Python 3.10 以上
- `requests`

依存関係のインストール：

```bash
pip install requests
```

### 使い方

メインファイルを実行します。

```bash
python getkogi.py -c "YOUR_COOKIE" -x "YOUR_X_CPAUTHORIZE" -t 1
```

引数：

- `-c`, `--cookie`: ログイン後の Cookie
- `-x`, `--x`: リクエストヘッダーの `x-cpauthorize`
- `-t`, `--term`: 学期。`1` は春学期、`2` は秋学期

実行後に生成されるファイル：

- `kogi.json`
- `kogi.ics`

すでに `kogi.json` がある場合は、変換モジュールだけを実行することもできます。

```bash
python generate_ics.py -i kogi.json -o kogi.ics
```

### 授業時間

時限ごとの時間はコード内に直接定義されています。

- 第1限 `09:30-11:00`
- 第2限 `11:10-12:40`
- 第3限 `13:30-15:00`
- 第4限 `15:10-16:40`
- 第5限 `16:50-18:20`
- 第6限 `18:30-20:00`
- 第7限 `20:10-21:40`

### カレンダーへの取り込み

#### Apple カレンダー

`.ics` の取り込みには次のショートカットを使えます。

`https://routinehub.co/shortcut/7005/`

#### Android カレンダー

Android で `.ics` を直接取り込めるかどうかは、使用するカレンダーアプリによって異なります。

- ローカルの `.ics` を直接開けるアプリがあります
- スマホ上で直接インポートできないアプリもあります
- Google Calendar を使う場合は、Web 版で先に `.ics` を読み込んで同期する方法が比較的確実です

まずは `kogi.ics` を直接開いて試し、うまくいかなければ Web 版や `.ics` 対応アプリを使うのがおすすめです。