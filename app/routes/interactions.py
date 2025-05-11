# app/routes/interactions.py
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_mail import Message
from .. import db, mail
from ..models import Vote, Comment, Artwork, Emotion, Report, User

bp = Blueprint('interactions', __name__)

class EmptyForm(FlaskForm):
    pass

@bp.route('/vote/<int:artwork_id>', methods=['POST'])
@login_required
def vote(artwork_id):
    form = EmptyForm()
    if form.validate_on_submit():
        emotion_id = request.form.get('emotion_id')
        if not emotion_id:
            flash('Veuillez sélectionner une émotion.')
            return redirect(url_for('main.artwork', artwork_id=artwork_id))
        existing_vote = Vote.query.filter_by(user_id=current_user.id, artwork_id=artwork_id).first()
        if existing_vote:
            flash('Vous avez déjà voté pour cette œuvre.')
        else:
            vote = Vote(user_id=current_user.id, artwork_id=artwork_id, emotion_id=emotion_id)
            db.session.add(vote)
            db.session.commit()
            flash('Votre vote a été enregistré.')
    return redirect(url_for('main.artwork', artwork_id=artwork_id))

@bp.route('/comment/<int:artwork_id>', methods=['POST'])
@login_required
def comment(artwork_id):
    form = EmptyForm()
    if form.validate_on_submit():
        content = request.form.get('content')
        if not content:
            flash('Le commentaire ne peut pas être vide.')
            return redirect(url_for('main.artwork', artwork_id=artwork_id))
        comment = Comment(content=content, user_id=current_user.id, artwork_id=artwork_id)
        db.session.add(comment)
        db.session.commit()
        flash('Votre commentaire a été ajouté.')
    return redirect(url_for('main.artwork', artwork_id=artwork_id))

@bp.route('/report/<int:artwork_id>', methods=['POST'])
@login_required
def report_artwork(artwork_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reason = request.form.get('reason')
        if not reason:
            flash('Veuillez indiquer une raison pour le signalement.')
            return redirect(url_for('main.artwork', artwork_id=artwork_id))
        report = Report(reason=reason, artwork_id=artwork_id, user_id=current_user.id)
        db.session.add(report)
        db.session.commit()
        # Envoyer une notification par email aux admins
        admins = User.query.filter_by(is_admin=True).all()
        for admin in admins:
            msg = Message(
                subject='Nouveau signalement d’œuvre',
                recipients=[admin.email],
                body=f'Un signalement a été soumis pour l’œuvre ID {artwork_id}.\nRaison : {reason}\nVeuillez vérifier dans l’interface d’administration.'
            )
            mail.send(msg)
        flash('Signalement envoyé.')
    return redirect(url_for('main.artwork', artwork_id=artwork_id))

@bp.route('/report_comment/<int:comment_id>', methods=['POST'])
@login_required
def report_comment(comment_id):
    form = EmptyForm()
    if form.validate_on_submit():
        reason = request.form.get('reason')
        if not reason:
            flash('Veuillez indiquer une raison pour le signalement.')
            return redirect(url_for('main.artwork', artwork_id=Comment.query.get_or_404(comment_id).artwork_id))
        report = Report(reason=reason, comment_id=comment_id, user_id=current_user.id)
        db.session.add(report)
        db.session.commit()
        # Envoyer une notification par email aux admins
        admins = User.query.filter_by(is_admin=True).all()
        for admin in admins:
            msg = Message(
                subject='Nouveau signalement de commentaire',
                recipients=[admin.email],
                body=f'Un signalement a été soumis pour le commentaire ID {comment_id}.\nRaison : {reason}\nVeuillez vérifier dans l’interface d’administration.'
            )
            mail.send(msg)
        flash('Signalement envoyé.')
    return redirect(url_for('main.artwork', artwork_id=Comment.query.get_or_404(comment_id).artwork_id))