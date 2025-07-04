import os

# === 1. Ввод информации о товаре ===
title = input("Название товара: ").strip()
description = input("Описание: ").strip()
image_name = input("Имя картинки (в папке images/): ").strip()
link = input("Ссылка на заказ: ").strip()

# === 2. HTML-шаблон блока товара ===
product_block = f"""
<section class="u-align-center u-clearfix u-section">
  <div class="u-container-layout">
    <img src="images/{image_name}" alt="{title}" class="u-image" />
    <h2 class="u-text">{title}</h2>
    <p class="u-text">{description}</p>
    <a href="{link}" class="u-btn">Заказать</a>
  </div>
</section>
"""

# === 3. Файл, в который вставляем блок ===
html_path = "PSYWEAR.html"

if not os.path.exists(html_path):
    print("❌ Файл PSYWEAR.html не найден.")
    exit()

# === 4. Вставка перед </body> ===
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

insert_index = content.lower().rfind("</body>")
if insert_index == -1:
    print("❌ Не удалось найти </body> для вставки.")
    exit()

new_content = content[:insert_index] + product_block + "\n" + content[insert_index:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ Новый товар добавлен в PSYWEAR.html")
