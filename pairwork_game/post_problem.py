import requests
import json
def main():
    aheaders = {'Content-Type': 'application/json'}
    url= "http://47.102.118.1:8089/api/challenge/create"
    try:
        values = {
            "teamid": 37,
            "data": {
                "letter": "H",
                "exclude": 9,
                "challenge": [
                    [5, 4, 3],
                    [7, 2, 1],
                    [8, 6, 0]
                ],
                "step": 3,
                "swap": [1, 2]
            },
            "token": "6098546f-f027-4a28-bacf-fda5805d21cf"
        }

        request = requests.post(url, headers=aheaders, data=json.dumps(values))
        #        html = urllib.request.urlopen(request).read().decode('utf-8')
        print(json.loads(request.text))
    except Exception as err:
        print(err)

main()