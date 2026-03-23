from flask import Flask, render_template, request, send_from_directory
from search import multimodal_search
from explain import explain
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "images/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔥 FIX: serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        query = request.form.get("query")
        file = request.files.get("image")

        image_path = None

        if file and file.filename != "":
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(image_path)

        search_results = multimodal_search(query, image_path)

        for r in search_results:
            results.append({
                "item": r["item"],
                "image": r["image"],
                "score": r["score"],
                "explanation": explain(query, r["item"], r["score"])
            })

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)