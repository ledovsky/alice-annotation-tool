# ALICE Annotation Tool

## How to set up dev (no docker-compose)

Run postgres on 5432

```
docker run -p 5432:5432 -d -e POSTGRES_PASSWORD=pwd postgres
```

Run redis on 6379

```
docker run --name some-redis -d -p 6379:6379 redis
```

Go through readme.md from backend


## How to set up dev

Create a docker network if not created

```
docker network create reverse-proxy
```

Set up .env files.

```
cp back/.env.sample back/.env
cp postgres/.env.sample postgres/.env
```

For production change secret key in back/.env and postgres password in postgres/.env.

### First start up

Build docker-compose. You need at least 8 Gb RAM for the build

```
docker-compose build
```

First, we need to init postgres db

```
docker-compose up postgres
```

After initialization is done exit docker-compose and start all the containers

```
docker-compose up
```

If everything is fine you can run it in the background mode

```
docker-compose up -d
```

### Updating

Use a regular docker-compose command sequence

```
docker-compose down
docker-compose build
docker-compose up -d
```


### Set up dev db

```
docker exec -it eeg-ic-annotation_back_1 /bin/bash

# then inside the container
cd drf_backend
python manage.py init_dev_db
python manage.py update_component_plots --dataset test_dataset
python manage.py update_links --dataset test_dataset
python manage.py update_plots --dataset test_dataset
```

You can login as admin/admin

## How to set up prod

Set up proper .env files

TODO - adding admin user

## Db dump

```
pg_dump --host localhost --port 5433 -U postgres postgres > eeg_ica_dump
```

```
psql --host=localhost --port 5433 -U postgres postgres_2 < eeg_ica_dump
```
