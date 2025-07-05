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

        # === Новый блок: формируем HTML в стиле второго скрипта ===
        carousel_indicators = ""
        carousel_items = ""

        for i, img_name in enumerate(images):
            active_class = "u-active" if i == 0 else ""
            indicator_li = f'<li data-u-target="#carousel-00ac" data-u-slide-to="{i}" class="{active_class} u-grey-70 u-shape-circle" style="width: 10px; height: 10px;"></li>'
            carousel_indicators += indicator_li + "\n                          "

            item_div = f'''
    <div class="{active_class} u-carousel-item u-gallery-item u-carousel-item-{i+1}">
      <div class="u-back-slide" data-image-width="960" data-image-height="1280">
        <img class="u-back-image u-expanded" src="images/{name}/{img_name}">
      </div>
      <div class="u-align-center u-over-slide u-shading u-valign-bottom u-over-slide-{i+1}">
        <h3 class="u-gallery-heading">Пример заголовка</h3>
        <p class="u-gallery-text">Пример текста</p>
      </div>
    </div>'''
            carousel_items += item_div + "\n                          "

        block = f"""
<section class="u-clearfix u-section-16" id="{name}">
  <div class="u-clearfix u-sheet u-valign-top-lg u-valign-top-xl u-sheet-1">
    <div class="data-layout-selected u-clearfix u-expanded-width u-layout-wrap u-layout-wrap-1">
      <div class="u-layout">
        <div class="u-layout-row">
          <div class="u-size-30">
            <div class="u-layout-col">
              <div class="u-container-style u-layout-cell u-size-60 u-layout-cell-1">
                <div class="u-container-layout u-valign-middle-lg u-valign-middle-sm u-valign-middle-xs u-container-layout-1">
                  <div class="u-carousel u-expanded-width u-gallery u-gallery-slider u-layout-carousel u-lightbox u-no-transition u-show-text-none u-gallery-1" data-interval="5000" data-u-ride="carousel" id="carousel-00ac">
                    <ol class="u-absolute-hcenter u-carousel-indicators u-carousel-indicators-1">
                      {carousel_indicators}
                    </ol>
                    <div class="u-carousel-inner u-gallery-inner" role="listbox">
                      {carousel_items}
                    </div>
                    <a class="u-absolute-vcenter u-carousel-control u-carousel-control-prev u-grey-70 u-icon-circle u-opacity u-opacity-70 u-spacing-10 u-text-white u-carousel-control-1" href="#carousel-00ac" role="button" data-u-slide="prev"><span aria-hidden="true">
                        <svg viewBox="0 0 451.847 451.847"><path d="M97.141,225.92c0-8.095,3.091-16.192,9.259-22.366L300.689,9.27c12.359-12.359,32.397-12.359,44.751,0
c12.354,12.354,12.354,32.388,0,44.748L173.525,225.92l171.903,171.909c12.354,12.354,12.354,32.391,0,44.744
c-12.354,12.365-32.386,12.365-44.745,0l-194.29-194.281C100.226,242.115,97.141,234.018,97.141,225.92z"></path></svg></span><span class="sr-only">
                        Previous</span></a>
                    <a class="u-absolute-vcenter u-carousel-control u-carousel-control-next u-grey-70 u-icon-circle u-opacity u-opacity-70 u-spacing-10 u-text-white u-carousel-control-2" href="#carousel-00ac" role="button" data-u-slide="next"><span aria-hidden="true">
                        <svg viewBox="0 0 451.846 451.847"><path d="M345.441,248.292L151.154,442.573c-12.359,12.365-32.397,12.365-44.75,0c-12.354-12.354-12.354-32.391,0-44.744
L278.318,225.92L106.409,54.017c-12.354-12.359-12.354-32.394,0-44.748c12.354-12.359,32.391-12.359,44.75,0l194.287,194.284
c6.177,6.18,9.262,14.271,9.262,22.366C354.708,234.018,351.617,242.115,345.441,248.292z"></path></svg></span><span class="sr-only">
                        Next</span></a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="u-size-30">
            <div class="u-layout-col">
              <div class="u-container-style u-layout-cell u-size-60 u-layout-cell-2">
                <div class="u-container-layout u-container-layout-2">
                  <h3 class="u-align-center u-text u-text-1">{title}</h3>
                  <p class="u-align-left u-text u-text-2">{description}</p>
                  <h3 class="u-align-center-md u-align-center-sm u-align-center-xs u-align-left-lg u-align-left-xl u-text u-text-default-lg u-text-default-xl u-text-3">Цена по запросу</h3>
                  <a href="https://donate.stream/anahart" class="u-btn u-btn-round u-button-style u-custom-font u-heading-font u-hover-palette-1-light-1 u-palette-1-base u-radius u-btn-1" title="Оплатить">Оплатить</a>
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