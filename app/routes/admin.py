# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Artwork, Comment, Report
from .. import db

bp = Blueprint('admin', __name__)

@bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    users = User.query.all()
    artworks = Artwork.query.all()
    comments = Comment.query.all()
    return render_template('admin/dashboard.html', users=users, artworks=artworks, comments=comments)

@bp.route('/admin/moderation')
@login_required
def moderation():
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    reports = Report.query.filter_by(resolved=False).all()
    return render_template('admin/moderation.html', reports=reports)

@bp.route('/admin/resolve_report/<int:report_id>', methods=['POST'])
@login_required
def resolve_report(report_id):
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    report = Report.query.get_or_404(report_id)
    report.resolved = True
    db.session.commit()
    flash('Signalement résolu.')
    return redirect(url_for('admin.moderation'))

@bp.route('/admin/delete_artwork/<int:artwork_id>', methods=['POST'])
@login_required
def delete_artwork(artwork_id):
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    artwork = Artwork.query.get_or_404(artwork_id)
    db.session.delete(artwork)
    db.session.commit()
    flash('Œuvre supprimée.')
    return redirect(url_for('admin.dashboard'))

@bp.route('/admin/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Commentaire supprimé.')
    return redirect(url_for('admin.dashboard'))

@bp.route('/admin/block_user/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash('Vous n’avez pas la permission d’accéder à cette page.')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Impossible de bloquer un administrateur.')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur bloqué.')
    return redirect(url_for('admin.dashboard'))