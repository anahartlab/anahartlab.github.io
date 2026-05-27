#!/usr/bin/env python3
# replace_footer.py

import os, re, shutil, datetime

HTML_DIR = "."
FOOTER_FILE = "footer.txt"
BACKUP_SUFFIX = ".bak"


def read_footer():
    if not os.path.exists(FOOTER_FILE):
        raise SystemExit(f"❌ Не найден {FOOTER_FILE}")

    txt = open(FOOTER_FILE, "r", encoding="utf-8").read()

    if "<footer" not in txt.lower() or "</footer>" not in txt.lower():
        raise SystemExit("❌ footer.txt должен содержать тег <footer>...</footer>")

    return txt


def backup_path(path):
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{path}{BACKUP_SUFFIX}.{ts}"


def replace_footer_in_file(path, new_footer):
    txt = open(path, "r", encoding="utf-8").read()

    pattern = re.compile(r"(?is)(<footer\b.*?>).*?(</footer>)")

    if not pattern.search(txt):
        return False

    shutil.copy2(path, backup_path(path))

    new_txt = pattern.sub(new_footer, txt, count=1)

    open(path, "w", encoding="utf-8").write(new_txt)
    return True


def main():
    new_footer = read_footer()

    files = [
        f
        for f in os.listdir(HTML_DIR)
        if f.lower().endswith(".html") and os.path.isfile(os.path.join(HTML_DIR, f))
    ]

    if not files:
        print("⚠️ HTML файлов не найдено в папке.")
        return

    replaced = 0
    skipped = []

    for fn in files:
        path = os.path.join(HTML_DIR, fn)

        ok = replace_footer_in_file(path, new_footer)

        if ok:
            print(f"✅ Обновлён: {fn}")
            replaced += 1
        else:
            print(f"— Пропущен (footer не найден): {fn}")
            skipped.append(fn)

    print(f"\nГотово. Обновлено: {replaced}. Пропущено: {len(skipped)}.")


if __name__ == "__main__":
    main()
