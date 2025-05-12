# Formulaires Flask-WTF
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

class EmptyForm(FlaskForm):
    """Formulaire vide utilisé pour valider le jeton CSRF uniquement."""
    pass

class LoginForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])

class ArtworkForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Images uniquement (.jpg, .png)')])
    emotion_target = SelectField('Émotion cible', validators=[DataRequired()], choices=[])
    submit = SubmitField('Soumettre')

class EditArtworkForm(ArtworkForm):
    image = FileField('Image (facultatif)', validators=[FileAllowed(['jpg', 'png'], 'Images uniquement (.jpg, .png)')])
    submit = SubmitField('Mettre à jour')

class ProfileForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png'], 'Images uniquement (.jpg, .png)')])
    submit = SubmitField('Mettre à jour')