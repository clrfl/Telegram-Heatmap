#
# This code can be used to create a dictionary of { from-id : username }, when compensating for deleted accounts.
# However, in most cases this won't be necessary.
#
# When creating this dictionary files, all known names are filled in automatically from your database file.
# You can fill in additional usernames manually (if you can restore them from context) by
# replacing the "none"s in the dictionary.json file.
# You then need to set the parameter read_file( ..., use_dictionary=True)

import json


def create_userdict():
    userdict = {}
    with open('../demodata.json', encoding="utf8") as json_file:
        data = json.load(json_file)
        for p in data['messages']:
            if p['type'] == 'message':
                userdict[p['from_id']] = p['from']

    with open('../dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(userdict, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    create_userdict()

