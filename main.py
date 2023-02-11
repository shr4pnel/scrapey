import re
from datetime import date, time


class MessageData(object):

    def __init__(self, raw_string):
        self._raw_string = raw_string
        # https://regex101.com/r/92uTge/1
        self._regex_object = None
        self._date = ""
        self._time = ""
        self._author = ""
        self._message = ""

    @property
    def regex_object(self):
        if not self._regex_object:
            self._regex_object = re.match(r"(?P<date>\d\d/\d\d/\d\d\d\d), (?P<time>\d\d:\d\d) - "
                                          r"(?P<author>[\w]*:|[\w]* [\w']*:)?(?P<message>.*?)$",
                                          self._raw_string)
        return self._regex_object

    @regex_object.setter
    def regex_object(self, value):
        self._regex_object = value

    @property
    def date(self):
        if not self._date:
            day, month, year = self.regex_object.group("date").split("/")
            self._date = date(int(year), int(month), int(day))
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, date):
            print(f"Date property must be a valid date object, {value} is {type(value)}")
            return
        self._date = value

    @property
    def time(self):
        if not self._time:
            hour, minute = self.regex_object.group("time").split(":")
            self._time = time(int(hour), int(minute))
        return self._time

    @time.setter
    def time(self, value):
        if not isinstance(value, time):
            print(f"Time property must be a valid time object, {value} is {type(value)}")
            return
        self._time = value

    @property
    def author(self):
        if not self._author:
            self._author = self.regex_object.group("author")
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def message(self):
        if not self._message:
            self._message = self.regex_object.group("message")
        return self._message

    @message.setter
    def message(self, value):
        self._message = value


def get_messagedata(file_path):
    message_block = ""
    with open(file_path, "r", encoding="utf8") as file:
        data = file.readlines()
        for line in data:
            if not line.strip():
                continue
            message_block += line.strip()
    messages = re.findall(r"(\d\d/\d\d/\d\d\d\d.*?)\d\d/\d\d/\d\d\d\d", message_block)
    return [MessageData(message) for message in messages]


def get_post_counts(message_datas):
    """ Get a dictionary mapping the name of each poster to the number of times they posted """
    author_to_count = {}
    for message in message_datas:
        if not message.author:
            # skip system messages
            continue
        if message.author not in author_to_count.keys():
            author_to_count[message.author] = 1
        author_to_count[message.author] += 1
    # sort the dict by the post count
    return {key: value for key, value in reversed(sorted(author_to_count.items(), key=lambda item: item[1]))}


def get_system_messages(message_datas):
    """ Get messages that have no author, meaning they're some kind of system message """
    system_messages = []
    for message in message_datas:
        if message.author:
            continue
        system_messages.append(message.message)
    return system_messages


def get_unique_group_names(system_messages):
    """ Get the unique names that the group has had """
    # TODO: sort these chronologically
    group_names = set()
    for message in system_messages:
        # TODO make this less shit, don't use string contains checks, do some regex or something
        if "\"" not in message:
            continue
        if "from" not in message:
            continue
        name_from, name_to = message.split("\"")[1], message.split("\"")[3]
        [group_names.add(name) for name in [name_from, name_to]]
    return group_names


def get_messages_per_day(message_datas):
    date_to_count = {}
    for message in message_datas:
        if not message.author:
            # skip system messages
            continue
        if message.date not in date_to_count.keys():
            date_to_count[message.date] = 1
        date_to_count[message.date] += 1
    # sort the dict by the post count
    return {key: value for key, value in reversed(sorted(date_to_count.items(), key=lambda item: item[1]))}


def get_average_busiest_hour(message_datas):
    hour_to_count = {}
    for message in message_datas:
        if not message.time:
            continue
        if message.time.hour not in hour_to_count:
            hour_to_count[message.time.hour] = 1
        hour_to_count[message.time.hour] += 1
    return {key: value for key, value in reversed(sorted(hour_to_count.items(), key=lambda item: item[1]))}


def main(file_path):
    messages = get_messagedata(file_path)
    sys_msgs = get_system_messages(messages)
    unique_names = get_unique_group_names(get_system_messages(messages))
    messages_per_day = get_messages_per_day(messages)
    post_counts = get_post_counts(messages)
    hour_counts = get_average_busiest_hour(messages)
    print("done")


if __name__ == '__main__':
    main(r"C:\Users\Benji.Aird\Downloads\WhatsApp Chat with Lumpsuckers & Slimeheads.txt")
