import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# 1) Load and prepare data at startup
df = pd.read_csv("data/scores.csv", parse_dates=["date"])
# keep only month-day
df["month_day"] = df["date"].dt.strftime("%m-%d")

# compute composite score: average of (100-crowd) + pricePoint + weather_score
df["composite"] = ( (100 - df["crowd_point"]) + df["pricePoint"] + df["weather_score"] ) / 3

# prepare list of cities
cities = sorted(df["City"].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        year = request.form["year"]
        # filter by city
        city_df = df[df["City"] == city]
        # find the best row
        best = city_df.loc[city_df["composite"].idxmax()]
        month_day = best["month_day"]
        # build a YYYY-MM-DD string
        recommended = f"{int(year):04d}-{month_day}"
        # pass all breakdowns to template
        return render_template("results.html",
                               city=city,
                               year=year,
                               recommended=recommended,
                               crowd=best["crowd_point"],
                               price=best["pricePoint"],
                               weather=best["weather_score"],
                               composite=best["composite"])
    return render_template("index.html", cities=cities)

if __name__ == "__main__":
    app.run(debug=True)
