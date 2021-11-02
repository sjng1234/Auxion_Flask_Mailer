# Auxion_Flask_Mailer

## Project Setup
 
## Step 1: If virtualenv is not installed as a package (1st Time)
```
pip install virtualenv
```

## Step 2: Create a virtualenv (1st Time)
```
# Create virtualenv
python3 -m venv venv

# Create virtualenv (for windows)
py -3 -m venv venv
```

## Step 3: Activate virtualenv
```
# Activate virualenv:
. venv/bin/activate

# Activate virualenv (for windows):
venv\Scripts\activate
```

## Step 4: Install requirements
```
pip install -r requirements.txt
```

## Step 5: Run the App
```
python application.py
```

## To update requirements after adding new packages
```
pip freeze > requirements.txt 
```

## To exit virtualenv
```
deactivate
```
