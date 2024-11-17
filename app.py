from flask import Flask,render_template,request,jsonify,redirect,url_for
from database import Database

app = Flask(__name__)
db = Database()

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        code = request.form["code"]
        url = request.form["url"]
        if not db.url_exists(code):
            db.insert_url(code, url)
            result = {
                'code': code,
                "url": url,
                "shorten_link": f"{code}"
            }
        else:
            result = {"error": "This code is already taken"}
        return jsonify(result)

@app.route("/<shorten>", methods=["GET"])
def code_redirect(shorten):
    url_data = db.get_url(shorten)
    if not url_data:
        return redirect(url_for('index')) 
    original_url = url_data[0]
    return redirect(original_url)

@app.route("/urls", methods=["GET"])
def return_urls():
    conn = db.create_connection() 
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT short_code, original_url FROM urls")
        urls = cursor.fetchall()
        conn.close() 
        return jsonify(urls), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)