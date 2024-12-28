# apiAssignment
To run locally, without docker-
You can run the main REST API service by using python main.py in the root directory.
For database, I am using redis(install it locally), So you can view the users and the token from redis-cli.

to run in docker container-
Go in root directory, and Run ```docker-compose up --build``` and your application should be up and running.

# Curl Commands to test each use case
(All the curl commands are for windows command prompt, for linux, remove the escape characters and change " to ')
## Task1 
#### Signup of user:
```
curl --location "http://localhost:8080/signup" --header "Content-Type: application/json" --data-raw "{\"email\": \"soham@gmail.com\", \"password\": \"soham123@\"}"
```

## Task2 
#### Signin of user with non-registered email
```
curl --location "http://localhost:8080/signin" --header "Content-Type: application/json" --data-raw "{\"email\\": \"random@gmail.com\", \"password\": \"soham123@\"}"
```

#### Signin of user with invalid credentials
```
curl --location "http://localhost:8080/signin" --header "Content-Type: application/json" --data-raw "{\"email\\": \"soham@gmail.com\", \"password\": \"soham\"}"
```

#### Signin of user with correct credentials returns access token and refresh token
```
curl --location "http://localhost:8080/signin" --header "Content-Type: application/json" --data-raw "{\"email\": \"soham@gmail.com\", \"password\": \"soham123@\"}"
```

## Task3
#### Mechanism of sending token along with a request from client to service. authorized route can only be accessed with access token and not refresh token. 
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Checking for refresh token accessing authorized route.
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <REFRESH_TOKEN>"
```

#### Checking for token is present or not
```
curl --location "http://localhost:8080/authorized"
```

#### Checking for Expiry, Expiry for access_token is 2 mins and Expiry for refresh_token is 5 mins.
After 2 mins, Send the same above curl command. 
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Checking for invalid token, in ACCESS_TOKEN field put any random characters, will give invalid token
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Checking for malformed token, If the header, doesnt contain keyword 'Bearer' will return token malformed
```
curl --location "http://localhost:8080/authorized" --header "Authorization: <ACCESS_TOKEN>"
```

## Task4
#### Revocation of token, Also checks for all the tasks in task3
```
curl --location --request POST "http://localhost:8080/revoke_token" --header "Authorization: Bearer <ACCESS_TOKEN>"
```
#### User can't sign in, once token has been revoked, After revoking a token, try this curl command
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <ACCESS_TOKEN>"
```

## Task5
#### Mechanism to refresh the access_token while refresh_token is still active. gives new access token
```
curl --location "http://localhost:8080/refresh" --header "Content-Type: application/json" --data "{\"refresh_token\":\"<REFRESH_TOKEN>\"}"
```

#### Task3 checks still hold,  you can call the authorized route with new access token
```
curl --location "http://localhost:8080/authorized" --header "Authorization: Bearer <NEW_ACCESS_TOKEN>"
```


# Redis Commands
keys * -> to get all the keys present inside the redis database.

hkeys users -> to get all the users username who made an account.

hget users <user_account_name> -> to get the encrypted password for the user account.

smembers revoke_tokens -> to get all the tokens that have been revoked

get refresh_token:<user_account_name> -> to get the refresh token of that particular user.



# Access Token Refresh Token Logic
![Diagram](https://github.com/user-attachments/assets/d4fd51b1-21b9-404e-9236-ea4da07c776f)

(1)  The client requests an access token by authenticating with the authorization server and presenting an authorization grant.

(2)  The authorization server authenticates the client and validates the authorization grant, and if valid, issues an access token and a refresh token.
  
(3)  The client makes a protected resource request to the resource server by presenting the access token.
  
(4)  The resource server validates the access token, and if valid, serves the request.
  
(5)  Steps (3) and (4) repeat until the access token expires.  If the client knows the access token expired, it skips to step (7); otherwise, it makes another protected resource request.
  
(6)  Since the access token is invalid, the resource server returns an invalid token error.
  
(7)  The client requests a new access token by authenticating with the authorization server and presenting the refresh token.
  
(8)  The authorization server authenticates the client and validates the refresh token, and if valid, issues a new access token. (In my case, No new refresh token)
