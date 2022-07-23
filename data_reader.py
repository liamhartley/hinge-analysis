import json
import time
from datetime import datetime, timedelta


class HingeData:

    def __init__(self, json_path: str, data_type: str):
        '''
        Base class object to analyse your Hinge data
        :param json_path: the path to your file to analyse
        :param data_type: all Hinge filetypes that are available for analysis
        '''
        data_types = ['matches']
        assert data_type in data_types

        self.data_type = data_type
        self.json_path = json_path
        self.datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.datetime_format_alternative = "%Y-%m-%dT%H:%M:%S"

        with open(self.json_path, "r") as read_file:
            self.json_dict = json.load(read_file)

    def get_message_time(self, message, field):
        '''
        Used to handle different datetime formats in Hinge data
        :param message:
        :param field:
        :return:
        '''
        try:
            message_time = datetime.fromtimestamp(
                time.mktime(time.strptime(message[field], self.datetime_format)))
        except ValueError:
            message_time = datetime.fromtimestamp(
                time.mktime(time.strptime(message[field], self.datetime_format_alternative)))
        return message_time

    def average_response_time(self):
        '''
        Average time that you take to respond to messages
        '''
        average_response_times = []
        for interaction in self.json_dict:
            total_response_time = timedelta(0)
            if 'chats' in interaction:
                if len(interaction['chats']) > 1:
                    previous_message = interaction['chats'][0]
                    for message in interaction['chats'][1:]:
                        first_message_time = self.get_message_time(previous_message, 'timestamp')
                        second_message_time = self.get_message_time(message, 'timestamp')
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

    def like_statistics(self):
        '''
        Prints statistics about matches, likes sent, like conversion and unmatching
        :return:
        '''
        like_no_match = 0
        matches = 0
        declined = 0
        unmatches = 0
        for interaction in self.json_dict:
            if 'like' in interaction:
                if 'match' in interaction:
                    matches += 1
                else:
                    like_no_match += 1
            if 'like' in interaction:
                if 'block' in interaction:
                    unmatches += 1
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

    def my_average_match_time(self):
        '''
        The average time that you accept matches
        '''
        match_times = []
        for interaction in self.json_dict:
            if 'match' in interaction:
                match_time = self.get_message_time(interaction['match'][0], 'timestamp')
                match_times.append(match_time)
        sum_of_time = sum(map(datetime.timestamp, match_times))
        unix_average_time = datetime.fromtimestamp(sum_of_time/len(match_times))
        average_time = datetime.strftime(unix_average_time, "%H:%M:%S")

        print(f"average match time for likes received: {average_time}")

    def their_average_match_time(self):
        '''
        The average time that your likes are accepted
        '''
        match_times = []
        for interaction in self.json_dict:
            if 'match' in interaction and 'like' in interaction:
                match_time = self.get_message_time(interaction['match'][0], 'timestamp')
                match_times.append(match_time)
        sum_of_time = sum(map(datetime.timestamp, match_times))
        unix_average_time = datetime.fromtimestamp(sum_of_time/len(match_times))
        average_time = datetime.strftime(unix_average_time, "%H:%M:%S")

        print(f"average match time for likes accepted: {average_time}")

    def average_match_day_theirs(self):
        match_days = []
        for interaction in self.json_dict:
            if 'match' in interaction and 'like' in interaction:
                match_time = self.get_message_time(interaction['match'][0], 'timestamp')
                match_day = match_time.isoweekday()
                match_days.append(match_day)

        most_matches = 0
        most_matched_day = 0
        for match_day in [1, 2, 3, 4, 5, 6, 7]:
            matches_on_day = match_days.count(match_day)
            if matches_on_day > most_matches:
                most_matches = matches_on_day
                most_matched_day = match_day

        print(f"most common day for your likes to be accepted: {most_matched_day} ({most_matches})")

    def average_match_day_yours(self):
        match_days = []
        for interaction in self.json_dict:
            if 'match' in interaction:
                match_time = self.get_message_time(interaction['match'][0], 'timestamp')
                match_day = match_time.isoweekday()
                match_days.append(match_day)

        most_matches = 0
        most_matched_day = 0
        for match_day in [1, 2, 3, 4, 5, 6, 7]:
            matches_on_day = match_days.count(match_day)
            if matches_on_day > most_matches:
                most_matches = matches_on_day
                most_matched_day = match_day

        print(f"most common day for you to accept likes: {most_matched_day} ({most_matches})")
