# apiAssignment
You can run the main REST API service by using python main.py in the root directory.
For database, I am using redis, So you can get the users and the token from redis-cli.



# Redis Commands
keys * -> to get all the keys present inside the redis database.

hkeys users -> to get all the users username who made an account.

hget users <user_account_name> -> to get the encrypted password for the account.
