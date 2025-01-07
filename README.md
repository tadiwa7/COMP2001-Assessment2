# Trail Service Microservice

This microservice provides a RESTful API to manage  trails. It supports features like user authentication, role-based authorization, and CRUD operations for trail management.

## Features
- **Authentication:** User authentication using an external authenticator API.
- **Authorization:** Role-based access control with two roles:
  - **Admin:** Can create, update, and delete trails.
  - **General User:** Can view trails.
- **CRUD Operations:** Manage trail data, including creating, reading, updating, and deleting trails.
- **OpenAPI Compliance:** API specification provided using `swagger.yml`.
- **Containerized Deployment:** Dockerized microservice for easy deployment.

## Technologies Used
- **Python 3.9**
- **Flask:** Framework for creating the RESTful API.
- **Connexion:** Ensures compliance with the OpenAPI specification.
- **Microsoft SQL Server:** Database for storing trail and user information.
- **Docker:** Used to containerize the application.
