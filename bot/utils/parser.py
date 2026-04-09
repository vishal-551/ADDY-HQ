from __future__ import annotations


def parse_csv_ints(value: str) -> list[int]:
    output: list[int] = []
    for raw in value.split(","):
        part = raw.strip()
        if part.isdigit():
            output.append(int(part))
    return output
