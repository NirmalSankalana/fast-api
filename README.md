# fast API development

This microservice is responsible for managing smart chatbot operations.

How to set up the project.

1. Install python 3.8 or above if not available
2. Create virtual environment name env in the project folder : python -m venv env
3. Move to the project folder and activate virtual environment :
   - in Mac and Linux :source env/bin/activate
   - in Windows : run activate.bat file which is inside \env\Scripts folder
4. Install required libraries : `pip3 install -r requirements.txt`
5. After stop the project, deactivate virtual environment : deactivate

Run project

1. uvicorn uvicorn app.main:app --reload
2. Swagger documentation is available at : http://{host}:{port}/docs#

Save Dependancies

1. Run `pip freeze > requirements.txt` after installing any pip package

## ORM - Object Relational Mapping

Used in creating a "bridge" between object-oriented programs and, in most cases, relational databases. `SQLAlchemy` is an ORM.

![traditional_vs_orm](./img/traditional_vs_orm.png)

### What ORMs can do

- Defining Tables as python models
- Queries can exclusivly made through python code. No SQL is necessary.

### Models

![schema_models](./img/sqlalchemy_models.png)
SQLAlchemy models defines the how database tables looks like.

### Schema Models

![schema_models](./img/schema_models.png)
Schemas(Pydantic models) define the shape of the requests and responses.
