import re
from datetime import date, time


class MessageData(object):
    """ A class to represent a message in a WhatsApp conversation """
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
    """ Builds a list of MessageData objects from a WhatsApp chat log
    :param file_path: absolute filepath containing a WhatsApp chat log
    :type file_path: str
    :return: list of MessageData objects
    :rtype: list
    """
    message_block = ""
    with open(file_path, "r", encoding="utf8") as file:
        data = file.readlines()
        for line in data:
            if not line.strip():
                # skip empty lines
                continue
            message_block += line.strip()
    messages = re.findall(r"(\d\d/\d\d/\d\d\d\d.*?)\d\d/\d\d/\d\d\d\d", message_block)
    return [MessageData(message) for message in messages]


def get_post_counts(message_datas):
    """ Get a dictionary mapping the name of each poster to the number of times they posted """
    return get_property_to_count("author", message_datas, "author")


def get_system_messages(message_datas):
    """ Get messages that have no author, meaning they're some kind of system message """
    system_messages = []
    for message in message_datas:
        if message.author:
            continue
        system_messages.append(message.message)
    return system_messages


def get_unique_group_names(system_messages):
    """ Get the unique names that the group has had
    :param system_messages: a list of MessageData objects that do not have a value in the 'author' property
    :type system_messages: list(MessageData)
    :return: set of names the group has had
    :rtype: set
    """
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
    """ Get a dictionary mapping date to number of messages sent on that date """
    return get_property_to_count("date", message_datas, "author")


def get_average_busiest_hour(message_datas):
    """ Get a dictionary mapping each 24 hour period to the number of messages sent in that period across the
    entire message set
    :param message_datas: a list of MessageData objects
    :type message_datas: list
    :return: dictionary mapping each 24-hour period to the number of posts in that period
    :rtype: dict
    """
    hour_to_count = {}
    for message in message_datas:
        if message.time.hour not in hour_to_count:
            hour_to_count[message.time.hour] = 1
        hour_to_count[message.time.hour] += 1
    return {key: value for key, value in reversed(sorted(hour_to_count.items(), key=lambda item: item[1]))}


def get_property_to_count(prop, iterable, condition_property=None):
    """Get the number of times a property appears in an iterable
    :param prop: the property to count
    :type prop: str
    :param iterable: the objects containing the property to count
    :type iterable: iterable
    :param condition_property: if provided, objects that do not have this property will be skipped (default None)
    :type condition_property: str
    :return: dictionary mapping the number of times the specified property appears in the iterated objects
    :rtype: dict
    """
    property_to_count = {}
    for item in iterable:
        if condition_property:
            if not getattr(item, condition_property):
                continue
        if getattr(item, prop) not in property_to_count:
            property_to_count[getattr(item, prop)] = 1
        property_to_count[getattr(item, prop)] += 1
    return {key: value for key, value in reversed(sorted(property_to_count.items(), key=lambda item: item[1]))}
