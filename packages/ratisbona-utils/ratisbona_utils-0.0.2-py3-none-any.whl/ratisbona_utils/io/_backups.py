from pathlib import Path

UTF8 = {"encoding": "utf-8"}


def maybe_backup_file(filepath: Path) -> bool:
    if not filepath.exists():
        return False
    print(f"Backuping {filepath}")
    with filepath.with_suffix(".bak").open("w", **UTF8) as backup:
        backup.write(filepath.read_text(**UTF8))
    return True