import json

from db import db
from flask import Flask, request
from db import User, Lobby, UserLobby, Course, Post, Comment

app = Flask(__name__)
db_filename = "study.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/api/lobbies/")
def get_all_lobbies():
    """
    Endpoint for getting all lobbies
    :return:
    """
    lobbies = [lobby.serialize() for lobby in Lobby.query.all()]
    return success_response({"lobbies": lobbies})


@app.route("/api/lobbies/", methods=["POST"])
def create_lobby():
    """
    Endpoint for creating a lobby
    :return:
    """
    body = json.loads(request.data)
    if (body.get("description", None) is None or body.get("location", None) is None or
            body.get("max_people", None) is None or body.get(
                "course_id", None) is None):
        return failure_response("Not all inputs provided", 400)

    course = Course.query.filter_by(id=body.get("course_id")).first()
    if course is None:
        return failure_response("Course not found")

    new_lobby = Lobby(description=body.get("description"), location=body.get("location"),
                      max_people=body.get("max_people"), course_id=body.get("course_id"))
    db.session.add(new_lobby)
    db.session.commit()
    return success_response(new_lobby.serialize(), 201)


@app.route("/api/lobbies/<int:lobby_id>/")
def get_lobby(lobby_id):
    """
    Endpoint for getting a lobby by id
    :return: 
    """
    lobby = Lobby.query.filter_by(id=lobby_id).first()
    if lobby is None:
        return failure_response("Lobby not found")
    return success_response(lobby.serialize())


@app.route("/api/lobbies/<int:lobby_id>/", methods=["DELETE"])
def delete_lobby(lobby_id):
    """
    Endpoint for deleting a Lobby
    :param lobby_id:
    :return:
    """
    lobby = Lobby.query.filter_by(id=lobby_id).first()
    if lobby is None:
        return failure_response("Lobby not found")
    db.session.delete(lobby)
    db.session.commit()
    return success_response(lobby.serialize(), 200)


@app.route("/api/users/")
def get_all_users():
    """
    Endpoint for getting all users
    :return:
    """
    users = [user.serialize() for user in User.query.all()]
    return success_response({"users": users})


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    :return:
    """
    body = json.loads(request.data)
    if body.get("name", None) is None:
        return failure_response("Not all inputs provided", 400)

    new_user = User(name=body.get("name"))
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by id
    :param user_id:
    :return:
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    return success_response(user.serialize())


@app.route("/api/lobbies/<int:lobby_id>/add/", methods=["POST"])
def add_user_to_lobby(lobby_id):
    """
    Endpoint for adding a user to a lobby
    :return:
    """
    body = json.loads(request.data)
    if body.get("user_id") is None or body.get("type") is None:
        return failure_response("Not all inputs provided", 400)
    user_id = body.get("user_id")
    user_type = body.get("type")

    lobby = Lobby.query.filter_by(id=lobby_id).first()
    if lobby is None:
        return failure_response("Lobby not found")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    new_user_lobby = UserLobby(type=user_type, lobby_id=lobby_id, user_id=user_id)
    db.session.add(new_user_lobby)
    db.session.commit()
    return success_response(lobby.serialize())


@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding a course to a user
    :param course_id:
    :return:
    """
    body = json.loads(request.data)
    if body.get("user_id") is None:
        return failure_response("Not all inputs provided", 400)
    user_id = body.get("user_id")

    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    course.users.append(user)
    db.session.commit()
    return success_response(user.serialize())


@app.route("/api/courses/")
def get_courses():
    """
    Endpoint for getting all courses
    :return:
    """
    courses = [course.serialize() for course in Course.query.all()]
    return success_response({"courses": courses})


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating a course
    :return:
    """
    body = json.loads(request.data)
    if body.get("name", None) is None or body.get("code", None) is None:
        return failure_response("Not all inputs provided", 400)

    new_course = Course(code=body.get("code"), name=body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)


@app.route("/api/courses/<int:course_id>/")
def get_course(course_id):
    """
    Endpoint for getting a course by id
    :param course_id:
    :return:
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")

    return success_response(course.serialize())


##################################


@app.route("/api/posts/")
def get_posts():
    """
    Endpoint for getting all posts
    :return:
    """
    posts = [post.serialize() for post in Post.query.all()]
    return success_response({"posts": posts})


@app.route('/api/posts/', methods=["POST"])
def create_post():
    """
    Endpoint for creating a post
    :return:
    """
    body = json.loads(request.data)
    if body.get("title", None) is None or body.get("content", None) is None or body.get("user_id", None) is None:
        return failure_response("Not all inputs provided", 400)

    new_post = Post(title=body.get("title"), content=body.get("content"), user_id=body.get("user_id"))
    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize(), 201)


@app.route('/api/posts/<int:post_id>/')
def get_post(post_id):
    """
    Endpoint for getting a specific post
    :param post_id:
    :return:
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found")

    return success_response(post.serialize())


@app.route('/api/posts/<int:post_id>/', methods=["DELETE"])
def delete_post(post_id):
    """
    Endpoint for deleting a post
    :param post_id:
    :return:
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found")
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize(), 200)


@app.route('/api/posts/<int:post_id>/comments/')
def get_comments(post_id):
    """
    Get all comments to a specific post
    :param post_id:
    :return:
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found")

    return success_response(post.serialize().get("comments"))


@app.route('/api/posts/<int:post_id>/comments/', methods=["POST"])
def create_comment(post_id):
    """
    Endpoint for creating a comment
    :param post_id:
    :return:
    """
    body = json.loads(request.data)
    if body.get("content", None) is None or body.get("user_id", None) is None:
        return failure_response("Not all inputs provided", 400)

    new_comment = Comment(content=body.get("content"), post_id=post_id, user_id=body.get("user_id"))
    db.session.add(new_comment)
    db.session.commit()
    return success_response(new_comment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
