import argparse
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path


CAMPUS_PREFIX_MAP = {
    "M": "KCGI百万遍キャンパス南校舎",
    "H": "KCGI百万遍キャンパス本部棟",
}

PERIOD_SCHEDULE = {
    1: ("09:30", "11:00"),
    2: ("11:10", "12:40"),
    3: ("13:30", "15:00"),
    4: ("15:10", "16:40"),
    5: ("16:50", "18:20"),
    6: ("18:30", "20:00"),
    7: ("20:10", "21:40"),
}

def extract_tooltip_fields(tooltip_html: str) -> dict[str, str]:
    items = re.findall(r"<li>(.*?)</li>", tooltip_html, flags=re.IGNORECASE | re.DOTALL)
    fields: dict[str, str] = {}

    for item in items:
        text = html.unescape(re.sub(r"<.*?>", "", item)).strip()
        if "：" not in text:
            continue
        key, value = text.split("：", 1)
        fields[key.strip()] = value.strip()

    return fields


def extract_title(event: dict, fields: dict[str, str], period: int | None) -> str:
    if "タイトル" in fields:
        return fields["タイトル"].strip()

    raw_title = event.get("title", "").strip()
    if period is None:
        return raw_title

    return re.sub(rf"^{period}\s+", "", raw_title).strip()


def build_location(room: str) -> str:
    if not room:
        return ""

    campus = CAMPUS_PREFIX_MAP.get(room[0])
    if campus:
        return f"{campus} {room}"
    return room


def ics_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def compact_time(value: str) -> str:
    hour, minute = value.split(":")
    return f"{int(hour):02d}{minute}00"


def make_uid(date_str: str, title: str, period: int, room: str) -> str:
    digest = hashlib.sha1(f"{date_str}|{title}|{period}|{room}".encode("utf-8")).hexdigest()
    return f"{digest}@getkogi"


def build_event_lines(
    event: dict,
    schedule_map: dict[int, tuple[str, str]],
    dtstamp: str,
) -> list[str]:
    fields = extract_tooltip_fields(event.get("tooltip", ""))

    period_text = fields.get("時限", "").strip()
    room = fields.get("教室", "").strip()
    date_str = event["start"]

    if not period_text.isdigit():
        fallback_title = event.get("title", "").strip()
        raise ValueError(f"课程 {fallback_title} 的時限无法解析: {period_text}")

    period = int(period_text)
    title = extract_title(event, fields, period)

    if period not in schedule_map:
        raise ValueError(f"未找到第 {period} 节课的时间配置: {title}")

    start_time, end_time = schedule_map[period]
    start_dt = f"{date_str.replace('-', '')}T{compact_time(start_time)}"
    end_dt = f"{date_str.replace('-', '')}T{compact_time(end_time)}"

    location = build_location(room)
    description_lines = [
        f"课程名称: {title}",
        f"時限: 第{period}节课",
    ]
    if room:
        description_lines.append(f"教室: {room}")
    if location and location != room:
        description_lines.append(f"地点: {location}")

    return [
        "BEGIN:VEVENT",
        f"UID:{make_uid(date_str, title, period, room)}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;TZID=Asia/Tokyo:{start_dt}",
        f"DTEND;TZID=Asia/Tokyo:{end_dt}",
        f"SUMMARY:{ics_escape(title)}",
        f"LOCATION:{ics_escape(location)}",
        f"DESCRIPTION:{ics_escape(chr(10).join(description_lines))}",
        "END:VEVENT",
    ]


def fold_ics_line(line: str) -> list[str]:
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return [line]

    chunks: list[str] = []
    current = b""
    for char in line:
        char_bytes = char.encode("utf-8")
        limit = 74 if chunks else 75
        if len(current) + len(char_bytes) > limit:
            chunks.append(current.decode("utf-8"))
            current = char_bytes
        else:
            current += char_bytes
    if current:
        chunks.append(current.decode("utf-8"))

    return [chunks[0], *[f" {chunk}" for chunk in chunks[1:]]]


def write_ics(events: list[dict], schedule_map: dict[int, tuple[str, str]], output: Path) -> None:
    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//getkogi//Course Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-TIMEZONE:Asia/Tokyo",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Tokyo",
        "BEGIN:STANDARD",
        "DTSTART:19700101T000000",
        "TZOFFSETFROM:+0900",
        "TZOFFSETTO:+0900",
        "TZNAME:JST",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]

    for event in events:
        lines.extend(build_event_lines(event, schedule_map, dtstamp))

    lines.append("END:VCALENDAR")

    folded_lines: list[str] = []
    for line in lines:
        folded_lines.extend(fold_ics_line(line))

    output.write_text("\r\n".join(folded_lines) + "\r\n", encoding="utf-8", newline="")
