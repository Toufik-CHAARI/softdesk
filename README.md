# softdesk API Documentation

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Projects](#projects)
- [Contributors](#contributors)
- [Issues](#issues)
- [Comments](#comments)
- [PEP8 Code compliance Report](#pep8-code-compliance-report)

***
## Installation

- Clone the project
'git clone https://github.com/Toufik-CHAARI/softdesk.git'

- check whether pipenv is installed in your system
  'pipenv --version'

- If pipenv is not installed run the following command
  'brew install pipenv' (on mac)

- create the following hidden folder
  'mkdir .venv'

- Install django for populating the venv folders
 'pipenv install django'

- Change directory
  'cd softdesk'

- Run virtual environment
 'pipenv shell'

- Change directory
 'cd softdesk'

- Run local server
  'python3 manage.py runserver'

The below superuser has been created for testing the application

username: test
password: test


***

## Authentication

### 1. Register a new user
Endpoint: /api/register/

parameters 
username :
password :
age :
can_be_contacted :
can_data_be_shared :

Methods:

POST: Register a new user.
Response:

HTTP_201_CREATED if successful.
HTTP_400_BAD_REQUEST with error details if there's an issue with the data.


### 2. Obtain a JWT Token
Endpoint: /api/token/

Methods:

POST: Get JWT Token by providing a valid username and password.

parameters 
username :
password :

### 3. Refresh a JWT Token
Endpoint: /api/token/refresh/

Methods:

POST: Refresh JWT Token using a valid refresh token.

Header must contain refresh token


### 4. Get User Data
Endpoint: /api/getuserdata/

Methods:

GET: Get data of all users (if superuser) or get the data of the authenticated user.

Permissions:
Authenticated users can fetch their own data.
Superusers can fetch data for all users.

Header must contain token


#### 5. User Detail
Endpoint: /api/user_detail/<int:user_id>/

Methods:

GET: Fetch the data for the specified user.
PUT: Update data for the specified user.
DELETE: Delete the specified user.
Permissions:

Users can only fetch, update, or delete their own data unless they are a superuser.
Superusers can perform actions on all users.

Header must contain token
For updating (PUT) the following parameters :

username :
password :
age :
can_be_contacted :
can_data_be_shared :




## Projects
Endpoint: /api/projects/

Methods:

GET: Retrieve a list of projects providing that the authenticated user is an author or contributor to.
POST: Create a new project.
PUT: Update an existing project's details. The author cannot be changed.
DELETE: Delete a project.

Permissions:


Header must contain token
parameters for POST & PUT are
name :
description :
project_type :
author :

## Contributors
Endpoint: /api/contributors/

Methods:

GET: Retrieve a list of contributors.
POST: Add a contributor to a project.
PUT: Update a contributor's details.
DELETE: Remove a contributor from a project.


Permissions: Only author,contributors of a project as well as superuser can add a contributor to a project

Header must contain token
parameters for POST & PUT are

user (user_id):
project (project_id):

## Issues

Endpoint: /api/issues/

Methods:

GET: Retrieve a list of issues from projects the authenticated user is involved in.
POST: Create a new issue.
PUT: Update an issue's details.
DELETE: Delete an issue.

Permissions: Only author,contributors of a project as well as superuser can add an Issue to a project

Header must contain token
parameters for POST & PUT are

project (project_id):
name :
tag :
description :
author (user_id) :
assignee (user_id) :


## Comments
Endpoint: /api/comments/

Methods:

GET: Retrieve a list of comments from issues of projects the user is involved in.
POST: Create a new comment on an issue.
PUT: Update a comment's details.
DELETE: Delete a comment.

Permissions: Only author,contributors of a Project as well as superuser can add a Comment to an issue

Header must contain token
parameters for POST & PUT are

description :
author (user_id):
issue (issue_id)

***

## PEP8 Code compliance Report