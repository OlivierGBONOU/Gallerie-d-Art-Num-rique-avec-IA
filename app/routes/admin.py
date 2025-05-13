# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..forms import EmptyForm
from ..models import User, Artwork, Comment, Report, Notification
from ..utils.decorators import admin_required
from .. import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    artworks = Artwork.query.all()
    comments = Comment.query.all()
    reports = Report.query.filter_by(resolved=False).all()
    return render_template('admin/dashboard.html', users=users, artworks=artworks, comments=comments, reports=reports)

@bp.route('/notifications')
@login_required
@admin_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    form = EmptyForm()
    return render_template('notifications.html', notifications=notifications, form=form)

@bp.route('/notification/<int:notification_id>/mark_read', methods=['POST'])
@login_required
@admin_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash('Non autorisé.')
        return redirect(url_for('admin.notifications'))
    notification.is_read = True
    db.session.commit()
    flash('Notification marquée comme lue.')
    return redirect(url_for('admin.notifications'))

@bp.route('/moderation')
@login_required
@admin_required
def moderation():
    form = EmptyForm()
    reports = Report.query.filter_by(resolved=False).all()
    return render_template('admin/moderation.html', reports=reports, form=form)

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
    artwork = Artwork.query.get_or_404(artwork_id)
    db.session.delete(artwork)
    db.session.commit()
    flash('Œuvre supprimée.')
    return redirect(url_for('admin.dashboard'))

@bp.route('/admin/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Commentaire supprimé.')
    return redirect(url_for('admin.dashboard'))

@bp.route('/admin/block_user/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()
    flash('Utilisateur bloqué avec succès.', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/moderate/<int:report_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def moderate(report_id):
    report = Report.query.get_or_404(report_id)
    if request.method == 'POST':
        if 'delete' in request.form:
            if report.artwork_id:
                artwork = Artwork.query.get(report.artwork_id)
                db.session.delete(artwork)
            elif report.comment_id:
                comment = Comment.query.get(report.comment_id)
                db.session.delete(comment)
            db.session.delete(report)
            db.session.commit()
            flash('Signalement traité et contenu supprimé.', 'success')
        elif 'dismiss' in request.form:
            db.session.delete(report)
            db.session.commit()
            flash('Signalement ignoré.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/moderation.html', report=report)