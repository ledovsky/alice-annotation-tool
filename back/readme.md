
## Назначение приложений DRF

* main_app. Contains functionality for the annotation web app: plotting, stats, frontend-friendly views
* data_app. Contains Dataset, Subject, IC and Annotation models. Handles the data uploading
* downloads_app. Creates files for the downloading

### Local Dev Setup

First, a virtual env should be created and activated

Ensure that postgres libraries are install. For mac

```
brew install libpq --build-from-source
brew install openssl
```

Also, install psycopg2-binaries in case of problems

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy .env.sample to .env.dev and paste necessary variables. Then you can export the variables via

```
set -o allexport; source .env.dev; set +o allexport
```

Backend runs at port 8000 using

```
cd back/drf_backend
python manage.py runserver
```

Development db initialization could be used by

```
python manage.py init_dev_db
```

Admin user is created with login and password admin/admin

## How to monitor max id values

Several times we got an error about wrong sequence value for ids for some tables.

Helper function

```sql
CREATE OR REPLACE function get_max_id(tablename varchar)
	returns bigint as 
$$
declare 
	max_id bigint;
begin 
	execute 'SELECT max(id) max_id FROM ' || quote_ident(tablename)
	into max_id;
	return max_id;
end
$$
language plpgsql;
```

SQL for monitoring sequence values and max ids for each table

```sql
select
	*,
	replace(sequencename, '_id_seq', '') table_name,
	get_max_id(replace(sequencename, '_id_seq', '')) max_id,
	sequencename,
	last_value
FROM pg_catalog.pg_sequences 
;
```
