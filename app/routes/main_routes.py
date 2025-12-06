from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from ..extensions import db
from ..model.user_model import User, Score

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    games_list = [
        {'id': 'pong', 'title': 'Classic Pong', 'thumb': url_for('static', filename='images/pong_thumbnail.png')},
        {'id': 'snake', 'title': 'Pixel Snake', 'thumb': url_for('static', filename='images/snake_thumbnail.png')},
    ]
    return render_template('index.html', games=games_list)

@main_bp.route('/game/<game_id>')
@login_required
def play_game(game_id):
    # This points to static/games/<game_id>/index.html
    # Ensure you moved your games to the root 'static' folder
    game_url = url_for('static', filename=f'games/{game_id}/index.html')
    return render_template('game_player.html', game_url=game_url, title=game_id)

@main_bp.route('/leaderboard')
def leaderboard():
    # Improved Query: Join User and Score, Order by Score Descending
    top_scores = db.session.query(
        Score.score,
        Score.game_id,
        User.username
    ).join(User).order_by(Score.score.desc()).limit(20).all()
    
    return render_template('leaderboard.html', scores=top_scores)

# --- API FOR GAMES ---
@main_bp.route('/api/submit-score', methods=['POST'])
@login_required
@cross_origin(supports_credentials=True) 
def submit_score():
    if not request.json:
        return jsonify({'success': False, 'message': 'Invalid JSON'}), 400
    
    data = request.json
    score_value = data.get('score')
    game_id = data.get('game_id')
    
    if score_value is None or game_id is None:
        return jsonify({'success': False, 'message': 'Missing data'}), 400
        
    try:
        new_score = Score(
            score=int(score_value),
            game_id=str(game_id),
            user_id=current_user.id
        )
        db.session.add(new_score)
        db.session.commit()
        
        print(f"SCORE SAVED: {current_user.username} - {score_value} pts")
        return jsonify({'success': True}), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"ERROR SAVING SCORE: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500