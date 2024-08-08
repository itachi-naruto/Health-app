

~/sehaty-api 

    |-- __init__.py
    |-- run.py	    	    # our run app file
    |-- config.py   	    # our config file with database connection
    |-- .env                # env url (db url)
    # Our Application Modules 
    |-- /app
        |-- __init__.py     # blueprint registration 
        |-- /users
            |-- __init__.py # empty file
            |-- model.py    # database table
            |-- service.py  # service and logic layer between database and api
            |-- routes.py   # routes of the api methods
        |-- /doctors
            |-- __init__.py # empty file
            |-- model.py    # database table
            |-- service.py  # service and logic layer between database and api
            |-- routes.py   # routes of the api methods
    |-- /...
        |-- __init__.py
            |-- ....py
            |-- ....py               
    |__ ..
    |__ ..
    |__ ..
    |__ .


**to use the code:**

1. clone the repository
2. pull the code
3. use develop branch
4. make your changes
5. push the code to development branch
