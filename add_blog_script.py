import os
from datetime import datetime

# === Параметры ===
BLOG_PATH = "blog.html"
INSERT_MARKER = "<!-- blog-insert-point -->"

# === Получение данных ===
date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

title = input("Заголовок блока: ").strip()
id_block = input("Короткое имя для id: ").strip()

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
<section class="u-clearfix u-section-1" id="{id_block}">
  <!--
    SEO Title: {title}
    SEO Description: 
    SEO Keywords: 
  -->
  <div class="u-clearfix u-sheet u-valign-middle-lg u-sheet-1">
    <h5 class="u-align-left u-text u-text-1">{date_str}</h5>
    <h3 class="u-align-center u-text u-text-2">{title}</h3>
    <p class="u-align-center u-text u-text-3">
      {content_html}
    </p>
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

new_html = html.replace("<!-- blog-insert-point -->", "<!-- blog-insert-point -->\n" + section)

with open(BLOG_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Секция '{title}' успешно добавлена в blog.html")