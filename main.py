import json
from data_reader import HingeData

if __name__ == '__main__':

    data_path = '/Users/liamhartley/PycharmProjects/hinge-analysis/exports/export_jd/matches.json'

    HingeDataObject = HingeData(json_path=data_path, data_type='matches')
    HingeDataObject.average_response_time()
    HingeDataObject.like_statistics()
    HingeDataObject.my_average_match_time()
    HingeDataObject.their_average_match_time()
    HingeDataObject.average_match_day_yours()
    HingeDataObject.average_match_day_theirs()

# TODO
# Transform the matches.json to amend all dates to one format
# add export to .gitignore
# add logging
# README
# SCALE this solution for large amount of files and write to a new .csv file
