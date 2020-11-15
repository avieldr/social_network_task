DEFAULT_NUMBER_OF_USERS = 5
DEFAULT_NUMBER_OF_POSTS_PER_USER = 5
DEFAULT_NUMBER_OF_LIKES_PER_USER = 5

MAX_SIGNUP_FAILURES = 20
MAX_SIGNIN_RETRIES = 5

DEFAULT_API_ROOT = "http://127.0.0.1:8000"

NUM_USERS = "number_of_users"
MAX_POSTS_PU = "max_posts_per_user"
MAX_LIKES_PU = "max_likes_per_user"
API_ROOT = "api_root_address"

SIGNUP_FAILED = "ABORTED: SIGNUP FAILED..."
SIGNIN_FAILED = "ABORTED: SIGNIN FAILED..."
REFRESH_FAILED = "ABORTED: REFRESH TOKEN FAILED..."
CREATE_POST_FAILED = "ABORTED: CREATE POST FAILED..."
REACT_FAILED = "ABORTED: REACT FAILED..."
INVALID_INPUT_MESSAGE = "(Invalid input arguments)"
CANNOT_SIGNIN_MESSAGE = "cannot signin user:"
POST_CREATED = "POST CREATED:"
REACTION_CREATED = "REACTION CREATED:"

FORGE_USERS_SUCCESS_MESSAGE = "---forge_users_phase ended successfully---"
FORGE_POSTS_SUCCESS_MESSAGE = "---forge_posts_phase ended successfully---"
FORGE_REACTIONS_SUCCESS_MESSAGE = "---forge_reactions_phase ended successfully---"

SIGNUP_SUCCESS = "SUCCESSFULLY SIGNED UP USER:"

SIGNIN_URI = "/api/token/"
SIGNUP_URI = "/users/"
REFRESH_URI = "/api/token/refresh/"
POST_CREATE_URI = "/posts/"
REACTIONS_URI = "/reactions/"

POSTS = "posts"
ID = 'id'
EMAIL = "email"
PASSWORD = "password"
ACCESS = "access"
REFRESH = "refresh"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
TITLE = "title"
TEXT = "text"
VALUE = "value"
POST = "post"
AUTHORIZATION = "Authorization"
BEARER = "Bearer "
REACTIONS = "reactions"
REACTED_TO = "reacted_to"
POSTS_WITH_NO_REACTIONS = "posts_with_no_reactions"

STATUS_CODE = "status code:"
UNAUTHORIZED = 401
CREATED = 201
SERVER_ERROR = 500

LIKE = 1

SUCCESS = 1
FAILED = 0

SESSION_SUCCESS = "SESSION ENDS SUCCESSFULLY!!!"
SESSION_FAILED = "SESSION FAILED"


WEBMAILS = ["@walla.com", "@gmail.com", "@hotmail.com", "@walla.co.il"]