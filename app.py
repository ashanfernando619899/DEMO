from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    weight = float(request.form["weight"])
    height = float(request.form["height"])

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal Weight"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obese"

    return render_template(
        "result.html",
        bmi=round(bmi, 2),
        category=category
    )


if __name__ == "__main__":
    app.run(debug=True)