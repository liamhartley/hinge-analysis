import json
import sys


if __name__ == '__main__':
    # try:
    #     assert sys.argv[1] is not None
    #     filepath = sys.argv[1]
    # except IndexError:
    #     print("Please pass in a valid filepath e.g. '/Users/liamhartley/export/matches.json'")
    #     sys.exit()

    filepath = "/Users/liam.hartley/PycharmProjects/hinge-analysis/export/matches.json"

    with open(filepath, "r+") as file:
        json_dict = json.load(file)

        redacted_counter = 0
        for match in json_dict:
            if 'chats' in match:
                for chat in match['chats']:
                    if chat['body'] != 'redacted':
                        print(f"redacting: {chat['body']}")
                        chat['body'] = 'redacted'
                    redacted_counter += 1
            elif 'like' in match:
                if 'comment' in match['like'][0]:
                    print(f"redacting: {match['like'][0]['comment']}")
                    match['like'][0] = 'redacted'
                    redacted_counter += 1

        print(f"{redacted_counter} messages redacted")

        file.seek(0)
        json.dump(json_dict, file)
        file.truncate()
