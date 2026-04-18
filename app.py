#Sau khi hoàn thành train sẽ chỉnh sửa lại sau, cái này demo thử
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["image"]
        result = "Uploaded successfully!"  

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)