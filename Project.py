from flask import Flask, render_template, request
from movies import get_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET'])
def recommend():
    movie_name = request.args.get('movie')
    preference = request.args.get('preference')

    if not movie_name:
        return render_template('error.html', error="Назва фільму є обов'язковою!")
    if preference not in ['movie', 'year', 'director']:
        return render_template('error.html', error="Некоректний вибір уподобань.")

    recommendations = get_recommendations(movie_name, preference)

    if "error" in recommendations:
        return render_template('error.html', error=recommendations["error"])

    icons = [
        '2025_18397876.png',
        'balloons_6266664.png',
        'fireworks_14301720.png',
        'heart_7450839.png',
        'ornament_9047448.png',
        'snowman_3737405.png',
        'snowman_7284636.png',
        'tent_8612099.png'
    ]
    for i, rec in enumerate(recommendations):
        rec['icon'] = icons[i % len(icons)]  # Циклічне додавання іконок

    return render_template(
        'result.html',
        selected_movie_name=movie_name,
        valueOption=preference,
        listmain=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)
