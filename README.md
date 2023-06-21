## Running the App

### Requirements to run the app
1. Python 3.6 or above
2. Node 16 or above

Make a copy of the `.env.sample` files present in the `server` and `client` folders and name them as `.env`.
Replace the content with your appropriate values.
The `.env` file in the `client` folder will contain the Vite server url. This can be left unchanged.
The `.env` file in the `server` folder will contain the database url and the secret key for the JWT token. The secret key for the JWT token can be left unchanged for development purposes, but the database url will need to be changed. Instructions for be are given below.


### Instructions to run the app
Depending on your Python install, you may need to use `python3` and `pip3` instead of `python` and `pip` respectively.

1. To run the Flask server: 
    Change directory to the server folder: `cd server`
    Create a venv in the server folder: `python -m venv venv`
    Activate the virtual environment
    Install the dependencies : `pip install -r requirements.txt`
    Run the server: `python app.py`

2. To run the VueJS client: 
    Change directory to the client folder: `cd client`
    Install the dependencies: `npm install`
    Run the application: `npm run dev`


### Making a Cloud MongoDB database
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and create an account.
2. Create a new project and a new cluster.
3. Create a new project named `test_database`.
4. Click on the connect button and select the appropriate options.(Note: when replacing <password>, make sure to use your user password and not your account password)
5. Copy the connection string and paste it into the `MONGO_URI` key in the `.env` file in the `server` folder.

### Creating Yelp Api Key
1. Go to [Yelp account](https://www.yelp.com/developers/v3/manage_app) and create/login to an account
2. Enter in the necessary information into the fields
3. Copy the API key given and paste it into the `YELP_API_KEY` key in the `.env` file in the `server` folder