# Infinite Craft Architecture

## Run Locally

### Set Up Environment Variables
Save a file in this directory named `.env`, or just export them.\
You can replace the Redis and Postgres connection strings with your own, or keep them as is to use the local Docker instances.
```sh
REDIS_CONNECTION_STRING=redis://:@127.0.0.1:6379/0
POSTGRES_CONNECTION_STRING=postgresql://postgres:password@127.0.0.1:5432/test_db
OPEN_AI_API_KEY={your_key_here}
```

### Start Services
Install Dependencies: `make deps`\
Start Docker: `make up-docker`\
Run Initial Database Migration: `make migrate`\
Start Everything: `make up`