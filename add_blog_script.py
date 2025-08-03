import os
from datetime import datetime

# === Параметры ===
BLOG_PATH = "blog.html"
INSERT_MARKER = "<!-- blog-insert-point -->"
NAV_MARKER = "<!-- blog-nav-insert-point -->"

# === Получение данных ===
date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

title = input("Заголовок блока: ").strip()
id_block = input("Короткое имя для id: ").strip()

print("Вставьте HTML-контент (завершите ввод двойным Enter):")
# Для добавления изображений используйте обычный HTML-тег, например:
# <img src=\"images/my-image.jpg\" alt=\"описание\" style=\"max-width:100%;\">
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

if NAV_MARKER in html:
    link_html = f'<a href="#{id_block}">{title}</a> | '
    html = html.replace(NAV_MARKER, NAV_MARKER + "\n      " + link_html)

if INSERT_MARKER not in html:
    print("❌ Маркер вставки записи не найден в файле блога.")
    exit(1)

# Вставка новой секции блога сразу после INSERT_MARKER
html = html.replace(INSERT_MARKER, INSERT_MARKER + "\n" + section)

# Переместить только что вставленную секцию сразу после контейнера навигации
container_start = html.find('<section style="max-width: 900px; margin: 20px auto;" id="blog-nav">')
if container_start == -1:
    print("⚠️ Контейнер с навигацией не найден, секция останется на месте.")
else:
    container_end = html.find('</section>', container_start)
    if container_end == -1:
        print("⚠️ Закрывающий тег </section> контейнера не найден.")
    else:
        container_end += len('</section>')
        # Найти вставленную секцию по id
        section_start = html.find(f'<section class="u-clearfix u-section-1" id="{id_block}">')
        if section_start == -1:
            print("❌ Вставленная секция не найдена для перемещения.")
        else:
            section_end = html.find('</section>', section_start)
            if section_end == -1:
                print("❌ Закрывающий тег </section> для секции не найден.")
            else:
                section_end += len('</section>')
                section_html = html[section_start:section_end]
                # Удалить секцию с текущего места
                html = html[:section_start] + html[section_end:]
                # Вставить секцию после контейнера
                html = html[:container_end] + '\n' + section_html + '\n' + html[container_end:]
                # Переместить маркер <!-- blog-insert-point --> после контейнера
                marker_pos = html.find(INSERT_MARKER)
                if marker_pos != -1:
                    html = html[:marker_pos] + html[marker_pos + len(INSERT_MARKER):]  # Удаляем маркер
                    html = html[:container_end] + '\n' + INSERT_MARKER + '\n' + html[container_end:]

with open(BLOG_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Секция '{title}' и ссылка в меню успешно добавлены в blog.html")