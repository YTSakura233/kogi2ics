import argparse
import datetime
import json
from pathlib import Path

import requests

from generate_ics import write_ics

URL = "https://home.kcg.ac.jp/portal/api/KogiCalendar/?uKbn=1&start={D1}&end={D2}"

OUTPUT_DIR = Path(__file__).parent

PERIOD_SCHEDULE = {
    1: ("09:30", "11:00"),
    2: ("11:10", "12:40"),
    3: ("13:30", "15:00"),
    4: ("15:10", "16:40"),
    5: ("16:50", "18:20"),
    6: ("18:30", "20:00"),
    7: ("20:10", "21:40"),
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="获取京都情报大学院大学的课程表并转换为icf格式"
    )
    parser.add_argument(
        "-c",
        "--cookie",
        type=str,
        required=True,
        help="your cookie",
    )
    parser.add_argument(
        "-x",
        "--x",
        type=str,
        required=True,
        help="your x-cpauthorize",
    )
    parser.add_argument(
        "-t",
        "--term",
        type=int,
        required=True,
        choices=[1, 2],
        help="School term, 1 for Spring, 2 for Autumn",
    )
    return parser.parse_args()

def getkogi(D1:str, D2:str, x:str, cookie:str) -> None:
    headers = {
        "x-cpauthorize": x,
        "cookie": cookie,
    }

    session = requests.Session()
    session.headers.update(headers)

    url = URL.format(D1=D1, D2=D2)
    try:
        response = session.get(url, timeout=30)
        response.encoding = response.apparent_encoding or "utf-8"

        filename = "kogi.json"
        filepath = OUTPUT_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"失败{e}")

def main():
    args = parse_args()

    year = datetime.date.today().year
    D1 = f"{year}-04-01" if args.term == 1 else f"{year}-10-01"
    D2 = f"{year}-08-30" if args.term == 1 else f"{year+1}-03-31"

    getkogi(D1, D2, args.x, args.cookie)

    kogipath = OUTPUT_DIR / "kogi.json"
    output_path = OUTPUT_DIR / "kogi.ics"

    events = json.loads(kogipath.read_text(encoding="utf-8"))
    if not isinstance(events, list):
        raise ValueError("课程 JSON 顶层必须是数组")

    write_ics(events, PERIOD_SCHEDULE, output_path)
    print(f"已生成 {output_path}，共 {len(events)} 条课程事件。")

if __name__ == "__main__":
    main()