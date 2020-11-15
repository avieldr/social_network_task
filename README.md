# social_network_task

This project is a basic social network RESTfull api implementation with Django.
It consists of two parts:
1. Social network restApi
2. An automated bot that demonstrates the API use.

-----------------
1. Social Network
-----------------

Models:
1. CustomUser - overrides the default django User model in order to use the user's email as model's id.
2. Post - implements a post in a social network.
3. PostReaction - implements a 'reaction' (= 'like', 'love', 'angry' etc...) of a user instance to a post instance.
All models implemented with django 'REST_FRAMEWORK's serializers and viewsets to allow creation, modification and deletion of all instances.

All operations except for signup and signin requires JWT authentication.

----------------
2. Automated bot
----------------

Demonstrates the API use as required.
Run instructions:
* Configure "automated_bot/config.json" (if not configured, bot will use default configuration)
* Run Bot.py

-----------------
3. External Api's
-----------------
Using Hunter's and clearbit's api's as required.
clearbit api use is currently disabled (in comment) because they want money and i dont want to pay them... you can use your clearbit key and uncomment the api call.
