from flask import Flask, render_template, request
import pandas as pd
import random
import os

app = Flask(__name__)

EXCEL_FILE = "claimed_discounts.xlsx"

# Initialize Excel if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Phone", "Discount"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    discount = None

    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()

        # Load existing claims
        df = pd.read_excel(EXCEL_FILE)

        if phone in df["Phone"].astype(str).values:
            message = f"❌ Phone number {phone} has already claimed a discount!"
        else:
            discount = random.randint(5, 15)
            new_row = {"Name": name, "Phone": phone, "Discount": discount}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            message = f"✅ Congrats {name}! You got ₹{discount} discount."

    return render_template("index.html", message=message, discount=discount)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
