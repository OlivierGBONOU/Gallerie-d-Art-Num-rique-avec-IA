# app/routes/user.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .. import db
from ..models import Artwork, User, Emotion
from ..forms import ArtworkForm, EditArtworkForm, ProfileForm, EmptyForm
from ..utils.emotion_analysis import analyze_emotion
from config import Config

bp = Blueprint('user', __name__)

@bp.route('/profile')
@login_required
def profile():
    artworks = Artwork.query.filter_by(user_id=current_user.id).all()
    form = EmptyForm()  # Instancier le formulaire pour la suppression
    return render_template('profile.html', user=current_user, artworks=artworks, form=form)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ArtworkForm()
    form.emotion_target.choices = [(e.name, e.name) for e in Emotion.query.all()]
    if form.validate_on_submit():
        if not form.image.data:
            flash('Veuillez sélectionner une image.')
            return redirect(url_for('user.upload'))
        filename = secure_filename(form.image.data.filename)
        image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        form.image.data.save(image_path)
        artwork = Artwork(
            title=form.title.data,
            description=form.description.data,
            image_path=filename,
            emotion_target=form.emotion_target.data,
            emotion_detected=analyze_emotion(form.description.data),
            user_id=current_user.id
        )
        db.session.add(artwork)
        db.session.commit()
        flash('Œuvre ajoutée avec succès.')
        return redirect(url_for('user.profile'))
    return render_template('upload.html', form=form)

@bp.route('/edit/<int:artwork_id>', methods=['GET', 'POST'])
@login_required
def edit(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.user_id != current_user.id:
        flash('Vous n’êtes pas autorisé à modifier cette œuvre.')
        return redirect(url_for('user.profile'))
    form = EditArtworkForm()
    form.emotion_target.choices = [(e.name, e.name) for e in Emotion.query.all()]
    if form.validate_on_submit():
        artwork.title = form.title.data
        artwork.description = form.description.data
        artwork.emotion_target = form.emotion_target.data
        artwork.emotion_detected = analyze_emotion(form.description.data)
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            form.image.data.save(image_path)
            artwork.image_path = filename
        db.session.commit()
        flash('Œuvre mise à jour.')
        return redirect(url_for('user.profile'))
    if request.method == 'GET':
        form.title.data = artwork.title
        form.description.data = artwork.description
        form.emotion_target.data = artwork.emotion_target
    return render_template('edit.html', form=form, artwork=artwork)

@bp.route('/delete/<int:artwork_id>', methods=['POST'])
@login_required
def delete(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    if artwork.user_id != current_user.id:
        flash('Vous n’êtes pas autorisé à supprimer cette œuvre.', 'danger')
        return redirect(url_for('user.profile'))
    db.session.delete(artwork)
    db.session.commit()
    flash('Œuvre supprimée.', 'success')  # Ajouter la catégorie 'success'
    return redirect(url_for('user.profile'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data, User.id != current_user.id).first():
            flash('Ce nom d’utilisateur est déjà pris.')
            return redirect(url_for('user.edit_profile'))
        if User.query.filter(User.email == form.email.data, User.id != current_user.id).first():
            flash('Cet email est déjà utilisé.')
            return redirect(url_for('user.edit_profile'))
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            avatar_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            form.avatar.data.save(avatar_path)
            current_user.avatar = filename
        db.session.commit()
        flash('Profil mis à jour.')
        return redirect(url_for('user.profile'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    return render_template('edit_profile.html', form=form)