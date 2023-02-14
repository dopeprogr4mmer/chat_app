## CHAT_APP

### Step 1: _Clone the repository_
 -  On terminal run >
 ```git clone https://github.com/phantom791/chat_app.git```

### Step 2: _Install requirements_
 -  Create a virtual environment run >
```pyhton -m venv myvenv```
 -  Activate the virtual environment run >
 ```myvenv\scripts\activate```
 -  Install the requirements run >
 ```pip install -r requirements.txt```
 
### Step 3: _Run the application_
 -  run >
 ```pyhton chat_app.py```
 
### Step 4: _Run the tests_
 -  On an another terminal activate the virtual environment as above
 -  run >
 ```pyhton tests.py```
 
## NOTE: 
### Please change the variables 'username' and 'groupname' in tests.py everytime you run the script. Running the script creates entries in DB which may throw assertion errors the next time you run the script with the same arguments.
 
