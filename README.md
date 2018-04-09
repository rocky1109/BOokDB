# BOokDB

## Heroku

Heroku app Url: https://bookdb-stage.herokuapp.com/


## APIs

Books: http://bookdb-stage.herokuapp.com/api/v1/books/ <br />
Genres: http://bookdb-stage.herokuapp.com/api/v1/genres/ <br />
Authors: http://bookdb-stage.herokuapp.com/api/v1/authors/ <br />
Publications: http://bookdb-stage.herokuapp.com/api/v1/publications/ <br />
Currencies: http://bookdb-stage.herokuapp.com/api/v1/currencies/ <br />



## How to run:

```
>> pip install -r requirements.txt


(BOokDB) >> python manage.py db init
Creating directory C:\Projects\BOokDB\migrations ... done
Creating directory C:\Projects\BOokDB\migrations\versions ... done
Generating C:\Projects\BOokDB\migrations\alembic.ini ... done
Generating C:\Projects\BOokDB\migrations\env.py ... done
Generating C:\Projects\BOokDB\migrations\README ... done
Generating C:\Projects\BOokDB\migrations\script.py.mako ... done
Please edit configuration/connection/logging settings in 'C:\\Projects\\BOokDB\\migrations\\alembic.ini' before proceeding.


(BOokDB) >> python manage.py db migrate
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'authors'
INFO  [alembic.autogenerate.compare] Detected added table 'currencies'
INFO  [alembic.autogenerate.compare] Detected added table 'genres'
INFO  [alembic.autogenerate.compare] Detected added table 'publications'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'books'
INFO  [alembic.autogenerate.compare] Detected added table 'books_authors'
INFO  [alembic.autogenerate.compare] Detected added table 'books_genres'
Generating C:\Projects\BOokDB\migrations\versions\6131a53048c9_.py ... done


(BOokDB) >> python manage.py db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 6131a53048c9, empty message

(BOokDB) >> python manage.py fake_data
5 data fields added to '<class 'app.products.models.Author'>'
3 data fields added to '<class 'app.products.models.Publication'>'
3 data fields added to '<class 'app.products.models.Genre'>'
3 data fields added to '<class 'app.products.models.Currency'>'

(BOokDB) >> python manage.py runserver
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 249-678-909

```
