import json
from data_reader import HingeData

if __name__ == '__main__':

    data_path = '/Users/liamhartley/PycharmProjects/hinge-analysis/export/matches.json'

    HingeDataObject = HingeData(json_path=data_path, data_type='matches')
    HingeDataObject.average_response_time()
    HingeDataObject.like_conversion_rate()
    HingeDataObject.my_average_match_time()
    HingeDataObject.their_average_match_time()

# TODO
# Transform the matches.json to amend all dates to one format
# add export to .gitignore
# push
# README
