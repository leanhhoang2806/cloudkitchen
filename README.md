black . && docker-compose down -v && docker volume prune -f  && docker-compose up -d --build

# Auto generate data model
sqlacodegen postgresql://your_user:your_password@localhost:5432/popo_24

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