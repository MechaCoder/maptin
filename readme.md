# Maptin
I love role play games, I recently started playing and dming games of Dungeons and dragons in this I found a lot of existing site unsuitable, because it takes a lot setup, they are not easy to use or they just didn't work.

Maptin is inspired by the "Marauder Army Commanders Model Kit" the idea is to give you a set of maps and tokens that you can use to build your adventures.

When building this app I implemented the following rules;

+ Simplistically is everything:
  + The dm wants something that easy to use and works
  + Players want to play not navigate complex interfaces

+ Collaborative storytelling is cental to the game.
  + People working together is not something that can offered by, by video games, and this should be supported

+ The rifle goes round the man
  + the tools should fit around the DM and players, and should not shape the way dm works.

## getting maptin To run

### LAN and Local development

on a LAN network to run this you will need `Python3.7` and a working installation of `pipenv`, you can get this the code base from git by cloning the repo;

1. change directory to a where you have cloned the project.
2. run `pipenv install`
3. then run  `pipenv run python start_script.py` this ensures that all requirements are met
4. then run `pipenv run start`
5. click [here](http://127.0.0.1)


### on a server
I only have notes thus far, so please take these with a grain of salt.

By default Maptin is set up to work a json file, this dose not work on the server due to the sercurity consurns. when you run `pipenv run python start_script.py` a file is created in the root of the project `credentials.json` this is where the required paths and credentials required to run the project, `credentials.json` is in the json format.

in this file you will need to two key, value pairs. `mysqlUname` and `mysqlPword` this will allow the software to use mysql.

## Terms Used in this project
|Term|Notes|
|---|---|
|`Maptin`| `maptin` is the project name|
|`A DM`, `A logged-in user`,| this is a uniqne user that has a ceds and is logged in|
|`A Player`, `A user`| this is a normal player that is not loggedin|
|`A Map`| A map is a essentaly a method made up of a title, background, and soundtrack. |
