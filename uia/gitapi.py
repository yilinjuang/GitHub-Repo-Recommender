import pickle
import sys

import requests
from requests.compat import urljoin


# Check arguments.
if len(sys.argv) < 3:
    print("Error: missing arguments.")
    print("Usage: gitapi.py <input-id-file> <output-starred-data>")
    sys.exit(1)

BASE_URL = "https://api.github.com/"
TOKEN = "22b359d8e8be7be5435f6f8b5e79e01ae22fcad5"
# TOKEN = "9f2e100a69c350c2208bb2cde5a48e62cd15384c"

HDR = {"Authorization": "token {}".format(TOKEN)}
# HDR = {}

class RequestTimeoutError(Exception):
    def __init__(self, url):
        super().__init__()
        self.url = url

class StatusCodeError(Exception):
    def __init__(self, url, code):
        super().__init__()
        self.url = url
        self.code = code

def req(url, hdr):
    try:
        res = requests.get(urljoin(BASE_URL, url), headers=hdr, timeout=10.0)
    except requests.Timeout:
        raise RequestTimeoutError(url)
    except requests.ConnectionError:
        raise RequestTimeoutError(url)
    if res.status_code != 200:
        raise StatusCodeError(url, res.status_code)
    return res

def get_rate_limit():
    try:
        res = req("/rate_limit", HDR)
    except (RequestTimeoutError, StatusCodeError):
        return
    rate = res.json()["rate"]
    limit, remaining = rate["limit"], rate["remaining"]
    print("Rate limit: {}, remaining: {}".format(limit, remaining))
    return limit, remaining

def get_user_starred(user):
    try:
        # User id.
        user = int(user)
        url = "/user/{}/starred".format(user)
    except ValueError:
        # User name.
        url = "/users/{}/starred".format(user)
    url += "?per_page=100"
    hdr = HDR.copy()
    # Alternative response with star creation timestamps
    hdr["Accept"] = "application/vnd.github.v3.star+json"

    starred = []
    while True:
        sys.stdout.flush()
        try:
            res = req(url, hdr)
        except RequestTimeoutError:
            print("*", end="")
            continue
        except StatusCodeError as err:
            print("Error: status code {} from request {}.".format(err.code,
                                                                  err.url))
            return None
        if not "Link" in res.headers:
            return starred
        print(".", end="")
        starred += res.json()
        if "next" in res.headers["Link"]:
            for link in res.headers["Link"].split(", "):
                if "next" in link:
                    url = link.split(";")[0][1:-1]
                    break
        else:
            break
    print("\n{} starred.".format(len(starred)))
    return starred

# Usage
# limit, remaining = get_rate_limit()
# user_starred = get_user_starred("frankyjuang")
# user_starred = get_user_starred(6175880)

try:
    with open(sys.argv[2], "rb") as f:
        all_starred = pickle.load(f)
except FileNotFoundError:
    print("Debug: {} not found, but created.".format(sys.argv[2]))
    all_starred = {}

try:
    with open(sys.argv[1], "r") as f:
        for uid in f:
            if uid[0] == "#":
                continue

            uid = uid.strip()
            if uid in all_starred:
                print("Debug: {} already fetched.".format(uid))
                continue

            _ = get_rate_limit()
            print("Fetching {}...".format(uid))
            user_starred = get_user_starred(uid)
            if user_starred is None:
                print("Warning: exit due to rate limit.")
                break
            elif len(user_starred) < 3000:
                print("Number of stars < 3000, UID: {}".format(uid))
                continue
            all_starred[uid] = user_starred
except KeyboardInterrupt:
    print("\nDebug: interrupted.")
finally:
    with open(sys.argv[2], "wb") as f:
        pickle.dump(all_starred, f)
