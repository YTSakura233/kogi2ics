# kogi2ics

中文 | [日本語](README_JP.md) | [English](README_EN.md)

`kogi2ics` 是一个把 KCG.EDU(京都コンピュータ学院、京都情报大学院大学) 的课程数据导出为 `.ics` 日历文件的小工具。

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
