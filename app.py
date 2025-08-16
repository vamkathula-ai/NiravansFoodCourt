from flask import Flask, render_template, request
import pandas as pd
import os
import random
from datetime import date

app = Flask(__name__)

EXCEL_FILE = "coupons.xlsx"

# Initialize Excel file with proper columns if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Phone", "Discount", "Date"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    discount = None
    message = None
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()

        df = pd.read_excel(EXCEL_FILE)

        today = date.today().strftime("%Y-%m-%d")

        # Check if this phone already claimed today
        if ((df["Phone"].astype(str) == phone) & (df["Date"].astype(str) == today)).any():
            message = "❌ This number has already claimed a discount today."
        else:
            discount = random.randint(5, 15)
            new_row = {
                "Name": name,
                "Phone": phone,
                "Discount": discount,
                "Date": today
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            message = f"✅ Congrats {name}, you got ₹{discount} off!"

    return render_template("index.html", message=message, discount=discount)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render dynamic port
    app.run(host="0.0.0.0", port=port)
