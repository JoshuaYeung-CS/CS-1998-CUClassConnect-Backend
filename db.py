from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"))
)


class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    # netid = db.Column(db.String, nullable=False)
    courses = db.relationship("Course", secondary=association_table, back_populates="users")
    user_lobby = db.relationship("UserLobby", cascade="delete")
    posts = db.relationship("Post", cascade="delete")
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a User object
        :param kwargs:
        """
        self.name = kwargs.get("name", "")
        # self.netid = kwargs.get("netid", "")

    def serialize(self):
        """
        Serialize a User object
        :return:
        """
        return {
            "id": self.id,
            "name": self.name,
            # "netid": self.netid,
            "courses": [c.simple_serialize() for c in self.courses],
            "lobbies": [l.simple_serialize() for l in self.get_lobbies()],
            "posts": [p.simple_serialize() for p in self.posts],
            "comments": [c.simple_serialize() for c in self.comments]
        }

    def simple_serialize(self):
        """
        Serialize a User object without the courses, lobbies, posts, or comments fields
        :return:
        """
        return {
            "id": self.id,
            "name": self.name,
            # "netid": self.netid
        }

    def get_lobbies(self):
        """
        Get all lobbies for a user
        :return:
        """
        query = UserLobby.query.filter_by(user_id=self.id)
        lobby_list = []
        for user_lobby in query:
            lobby_list.append(Lobby.query.filter_by(id=user_lobby.lobby_id).first())
        return lobby_list


class Lobby(db.Model):
    """
    Lobby Model
    """
    __tablename__ = "lobbies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    max_people = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    user_lobby = db.relationship("UserLobby", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a Lobby object
        :param kwargs:
        """
        self.description = kwargs.get("description", "")
        self.location = kwargs.get("location", "")
        self.max_people = kwargs.get("max_people", -1)
        self.course_id = kwargs.get("course_id", -1)

    def serialize(self):
        """
        Serialize a Lobby object
        :return:
        """

        return {
            "id": self.id,
            "description": self.description,
            "location": self.location,
            "max_people": self.max_people,
            "course": Course.query.filter_by(id=self.course_id).first().simple_serialize(),
            "owner": [o.simple_serialize() for o in self.get_users_by_type("owner")],
            "users": [u.simple_serialize() for u in self.get_users_by_type("user")]
        }

    def simple_serialize(self):
        """
        Serialize a Lobby object without the owner or users fields
        :return:
        """
        return {
            "id": self.id,
            "description": self.description,
            "location": self.location,
            "max_people": self.max_people,
            "course": Course.query.filter_by(id=self.course_id).first().simple_serialize()
        }

    def get_users_by_type(self, type):
        """
        Get users in a lobby by type of user
        :param type:
        :return:
        """
        query = UserLobby.query.filter_by(lobby_id=self.id, type=type)
        user_list = []
        for user_lobby in query:
            user_list.append(User.query.filter_by(id=user_lobby.user_id).first())
        return user_list


class UserLobby(db.Model):
    """
    User-Lobby Model
    """
    __tablename__ = "user_lobby"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)
    lobby_id = db.Column("Lobby", db.ForeignKey("lobbies.id"), nullable=False)
    user_id = db.Column("User", db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a User-Lobby object
        :param kwargs:
        """
        self.type = kwargs.get("type", "")
        self.lobby_id = kwargs.get("lobby_id")
        self.user_id = kwargs.get("user_id")


class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.Text, nullable=False)
    users = db.relationship("User", secondary=association_table, back_populates="courses")
    lobbies = db.relationship("Lobby", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a Course object
        :param kwargs:
        """
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serialize a Course object
        :return:
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "users": [u.simple_serialize() for u in self.users],
            "lobbies": [l.simple_serialize() for l in self.lobbies],
        }

    def simple_serialize(self):
        """
        Serialize a Course object without the users or lobbies field
        :return:
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }


class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a Post object
        :param kwargs:
        """
        self.title = kwargs.get("title", "")
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id")

    def serialize(self):
        """
        Serialize a Post object
        :return:
        """
        return {
            "id": self.id,
            "user": User.query.filter_by(id=self.user_id).first().simple_serialize(),
            "title": self.title,
            "content": self.content,
            "comments": [c.simple_serialize() for c in self.comments],
        }

    def simple_serialize(self):
        """
        Serialize a Post object without the comments or user field
        :return:
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content
        }


class Comment(db.Model):
    """
    Comment Model
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Comment object
        :param kwargs:
        """
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id")
        self.post_id = kwargs.get("post_id")

    def serialize(self):
        """
        Serialize a Comment object
        :return:
        """
        return {
            "id": self.id,
            "user": User.query.filter_by(id=self.user_id).first().simple_serialize(),
            "post": Post.query.filter_by(id=self.post_id).first().simple_serialize(),
            "content": self.content,
        }

    def simple_serialize(self):
        """
        Serialize a Comment object without the user or post field
        :return:
        """
        return {
            "id": self.id,
            "content": self.content
        }
