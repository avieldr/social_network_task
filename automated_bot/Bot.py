import os
import json
import requests
import random
from utils.constants import *

from faker import Faker
fake = Faker()

class Bot:

    def __init__(self):
        conf = self.get_config()
        self.number_of_users = conf[NUM_USERS] if NUM_USERS in conf else DEFAULT_NUMBER_OF_USERS
        self.max_posts_per_user = conf[MAX_POSTS_PU] if MAX_POSTS_PU in conf else DEFAULT_NUMBER_OF_POSTS_PER_USER
        self.max_likes_per_user = conf[MAX_LIKES_PU] if MAX_LIKES_PU in conf else DEFAULT_NUMBER_OF_LIKES_PER_USER
        self.api_root = conf[API_ROOT] if API_ROOT in conf else DEFAULT_API_ROOT
        self.session_signin_failures = 0
        self.session_create_post_failures = 0
        self.users = []

    @staticmethod
    def get_config(config_file="./config.json"):
        config = {}
        if os.path.isfile(config_file):
            f = open(config_file, "r")
            config = json.load(f)
            f.close()
        return config

    @staticmethod
    def generate_user_details():

        def gen_add_numbers_suffix(first_name, last_name, provider):
            return first_name + last_name + str(random.randint(0, 1000)) + provider

        def gen_dot(first_name, last_name, provider):
            r = int(random.randint(0, len(last_name)))
            return first_name + last_name[0: r] + provider

        def gen_dup(first_name, last_name, provider):
            r = int(random.randint(0, len(first_name)))
            return first_name + first_name[0: r] + str(random.randint(0, 100)) + provider

        def generate_mail_address(first_name, last_name):
            generator = random.choice([gen_add_numbers_suffix, gen_dot, gen_dup])
            webmail_pref = random.choice(WEBMAILS)
            return generator(first_name, last_name, webmail_pref)

        f_name = fake.first_name()
        l_name = fake.last_name()
        email = generate_mail_address(f_name.lower(), l_name.lower())
        password = fake.password()
        return f_name, l_name, email, password

    @staticmethod
    def generate_post():
        title = fake.text(random.randint(20, 80))
        body = fake.text(random.randint(100, 800))

        return title, body

    def sign_up(self, email, password, first_name, last_name):

        if not email or not password or not first_name or not last_name:
            print(SIGNUP_FAILED, INVALID_INPUT_MESSAGE)
            return INVALID_INPUT_MESSAGE, FAILED

        url = self.api_root + SIGNUP_URI
        data = {EMAIL: email, PASSWORD: password, FIRST_NAME: first_name, LAST_NAME: last_name}
        try:
            res = requests.post(url, data=data)
        except requests.exceptions.RequestException as e:
            print(e)
            return None, FAILED
        else:

            if res.status_code != 201:
                print(SIGNUP_FAILED, STATUS_CODE, res.status_code, res.text)
                return None, FAILED
            print(SIGNUP_SUCCESS, res.json())
            return res.json(), SUCCESS

    def sign_in(self, email, password):

        if not email or not password:
            print(SIGNIN_FAILED, INVALID_INPUT_MESSAGE)
            return INVALID_INPUT_MESSAGE, FAILED

        url = self.api_root + SIGNIN_URI
        data = {EMAIL: email, PASSWORD: password}
        try:
            res = requests.post(url, data=data)
        except requests.exceptions.RequestException as e:
            print(e)
            return None, FAILED
        else:
            if res.status_code != 200:
                print(SIGNIN_FAILED, STATUS_CODE, res.status_code, res.text)
                return None, FAILED

            json_obj = res.json()
            refresh, access = json_obj[REFRESH], json_obj[ACCESS]
            return [refresh, access], SUCCESS

    def refresh_token(self, refresh_token):
        if not refresh_token:
            print(REFRESH_FAILED, INVALID_INPUT_MESSAGE)
            return INVALID_INPUT_MESSAGE

        url = self.api_root + REFRESH_URI
        data = {REFRESH: refresh_token}

        try:
            res = requests.post(url, data=data)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        else:
            if res.status_code != 200:
                print(REFRESH_FAILED, STATUS_CODE, res.status_code, res.text)
                return None

            return res.json()[ACCESS]

    def create_post(self, access_token, title, body):
        if not access_token or not title or not body:
            print(CREATE_POST_FAILED, INVALID_INPUT_MESSAGE)
            return INVALID_INPUT_MESSAGE

        url = self.api_root + POST_CREATE_URI
        headers = {AUTHORIZATION: BEARER + access_token}
        data = {TITLE: title, TEXT: body}

        try:
            res = requests.post(url, data=data, headers=headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        else:
            if res.status_code != 201:
                print(CREATE_POST_FAILED, STATUS_CODE, res.status_code, res.text)
                return None
            print(POST_CREATED, res.json())
            return res.json()


    def react(self, access_token, value, post):
        if not access_token or not value or not post:
            print(REACT_FAILED, INVALID_INPUT_MESSAGE)
            return INVALID_INPUT_MESSAGE

        url = self.api_root + REACTIONS_URI
        headers = {AUTHORIZATION: BEARER + access_token}
        data = {VALUE: value, POST: post}

        try:
            res = requests.post(url, data=data, headers=headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        else:
            if res.status_code != 201:
                print(REACT_FAILED, STATUS_CODE, res.status_code, res.text)
                return None
            print(REACTION_CREATED, res.json())
            return res.json()


    def forge_users_phase(self):
        created_users = 0
        while created_users < self.number_of_users:
            f_name, l_name, email, password = self.generate_user_details()
            user, res = self.sign_up(email, password, f_name, l_name)
            if res:
                created_users += 1
                user[PASSWORD] = password
                user[REACTED_TO] = []
                self.users.append(user)

            else:
                self.session_signin_failures += 1
                if self.session_signin_failures >= MAX_SIGNUP_FAILURES:
                    return FAILED
        return SUCCESS

    def forge_single_user_posts_phase(self, user):
        retries = 0
        posts_arr = []
        num_of_posts_to_create = random.randint(0, self.max_posts_per_user)
        email, password = user[EMAIL], user[PASSWORD]
        user[POSTS_WITH_NO_REACTIONS] = num_of_posts_to_create

        res = 0
        while not res and retries < MAX_SIGNIN_RETRIES:
            access_tokens, res = self.sign_in(email, password)

        if not res:
            print(CANNOT_SIGNIN_MESSAGE, user)
            return FAILED

        for create_post_iter in range(num_of_posts_to_create):
            title, text = bot.generate_post()
            new_post = self.create_post(access_tokens[1], title, text)
            new_post[REACTIONS] = 0
            posts_arr.append((new_post[ID], 0))
        user[POSTS] = posts_arr

        return SUCCESS

    def get_user_candidates_indexes(self, i):
        candidates = []
        for j in range(len(self.users)):
            if i == j:
                continue

            if self.users[j][POSTS_WITH_NO_REACTIONS] > 0:
                candidates.append(j)

        return candidates


    def perform_like_abuse(self):
        for i in range(len(self.users)):
            user = self.users[i]
            while len(user[REACTED_TO]) < self.max_likes_per_user:

                candidates = self.get_user_candidates_indexes(i)

                if len(candidates) == 0:
                    return SUCCESS

                chosen_idx = random.choice(candidates)

                post_candidates = [item[0] for item in self.users[chosen_idx][POSTS] if item[0] not in user[REACTED_TO]]
                if len(post_candidates) == 0:
                    break

                chosen_post_idx = random.choice(range(len(post_candidates)))
                post = post_candidates[chosen_post_idx]

                email, password = user[EMAIL], user[PASSWORD]

                retries = 0
                res = 0
                while not res and retries < MAX_SIGNIN_RETRIES:
                    access_tokens, res = self.sign_in(email, password)

                if not res:
                    print(CANNOT_SIGNIN_MESSAGE, user)
                    return FAILED
                res = self.react(access_tokens[1], LIKE, post)

                if res:
                    user[REACTED_TO].append(post)
                    prev_likes_for_chosen_post = self.users[chosen_idx][POSTS][chosen_post_idx][1]
                    if prev_likes_for_chosen_post == 0:
                        self.users[chosen_idx][POSTS_WITH_NO_REACTIONS] -= 1
                        self.users[chosen_idx][POSTS][chosen_post_idx] = (post, prev_likes_for_chosen_post + 1)
        return SUCCESS

    @staticmethod
    def get_num_posts(elem):
        return len(elem[POSTS])

    def run_session(self):
        res = self.forge_users_phase()
        if not res:
            return FAILED

        print(FORGE_USERS_SUCCESS_MESSAGE)

        for user in self.users:
            res = self.forge_single_user_posts_phase(user)
            if not res:
                return FAILED

        print(FORGE_POSTS_SUCCESS_MESSAGE)

        self.users.sort(key=self.get_num_posts, reverse=True)

        res = self.perform_like_abuse()
        if not res:
            return FAILED

        print(FORGE_REACTIONS_SUCCESS_MESSAGE)

        return SUCCESS


bot = Bot()
r = bot.run_session()
print(SESSION_SUCCESS if r else SESSION_FAILED)
