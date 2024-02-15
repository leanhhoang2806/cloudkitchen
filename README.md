black . && docker-compose down -v && docker-compose up -d --build

# Auto generate data model
sqlacodegen postgresql://your_user:your_password@localhost:5432/your_dbname

# to run integration test
1. Spin up all needed containers
2. Run the test suite from the command line `cloudkitchen-BE hoang$ pytest src/tests/`