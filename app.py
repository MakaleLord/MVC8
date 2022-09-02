#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, abort, request, flash

import random, math

from .decorators import welcome_screen
from .post_models import (
    create_post_table,
    get_posts,
    find_post,
    random_post,
    insert_post,
    count_posts,
    paginated_posts,
)

app = Flask(__name__)

######## SET THE SECRET KEY ###############
# You can write random letters yourself or
# Go to https://randomkeygen.com/ and select a
# random secret key
####################
app.secret_key = "Y57i"

posts_per_page = 3

with app.app_context():
    create_post_table()


@app.route("/")
@welcome_screen
def home_page():
    total_posts = count_posts()
    pages = math.ceil(total_posts / posts_per_page)
    current_page = request.args.get("page", 1, int)
    posts_data = paginated_posts(current_page, posts_per_page)
    return render_template(
        "page.html",
        posts=posts_data,
        current_page=current_page,
        total_posts=total_posts,
        pages=pages,
    )


@app.route("/welcome")
def welcome_page():
    return render_template("welcome.html")


@app.route("/<post_link>")
@welcome_screen
def post_page(post_link):
    post = find_post(post_link)
    if post:
        return render_template("post.html", post=post)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.route("/random")
def random_post_page():
    post = random_post()
    return redirect(url_for("post_page", post_link=post["permalink"]))


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("newpost.html", post_data={})
    else:
        post_data = {
            "title": request.form["post-title"],
            "author": request.form["post-author"],
            "content": request.form["post-content"],
            "permalink": request.form["post-title"].replace(" ", "-"),
            "tags:": request.form["post-tags"],
        }

        existing_post = find_post(post_data["permalink"])
        if existing_post:
            app.logger.warning(f"duplicate post: {post_data['title']}")
            flash(
                "error", "There's already a similar post, maybe use a different title"
            )
            return render_template("newpost.html")
        else:
            insert_post(post_data)
            app.logger.info(f"new post: {post_data['title']}")
            flash("success", "Congratulations on publishing another blog post.")
            return redirect(url_for("post_page", post_link=post_data["permalink"]))

###### E X E R C I S E S #########
#
#  Exercise 1: Examine the server log
#  Exercise 2: Make your own log events
#  Exercise 3: Show a success message on publishing a new blog post.
#  Exercise 4: Give a category to your flash messages.
#
#  Homework 1: Make the navbar collapsible
#              In `layout.html`, add a collapsible navbar using Bootstrap classes
#               -pick a `container` size for the collapse breakpoint
#               -`container-fluid` is always 100% width, so it won't work.
#               -put the `.navbar-nav` and `form` inside a `div` with class `collapse navbar-collapse`
#               -add a "hamburger" button to appear when the navbar collapses
#               <-- hamburger button -->
#               <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar">
#                   <span class="navbar-toggler-icon"></span>
#               </button>
#
# Navbar Docs Link: https://getbootstrap.com/docs/5.2/components/navbar/

#
#  Homework 2: Use flash message to show the exisitng post error as well.
#             - In the new_post() function, inside the if that checks existing_post.
#             - Use flash to throw an error message that "There's already a similar post, maybe use a different title."
#             - Remove the error from render_template as template variable
#            In layout.html,
#             - In the if statement that checks the category of flash message
#             - Add an else if statement to check if category is error.
#             - Inside else if, add a div with class ui alert alert-danger w-50 mx-auto m-3
#             - Inside above div,
#             - Add an h4 with class alert-heading with some error heading of your choice.
#             - Add a p tag with message
#
# Alert docs Link: https://getbootstrap.com/docs/5.2/components/alerts/
##################################
