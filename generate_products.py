import os
import csv

# === Параметры ===
csv_path = "products.csv"
html_path = "PSYWEAR.html"
images_dir = "images"
valid_exts = {".jpg", ".jpeg", ".png"}

# === Проверка HTML-файла ===
if not os.path.exists(html_path):
    print(f"❌ HTML-файл '{html_path}' не найден.")
    exit()

# === Читаем текущий HTML ===
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

insert_index = html_content.lower().find("<footer")
if insert_index == -1:
    print("❌ Не найден <footer> в PSYWEAR.html")
    exit()

# === Читаем CSV ===
with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Name"].strip()
        title = row["Title"].strip()
        description = row["Description"].strip()
        folder_path = os.path.join(images_dir, name)

        if not os.path.isdir(folder_path):
            print(f"⚠️  Пропущен '{name}' — папка '{folder_path}' не найдена.")
            continue

        images = [f for f in sorted(os.listdir(folder_path)) if os.path.splitext(f)[1].lower() in valid_exts]
        if not images:
            print(f"⚠️  Пропущен '{name}' — нет изображений.")
            continue

        # === Генерируем блок галереи ===
        indicators = ""
        slides = ""
        for i, img in enumerate(images):
            active = "u-active" if i == 0 else ""
            indicators += f'<li data-u-target="#carousel-{name}" data-u-slide-to="{i}" class="{active} u-grey-70 u-shape-circle" style="width: 10px; height: 10px;"></li>\n'

            slides += f'''
    <div class="{active} u-carousel-item u-gallery-item u-carousel-item-{i+1}">
      <div class="u-back-slide" data-image-width="960" data-image-height="1280">
        <img class="u-back-image u-expanded" src="images/{name}/{img}">
      </div>
      <div class="u-align-center u-over-slide u-shading u-valign-bottom u-over-slide-{i+1}">
        <h3 class="u-gallery-heading">{title}</h3>
        <p class="u-gallery-text">{description}</p>
      </div>
    </div>'''

        block = f"""
<section class="u-clearfix u-section-16" id="{name}">
  <div class="u-clearfix u-sheet">
    <div class="u-layout-wrap">
      <div class="u-layout">
        <div class="u-layout-row">
          <div class="u-size-30">
            <div class="u-layout-col">
              <div class="u-container-style u-layout-cell u-size-60">
                <div class="u-container-layout">
                  <div class="u-carousel u-gallery u-gallery-slider u-layout-carousel u-lightbox u-show-text-none u-gallery-1" data-interval="5000" data-u-ride="carousel" id="carousel-{name}">
                    <ol class="u-carousel-indicators">{indicators}</ol>
                    <div class="u-carousel-inner u-gallery-inner">{slides}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="u-size-30">
            <div class="u-layout-col">
              <div class="u-container-style u-layout-cell u-size-60">
                <div class="u-container-layout">
                  <h3 class="u-align-center">{title}</h3>
                  <p class="u-align-left">{description}</p>
                  <a href="https://donate.stream/anahart" class="u-btn u-btn-round u-button-style u-custom-font u-heading-font u-hover-palette-1-light-1 u-palette-1-base u-radius">Оплатить</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
        # === Вставка перед <footer> ===
        html_content = html_content[:insert_index] + block + "\n" + html_content[insert_index:]
        insert_index += len(block)

# === Сохраняем результат ===
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Все товары из CSV добавлены в PSYWEAR.html")