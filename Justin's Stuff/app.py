from flask import Flask, render_template, request, redirect, url_for
from todolist import ToDo

app = Flask(__name__)
toDo = ToDo()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        item = request.form.get("item")

        if action == "Add":
            toDo.addItem(item)
        elif action == "Remove":
            toDo.removeItem(item)
        
        return redirect(url_for("index"))

    return render_template("index.html", todo_list=toDo.lst)

if __name__ == "__main__":
    app.run(debug=True)
