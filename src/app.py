from flask import Flask, render_template, request
from weather import get_coordinates, get_current_weather, WeatherError


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        weather = None
        error = None
        city_input = ""

        if request.method == "POST":
            city_input = request.form.get("city", "").strip()
            try:
                lat, lon, city_name = get_coordinates(city_input)
                data = get_current_weather(lat, lon)
                weather = {"city": city_name, **data}
            except WeatherError as e:
                error = str(e)

        return render_template("index.html", weather=weather, error=error, city=city_input)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
