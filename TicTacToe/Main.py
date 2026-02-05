from flask import Flask, jsonify, render_template
from database.db_utils import get_tictactoe_stats, get_checkers_stats, get_connectfour_stats
import webbrowser

app = Flask(__name__)

from games.TicTacToe import ttt_bp
from games.Checkers import checkers_bp
from games.ConnectFour import connectfour_bp

app.register_blueprint(ttt_bp)
app.register_blueprint(checkers_bp)
app.register_blueprint(connectfour_bp)

@app.route('/')
@app.route('/main')
def main():
    return render_template('Main.html')

@app.route('/stats')
def stats():
    try:
        return jsonify({
            "tictactoe": get_tictactoe_stats(),
            "checkers": get_checkers_stats(),
            "connectfour": get_connectfour_stats()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    webbrowser.open_new("http://localhost:5000/main")
    app.run(debug=True, use_reloader=False)