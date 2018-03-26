# Key-value-pairs-storage
Flask webapp allowing users to create and search their key value pairs

##Dependencies
-Flask==0.11.1
-Flask-Login==0.4.1
-Flask-Migrate==2.1.1
-Flask-SQLAlchemy==2.3.2
-SQLAlchemy==1.2.5
-Werkzeug==0.11.11
-WTForms==2.1

##Database setup
1. Create your database (I used sqlite3 to create database "kvp_storage").
2. In __init__.py, set app.config['SQLALCHEMY_DATABASE_URI'] to point to the database you just created.
3. In your project directory, run "flask db upgrade" from the terminal.

#API

##GET KeyValuePair
base_url/api/kvp/get/<key>
Arguments: A single url parameter
Returns: A KeyValuePair with key matching the argument

##SET KeyValuePair
base_url/api/kvp/set
Arguments: A JSON with structure {"key": "my_key", "value": "my_value"}
Returns: A success message which includes the KeyValuePair just set
Note: If a KeyValuePair with the desired key already exists, then only the value is modified. If the KeyValuePair is newly created, no user is tied to it.
