from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

def get_posts(sortForm):
    sortnum = int(sortForm.sortby.data)
    if sortnum == 1:
        return Post.query.order_by(Post.timestamp.desc())
    if sortnum == 2:
        return Post.query.order_by(Post.title.desc())
    elif sortnum == 3:
        return Post.query.order_by(Post.likes.desc())
    else:
        return Post.query.order_by(Post.happiness_level.desc())
        

@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sortForm = SortForm()
    if sortForm.validate_on_submit():
        if sortForm.myposts.data:
            posts = get_posts(sortForm).filter_by(user_id = current_user.id)
        else:
            posts = get_posts(sortForm)
    else:
        posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all(), sform = sortForm)

@bp_routes.route('/postsmile', methods=['GET', 'POST'])
@login_required
def postsmile():
    postForm = PostForm()
    if postForm.validate_on_submit():
        newPost = Post(title = postForm.title.data, 
            user_id = current_user.id, happiness_level = postForm.happiness_level.data,
            body = postForm.body.data)
        for tempTag in postForm.tag.data:
            newPost.tags.append(tempTag)
        db.session.add(newPost)
        db.session.commit()
        flash("Post " + newPost.title + " is created")
        return redirect(url_for('routes.index')) 
    return render_template("create.html", form = postForm)

@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    if thepost is None:
        flash("Post with id '{}' not found").format(post_id)
        return redirect(url_for("routes.index"))
    thepost.likes += 1
    db.session.add(thepost)
    db.session.commit()
    return redirect(url_for("routes.index"))

@bp_routes.route('/delete/<post_id>', methods=['DELETE', 'POST'])
@login_required
def delete(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    print(thepost.id)
    if thepost is None:
        flash("Post with id '{}' not found").format(post_id)
        return redirect(url_for("routes.index"))
    for t in thepost.tags:
        thepost.tags.remove(t)
    db.session.add(thepost)
    db.session.commit()
    db.session.delete(thepost)
    db.session.commit()
    flash("Post succesfully deleted")
    return redirect(url_for("routes.index"))

    