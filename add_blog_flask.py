# add_blog_flask.py
from flask import Flask, request, render_template_string, redirect, url_for
import os

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
</style>
</head>
<body>
<h2>Добавить запись в блог</h2>
<form method="POST">
  <label>Заголовок:</label>
  <input type="text" name="title" required>
  
  <label>Короткий id для ссылки:</label>
  <input type="text" name="id_block" required>
  
  <label>HTML-контент (можно писать HTML-теги):</label>
  <textarea name="content" required></textarea>
  
  <button type="submit">Добавить запись</button>
</form>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"].strip()
        id_block = request.form["id_block"].strip()
        content_html = request.form["content"].strip()

        if not os.path.exists(BLOG_PATH):
            return f"❌ Файл {BLOG_PATH} не найден.", 500

        with open(BLOG_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        # --- Добавляем ссылку в навигацию ---
        if NAV_MARKER in html:
            link_html = f'<a href="#{id_block}">{title}</a> | '
            html = html.replace(NAV_MARKER, NAV_MARKER + "\n      " + link_html)

        # --- Формируем новую секцию ---
        section_html = f"""
<section class="u-clearfix u-section-1" id="{id_block}">
  <h3>{title}</h3>
  {content_html}
</section>
"""

        if INSERT_MARKER not in html:
            return "❌ Маркер вставки записи не найден в файле блога.", 500

        html = html.replace(INSERT_MARKER, INSERT_MARKER + "\n" + section_html)

        with open(BLOG_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        return f"✅ Запись '{title}' успешно добавлена! <a href='/'>Добавить ещё</a>"

    return render_template_string(FORM_HTML)


if __name__ == "__main__":
    print("Сервер запущен на http://127.0.0.1:5000/")
    app.run(debug=True)
