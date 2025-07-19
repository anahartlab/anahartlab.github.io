import os
from datetime import datetime

# === Параметры ===
BLOG_PATH = "blog.html"
INSERT_MARKER = "<!-- blog-insert-point -->"

# === Получение данных ===
date_str = datetime.today().strftime("%Y-%m-%d")

title = input("Заголовок блока: ").strip()
id_block = input("Короткое имя для id (например: festival-marocco): ").strip()

print("Вставьте HTML-контент (завершите ввод двумя пустыми строками):")
lines = []
while True:
    line = input()
    if line.strip() == "" and (len(lines) > 0 and lines[-1].strip() == ""):
        break
    lines.append(line)
content_html = "\n".join(lines)

# === Формирование секции ===
section = f'''
    <section class="u-clearfix u-section" id="{id_block}">
      <h2>{title}</h2>
      <p><small>Опубликовано: {date_str}</small></p>
      <div>
        {content_html}
      </div>
    </section>
'''

# === Чтение и вставка ===
if not os.path.exists(BLOG_PATH):
    print(f"❌ Файл {BLOG_PATH} не найден.")
    exit(1)

with open(BLOG_PATH, "r", encoding="utf-8") as f:
    html = f.read()

if INSERT_MARKER not in html:
    print("❌ Маркер вставки не найден в файле блога.")
    exit(1)

new_html = html.replace(INSERT_MARKER, section + "\n" + INSERT_MARKER)

with open(BLOG_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Секция '{title}' успешно добавлена в blog.html")