from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.core import BooleanField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app.Model.models import Post, Tag

def get_tags():
    return Tag.query.all()
 
def get_tagLabel(tag):
    return tag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tag =  QuerySelectMultipleField( 'Tag',
        query_factory= get_tags,
        get_label= get_tagLabel,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput() )
    body = TextAreaField("Body", validators=[DataRequired(),Length(min = 1, max = 1500)])
    submit = SubmitField('Post')
    
class CommentForm(FlaskForm):
    body = TextAreaField("Body", validators=[DataRequired(),Length(min = 1, max = 1500)])
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sortby = SelectField('Sort By', choices = [(1,' Date'),(2, 'Official WSU Events'),(3, 'Greek Row Events'), (4, 'WSU-Club-Events'), (5, 'Open-to-All'),(6, '#-of-upvotes')])
    myposts = BooleanField('Display my posts only')
    submit = SubmitField('Refresh')