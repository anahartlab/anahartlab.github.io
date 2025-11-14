from flask import Flask, request, render_template_string, redirect, url_for
import os
from datetime import datetime
import re

app = Flask(__name__)

BLOG_PATH = "blog.html"
INSERT_MARKER = "<!-- blog-insert-point -->"
NAV_MARKER = "<!-- blog-nav-insert-point -->"

# HTML шаблон формы
FORM_HTML = """
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Добавить запись в блог</title>
<style>
body { font-family: Arial, sans-serif; margin: 40px; }
input, textarea { width: 100%; margin-bottom: 15px; padding: 8px; font-size: 14px; }
textarea { height: 200px; font-family: monospace; }
button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
label { font-weight: bold; }
.preview-section { border: 1px solid #ccc; padding: 15px; margin-top: 20px; background: #f9f9f9; }
</style>
</head>
<body>
<h2>Добавить запись в блог</h2>
<form method="POST" enctype="multipart/form-data">
  <label>Заголовок:</label>
  <input type="text" name="title" required value="{{ title|default('') }}">
  
  <label>Короткий id для ссылки:</label>
  <input type="text" name="id_block" required value="{{ id_block|default('') }}">
  
  <label>HTML-контент (можно писать HTML-теги):</label>
  <textarea name="content" required>{{ content|default('') }}</textarea>
  
  <label>Загрузить изображения (можно несколько):</label>
  <input type="file" name="images" accept="image/*" multiple>
  
  <button type="submit" name="action" value="preview">Предпросмотр</button>
  <button type="submit" name="action" value="add">Добавить запись</button>
</form>

{% if preview_html %}
<h3>Предпросмотр записи:</h3>
<div class="preview-section">
  {{ preview_html|safe }}
</div>
{% endif %}
</body>
</html>
"""

UPLOAD_FOLDER = "images/blog"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def convert_links(text):
    # Регулярное выражение для URL с протоколом и без (например, t.me/...)
    pattern = re.compile(r'(?P<url>(https?://[^\s"<>]+|t\.me/[^\s"<>]+))')

    def repl(match):
        url = match.group("url")
        if url.startswith("t.me/"):
            href = "https://" + url
        else:
            href = url
        return f'<a href="{href}" target="_blank">{url}</a>'

    return pattern.sub(repl, text)


@app.route("/", methods=["GET", "POST"])
def index():
    preview_html = None
    title = ""
    id_block = ""
    content_html = ""

    if request.method == "POST":
        title = request.form["title"].strip()
        id_block = request.form["id_block"].strip()
        content_html = request.form["content"].strip()
        action = request.form.get("action")

        # --- Формируем дату и время ---
        now = datetime.now()
        months = [
            "января",
            "февраля",
            "марта",
            "апреля",
            "мая",
            "июня",
            "июля",
            "августа",
            "сентября",
            "октября",
            "ноября",
            "декабря",
        ]
        date_str = now.strftime("%Y-%m-%d %H:%M")

        uploaded_files = request.files.getlist("images")
        saved_img_tags = []
        for file in uploaded_files:
            if file and file.filename:
                safe_name = file.filename.replace(" ", "_")
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
                file.save(save_path)
                saved_img_tags.append(f'<img src="images/blog/{safe_name}" alt="">')

        # --- Обработка изображений для карусели ---
        # Предполагается, что изображения в контенте имеют теги <img src="...">.
        # Извлекаем все src изображений
        content_html_converted = convert_links(content_html) + "<br>" + "".join(saved_img_tags)

        img_srcs = re.findall(r'<img\s+[^>]*src="([^"]+)"', content_html_converted)

        if len(img_srcs) == 1:
            # Одна картинка - вывод без карусели
            carousel_html = f'<img src="{img_srcs[0]}" alt="Image" style="max-width:100%;">'
        elif len(img_srcs) > 1:
            # Несколько картинок - карусель с индикаторами и стрелками
            indicators = ''.join(
                '<li data-target="#carouselExampleIndicators" data-slide-to="{}"{}></li>'.format(
                    i, ' class="active"' if i == 0 else ''
                ) for i in range(len(img_srcs))
            )
            items = ''.join(
                '<div class="carousel-item{}"><img class="d-block w-100" src="{}" alt="Slide {}"></div>'.format(
                    ' active' if i == 0 else '', src, i + 1
                ) for i, src in enumerate(img_srcs)
            )
            carousel_html = f'''
<div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
  <ol class="carousel-indicators">
    {indicators}
  </ol>
  <div class="carousel-inner">
    {items}
  </div>
  <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>
'''
        else:
            carousel_html = ''

        # --- Формируем новую секцию ---
        section_html = f"""
<section class="u-clearfix u-section-1" id="{id_block}">
  <div class="u-clearfix u-sheet u-valign-middle-lg u-sheet-1">
    <h5 class="u-align-left u-text u-text-1">{date_str}</h5>
    <h3 class="u-align-center u-text u-text-2">{title}</h3>
    <p class="u-align-center u-text u-text-3">
      {content_html_converted}
    </p>
    {carousel_html}
  </div>
</section>
"""

        if action == "preview":
            preview_html = section_html
        elif action == "add":
            if not os.path.exists(BLOG_PATH):
                return f"❌ Файл {BLOG_PATH} не найден.", 500

            with open(BLOG_PATH, "r", encoding="utf-8") as f:
                html = f.read()

            # --- Добавляем ссылку в навигацию ---
            if NAV_MARKER in html:
                link_html = f'<a href="#{id_block}">{title}</a> | '
                html = html.replace(NAV_MARKER, NAV_MARKER + "\n      " + link_html)

            if INSERT_MARKER not in html:
                return "❌ Маркер вставки записи не найден в файле блога.", 500

            html = html.replace(INSERT_MARKER, INSERT_MARKER + "\n" + section_html)

            with open(BLOG_PATH, "w", encoding="utf-8") as f:
                f.write(html)

            return (
                f"✅ Запись '{title}' успешно добавлена! <a href='/'>Добавить ещё</a>"
            )

    return render_template_string(
        FORM_HTML,
        preview_html=preview_html,
        title=title,
        id_block=id_block,
        content=content_html,
    )


if __name__ == "__main__":
    print("Сервер запущен на http://127.0.0.1:5000/")
    app.run(debug=True)
