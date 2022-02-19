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
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    tag =  QuerySelectMultipleField( 'Tag',
        query_factory= get_tags,
        get_label= get_tagLabel,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput() )
    submit = SubmitField('Post')
    body = TextAreaField("Body", validators=[DataRequired(),Length(min = 1, max = 1500)])

class SortForm(FlaskForm):
    sortby = SelectField('Sort By', choices = [(1,' Date'),(2, 'Title'),(3, '# of likes'), (4, 'Happiness Level')])
    myposts = BooleanField('Display my posts only')
    submit = SubmitField('Refresh')