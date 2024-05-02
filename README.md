black . && docker-compose down -v && docker volume prune -f  && docker-compose up -d --build

# Auto generate data model
sqlacodegen postgresql://your_user:your_password@localhost:5432/popo_24

![Architecture Diagram](readme-media/popo24-architect.png)


# to run integration test
1. Spin up all needed containers
2. `export PYTHONDONTWRITEBYTECODE=1`
3. Run the test suite from the command line `cloudkitchen-BE hoang$ pytest src/tests/`

# Get the token from front end
1. Login and find the token at 


# Managing github actions note
1. If the build is stuck, Just  cancel the build and restart

# DevOps philosiphy
1. The CI/CD end at pushing the image to ECR
2. Terraform will take care of the provision on ECS
3. For the revision of this variable `secrets.ECS_TASK_DEFINITION` every time terraform `apply` happened, make sure to change the revision (manually doing this for now until filter references)

# Debugger:
1. import logging
2. use logging.info() to print out stuff


# Managing database migrations
`alembic revision -m <name>`

# To run the test suite
1. Spin the the containers based on instructions above, wait for container to be ready
2. under the same directory as `src`, run `pytest -s test/{your_file_directory}`


# Notes:
1. To manage UUID of a system. it's better to generate it at the application level. don't generate it at the database level. to avoid the case where a commit needs to happen then using this UUID in other tables, the commits will lose the transaction.
2. Secondly, database is strictly for `storing` data, no logic should happen to store data. Just a plain data, get ready to write

3. For security purposes, never shown any other UUID except for the UUID of the person who made a request. 