import os
from time import sleep, time

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
password = os.getenv("GITHUB_PASSWORD")
API_URL = "https://api.github.com"


def get_response(page: int = 1) -> requests.Response:
    res = requests.get(
        f"{API_URL}/search/code",
        auth=(username, password),
        params={"q": "fastapi language:Python", "per_page": 90, "page": page},
    )
    return res


main_df = pd.DataFrame()

has_next = True
_page = 1
reset_seconds = 10
while has_next:
    sleep(1)
    resp = get_response(_page)
    data = resp.json()
    print(resp.headers)
    reset_time = int(resp.headers.get("X-RateLimit-Reset"))
    reset_seconds = abs((time() - reset_time))
    print(reset_seconds)
    print("Total: ", data.get("total_count"))
    if data.get("total_count") is None:
        print(data)
        print("reset: ", resp.headers.get("Retry-After"))
        sleep(60)
        continue
    if data.get("total_count", 0) < 30:
        print("total count less than page")
        has_next = False
        break
    if "items" not in data:
        print("items not found")
        has_next = False
        break
    print("items", len(data.get("items", [])))
    if len(data.get("items", [])) == 0:
        break
    df = pd.json_normalize(data.get("items"))
    main_df = pd.concat([main_df, df])
    print(main_df)
    _page += 1

main_df.to_excel("all.xlsx")

# df = pd.DataFrame.from_records(data.get("items"))

# df.to_excel("repo2.xlsx")

#
#
# filename = "links.txt"
# file1 = open(filename, "a")  # append mode
# has_next = True
# page = 1
# while has_next:
#     sleep(1)
#     res = get_response(page)
#     res_json = res.json()
#     if "items" in res_json:
#         for item in res_json["items"]:
#             file1.write(f"{item['repository']['html_url']}\n")
#     print(f"Page: {page}")
#     print(res.headers)
#     # print(json.dumps(res_json, indent=4, sort_keys=True))
#     # print(res.headers.get('X-RateLimit-Reset', 0))
#     if int(
#         res.headers.get("X-RateLimit-Remaining", 0)
#     ) == 0 or "422" in res.headers.get("Status", "422"):
#         has_next = False
#     page += 1
#
# file1.close()
