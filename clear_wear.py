

from bs4 import BeautifulSoup

# Путь к файлу HTML
html_file = "/Users/anahart/GitHub/index/anahartlab.github.io/wear.html"

# Читаем HTML
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 1️⃣ Удаляем проданные товары
sections = soup.find_all("section", class_="u-clearfix u-section-16")
for section in sections:
    availability = section.find("p", class_="u-text-availability")
    if availability:
        text = availability.get_text(strip=True)
        if "0" in text or "нет" in text.lower():
            section.decompose()

# 2️⃣ Создаем навигацию по оставшимся товарам
nav = soup.new_tag("nav", **{"class": "u-nav u-unstyled"})
ul = soup.new_tag("ul", **{"class": "u-unstyled"})
for section in soup.find_all("section", class_="u-clearfix u-section-16"):
    sec_id = section.get("id")
    # ищем заголовок внутри секции
    h3 = section.find(["h3", "h2", "h1"])
    if not h3:
        continue
    title = h3.get_text(strip=True)
    li = soup.new_tag("li")
    a = soup.new_tag("a", href=f"#{sec_id}")
    a.string = title
    li.append(a)
    ul.append(li)
nav.append(ul)

# Вставляем навигацию после header
header = soup.find("header")
if header:
    header.insert_after(nav)

# Сохраняем HTML
with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("✅ Проданные товары удалены, навигация создана.")