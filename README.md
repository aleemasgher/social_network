# social_network
This project is about to user's social network.

Install all the packages from requirements.txt
```
pip3 install -r requirements.txt
```

To apply migrations
```
python3 manage.py migrate
```
To run local server
```
python3 manage.py runserver
```
For making Docker build
```
docker-compose build
```
Run docker build
```
docker-compose up
```
To shutdown docker 
```
docker-compose down
```

## Automation bot
Automation bot read the settings from the config file and perform the following task.

Register the new users in the database until it reaches number of users that set in config file.

Login a particular User.

Each login user create new posts until it reaches number of max posts per user that set in config file.

Like the users post according to config file settings.

User can not like its post.

One user can like a post one time.

Many user like many posts.
