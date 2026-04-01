# getkogi

[中文](#中文) | [日本語](#日本語) | [English](#english)

## 中文

`getkogi` 是一个把 KCG.EDU(京都コンピュータ学院、京都情报大学院大学) 的课程数据导出为 `.ics` 日历文件的小工具。

这个项目主要围绕两个 Python 文件：

- [getkogi.py](/e:/京都情报/getkogi/getkogi.py): 主文件。负责从 KCGI Portal API 获取课程数据，并生成 `kogi.json` 和 `kogi.ics`
- [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py): 转换模块。负责把课程 JSON 转换成 `.ics`

### 工作流程

1. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) 请求 KCGI Portal API
2. 返回结果保存为 `kogi.json`
3. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) 调用 [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py) 中的 `write_ics(...)`
4. 输出 `kogi.ics`

### 功能

- 获取 KCGI 课程日程 JSON
- 从 `tooltip` 中提取课程名称、日期、`時限`、教室
- 按节次转换成真实上课时间
- 自动补全教室所在校区
  - `M` = `KCGI百万遍キャンパス南校舎`
  - `H` = `KCGI百万遍キャンパス本部棟`
- 生成 `Asia/Tokyo` 时区的标准 `.ics` 文件

### 环境要求

- Python 3.10+
- `requests`

安装依赖：

```bash
pip install requests
```

### 用法

运行主文件：

```bash
python getkogi.py -c "YOUR_COOKIE" -x "YOUR_X_CPAUTHORIZE" -t 1
```

参数说明：

- `-c`, `--cookie`: 登录后的 Cookie
- `-x`, `--x`: 请求头中的 `x-cpauthorize`
- `-t`, `--term`: 学期，`1` 为春学期，`2` 为秋学期

执行后会生成：

- `kogi.json`
- `kogi.ics`

如果你已经有 `kogi.json`，也可以单独运行转换模块：

```bash
python generate_ics.py -i kogi.json -o kogi.ics
```

### 上课时间

节次时间已经直接写在代码中：

- 第1节 `09:30-11:00`
- 第2节 `11:10-12:40`
- 第3节 `13:30-15:00`
- 第4节 `15:10-16:40`
- 第5节 `16:50-18:20`
- 第6节 `18:30-20:00`
- 第7节 `20:10-21:40`

### 导入日历

#### Apple 日历

可以使用这个快捷指令导入 `.ics`：

`https://routinehub.co/shortcut/7005/`

#### Android 日历

Android 是否能直接导入 `.ics`，取决于你使用的日历应用。

- 有些应用支持直接打开本地 `.ics`
- 有些应用不支持手机端直接导入
- 如果你用 Google Calendar，更稳妥的方式通常是先在网页端导入，再同步到手机

所以建议先尝试直接打开 `kogi.ics`；如果不行，再改用网页端或支持 `.ics` 的第三方日历应用。

---

## 日本語

`getkogi` は、KCGI の授業データを `.ics` カレンダーファイルとして書き出すための小さなツールです。

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

---

## English

`getkogi` is a small tool for exporting KCGI class data as `.ics` calendar files.

This project is centered around two Python files:

- [getkogi.py](/e:/京都情报/getkogi/getkogi.py): the main entry point. It fetches class data from the KCGI Portal API and generates `kogi.json` and `kogi.ics`
- [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py): the conversion module. It converts class JSON into `.ics`

### Flow

1. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) calls the KCGI Portal API
2. The response is saved as `kogi.json`
3. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) calls `write_ics(...)` from [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py)
4. `kogi.ics` is written

### Features

- Fetches KCGI class schedule JSON
- Extracts class title, date, `時限`, and room from `tooltip`
- Converts class periods into actual class times
- Expands room prefixes into campus names
  - `M` = `KCGI百万遍キャンパス南校舎`
  - `H` = `KCGI百万遍キャンパス本部棟`
- Generates a standard `.ics` file in the `Asia/Tokyo` timezone

### Requirements

- Python 3.10+
- `requests`

Install dependencies:

```bash
pip install requests
```

### Usage

Run the main file:

```bash
python getkogi.py -c "YOUR_COOKIE" -x "YOUR_X_CPAUTHORIZE" -t 1
```

Arguments:

- `-c`, `--cookie`: your logged-in cookie
- `-x`, `--x`: the `x-cpauthorize` request header
- `-t`, `--term`: school term, `1` for spring and `2` for autumn

This generates:

- `kogi.json`
- `kogi.ics`

If you already have `kogi.json`, you can also run the conversion module directly:

```bash
python generate_ics.py -i kogi.json -o kogi.ics
```

### Class periods

The class period schedule is embedded directly in the code:

- Period 1 `09:30-11:00`
- Period 2 `11:10-12:40`
- Period 3 `13:30-15:00`
- Period 4 `15:10-16:40`
- Period 5 `16:50-18:20`
- Period 6 `18:30-20:00`
- Period 7 `20:10-21:40`

### Calendar import

#### Apple Calendar

You can use this Shortcut to import the `.ics` file:

`https://routinehub.co/shortcut/7005/`

#### Android calendars

Whether Android can import `.ics` directly depends on the calendar app you use.

- Some apps can open a local `.ics` file directly
- Some apps do not support direct import on the phone itself
- If you use Google Calendar, importing on the web first and then syncing is usually the safer approach

So the best first step is to try opening `kogi.ics` directly. If that does not work, use a web import flow or a third-party calendar app with `.ics` support.
