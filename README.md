# apiAssignment
You can run the main REST API service by using python main.py in the root directory.
For database, I am using redis, So you can view the users and the token from redis-cli.

# Curl Commands to test each use case
## Task1 
#### Signup of user:
Windows->curl "http://127.0.0.1:8080/signup" --header "Content-Type: application/json" --data-raw "{\\"email\\": \\"soham@gmail.com\\", \\"password\\": \\"soham123@\\"}"

## Task2 Signin of user:




# Redis Commands
keys * -> to get all the keys present inside the redis database.

hkeys users -> to get all the users username who made an account.

hget users <user_account_name> -> to get the encrypted password for the user account.

smembers revoke_tokens -> to get all the tokens that have been revoked

get refresh_token:<user_account_name> -> to get the refresh token of that particular user.
