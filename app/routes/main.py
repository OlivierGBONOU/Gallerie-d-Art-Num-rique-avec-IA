# app/routes/main.py
from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from sqlalchemy import func
from ..models import Artwork, Emotion, Vote, Like
from ..forms import EmptyForm
from ..utils.wordcloud_generator import generate_wordcloud
from .. import db
from flask_login import current_user
bp = Blueprint('main', __name__)

@bp.route('/', defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    per_page = 8  # Nombre d'œuvres par page
    artworks = Artwork.query.paginate(page=page, per_page=per_page, error_out=False)
    emotions = Emotion.query.all()
    return render_template('index.html', artworks=artworks, emotions=emotions)

@bp.route('/artwork/<int:artwork_id>')
def artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    emotions = Emotion.query.all()
    vote_counts = db.session.query(Vote.emotion_id, func.count(Vote.id))\
        .filter_by(artwork_id=artwork_id)\
        .group_by(Vote.emotion_id).all()
    vote_dict = {emotion.id: 0 for emotion in emotions}
    for emotion_id, count in vote_counts:
        vote_dict[emotion_id] = count
    wordcloud_img = generate_wordcloud(artwork.comments) if artwork.comments else None
    form = EmptyForm()
    # Vérifier si l'utilisateur a aimé l'œuvre
    has_liked = current_user.is_authenticated and any(like.user_id == current_user.id for like in artwork.likes)
    return render_template('artwork.html', artwork=artwork, emotions=emotions, vote_counts=list(vote_dict.values()), wordcloud_img=wordcloud_img, form=form, has_liked=has_liked)

@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    emotion = request.args.get('emotion', '')
    sort = request.args.get('sort', 'date_desc')  # Par défaut : tri par date décroissante
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = Artwork.query
    if keyword:
        query = query.filter(Artwork.title.ilike(f'%{keyword}%') | Artwork.description.ilike(f'%{keyword}%'))
    if emotion:
        query = query.filter(Artwork.emotion_target == emotion)
    if sort == 'date_asc':
        query = query.order_by(Artwork.created_at.asc())
    elif sort == 'date_desc':
        query = query.order_by(Artwork.created_at.desc())
    elif sort == 'likes':
        query = query.outerjoin(Like).group_by(Artwork.id).order_by(db.func.count(Like.id).desc())
    artworks = query.paginate(page=page, per_page=per_page, error_out=False)
    emotions = Emotion.query.all()
    return render_template('index.html', artworks=artworks, emotions=emotions, keyword=keyword, selected_emotion=emotion, sort=sort)