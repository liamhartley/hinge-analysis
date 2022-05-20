import json
import time
from datetime import datetime, timedelta


class HingeData:
    def __init__(self, json_path: str, data_type: str):

        data_types = ['matches']
        assert data_type in data_types

        self.data_type = data_type
        self.json_path = json_path
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.datetime_format_alternative = "%Y-%m-%dT%H:%M:%S"

        with open(self.json_path, "r") as read_file:
            self.json_dict = json.load(read_file)

    def average_response_time(self):
        average_response_times = []
        for interaction in self.json_dict:
            total_response_time = timedelta(0)
            if 'chats' in interaction:
                if len(interaction['chats']) > 1:
                    previous_message = interaction['chats'][0]
                    for message in interaction['chats'][1:]:
                        try:
                            first_message_time = datetime.fromtimestamp(
                                time.mktime(time.strptime(previous_message['timestamp'], self.datetime_format)))
                        except ValueError:
                            first_message_time = datetime.fromtimestamp(
                                time.mktime(time.strptime(previous_message['timestamp'], self.datetime_format_alternative)))
                        try:
                            second_message_time = datetime.fromtimestamp(
                                time.mktime(time.strptime(message['timestamp'], self.datetime_format)))
                        except ValueError:
                            second_message_time = datetime.fromtimestamp(
                                time.mktime(time.strptime(message['timestamp'], self.datetime_format_alternative)))
                        response_time = second_message_time - first_message_time
                        total_response_time = response_time + total_response_time
                        previous_message = message
                    average_response_times.append(total_response_time/(len(interaction['chats']) - 1))

        total_response_time = timedelta(0)
        for average_response_time in average_response_times:
            total_response_time = total_response_time + average_response_time
        average_response_time = total_response_time/len(average_response_times)
        print(f"average response time: {average_response_time}")
        print(f"slowest response time: {max(average_response_times)}")
        print(f"fastest response time: {min(average_response_times)}")

    def like_conversion_rate(self):
        like_no_match = 0
        matches = 0
        for interaction in self.json_dict:
            if 'like' in interaction:
                if 'match' in interaction:
                    matches += 1
                else:
                    like_no_match += 1

        unmatches = 0
        for interaction in self.json_dict:
            if 'like' in interaction:
                if 'block' in interaction:
                    unmatches += 1

        declined = 0
        for interaction in self.json_dict:
            if 'block' in interaction:
                if 'match' not in interaction:
                    declined += 1

        like_conversion_rate = matches/(like_no_match+matches)
        print(f"total matches: {matches}")
        print(f"total likes sent without matches: {like_no_match}")
        print(f"total likes sent: {matches+like_no_match}")
        print(f"like conversion rate: {round(like_conversion_rate, 2)}%")
        print(f"total number of people I have unmatched: {unmatches}")
        print(f"total number of people I have declined: {declined}")

    def get_match_time(self, interaction):
        try:
            match_time = datetime.fromtimestamp(
                time.mktime(time.strptime(interaction['match'][0]['timestamp'], self.datetime_format)))
        except ValueError:
            match_time = datetime.fromtimestamp(
                time.mktime(time.strptime(interaction['match'][0]['timestamp'], self.datetime_format_alternative)))
        return match_time

    def my_average_match_time(self):
        match_times = []
        for interaction in self.json_dict:
            if 'match' in interaction:
                match_time = self.get_match_time(interaction)
                match_times.append(match_time)
        sum_of_time = sum(map(datetime.timestamp, match_times))
        unix_average_time = datetime.fromtimestamp(sum_of_time/len(match_times))
        average_time = datetime.strftime(unix_average_time, "%H:%M:%S")

        print(f"average match time for likes received: {average_time}")

    def their_average_match_time(self):
        match_times = []
        for interaction in self.json_dict:
            if 'match' in interaction and 'like' in interaction:
                match_time = self.get_match_time(interaction)
                match_times.append(match_time)
        sum_of_time = sum(map(datetime.timestamp, match_times))
        unix_average_time = datetime.fromtimestamp(sum_of_time/len(match_times))
        average_time = datetime.strftime(unix_average_time, "%H:%M:%S")

        print(f"average match time for likes sent: {average_time}")






