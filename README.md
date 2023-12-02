# CS-1998-CUClassConnect-Backend
App name: CUClassConnect

Link to Frontend: https://github.com/jedi244/Cornell-AppDev-Hack-Challenge.git


Overview: A web application where users can select courses and enter new lobbies, for discussion (Q&amp;A) and collaboration (meeting up). The application is designed to be run in a Docker container for ease of deployment and consistency across different environments.

![ss of design](https://github.com/JoshuaYeung-CS/CS-1998-CUClassConnect-Backend/assets/147670968/5554ef77-a629-44ac-a5bb-a539cc5e3f19)

**Routes**

- User: Endpoints for registering, logging in, and managing user profiles.
  
- Course: APIs to add, update, delete, and view courses.
  
- Lobby: APIs for creating lobbies for courses (get a lobby's information, create a lobby, get and create posts for a lobby).

- Posts and Comments: Functionality to allow users to create, edit, and delete posts and comments in lobbies.


**Database Models**

- User: Includes attributes like name, email, password, etc.

- Course: Details about courses: title, description, instructor

- Lobby: Information about lobbies: associated course, users.

- Post: Represents user-generated posts in lobbies.

- Comment: Related to posts, allowing threaded discussions


**Technical Stack**

- Backend Framework: Flask

- Database: SQLAlchemy with SQLite

- Containerization: Docker, Docker Compose
