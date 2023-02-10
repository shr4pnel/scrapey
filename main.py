import re


class MessageData(object):

    def __init__(self, raw_string):
        self._raw_string = raw_string
        # https://regex101.com/r/92uTge/1
        self._regex_object = None
        self._date = ""
        self._time = ""
        self._poster = ""
        self._message = ""

    @property
    def regex_object(self):
        if not self._regex_object:
            self._regex_object = re.match(r"(?P<date>\d\d/\d\d/\d\d\d\d), (?P<time>\d\d:\d\d) - "
                                          r"(?P<poster>[\w]*:|[\w]* [\w']*:)?(?P<message>.*?)$",
                                          self._raw_string)
        return self._regex_object

    @regex_object.setter
    def regex_object(self, value):
        self._regex_object = value

    @property
    def date(self):
        if not self._date:
            self._date = self.regex_object.group("date")
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def time(self):
        if not self._time:
            self._time = self.regex_object.group("time")
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def poster(self):
        if not self._poster:
            self._poster = self.regex_object.group("poster")
        return self._poster

    @poster.setter
    def poster(self, value):
        self._poster = value

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
            # current_message = MessageData(line)
            # messages.append(current_message)
    messages = re.findall(r"(\d\d/\d\d/\d\d\d\d.*?)\d\d/\d\d/\d\d\d\d", message_block)
    return [MessageData(message) for message in messages]


def get_post_counts(message_datas):
    """ Get a dictionary mapping the name of each poster to the number of times they posted """
    poster_to_count = {}
    for message in message_datas:
        if message.poster not in poster_to_count.keys():
            poster_to_count[message.poster] = 1
        else:
            poster_to_count[message.poster] += 1
    # sort the dict by the post count
    return {key: value for key, value in sorted(poster_to_count.items(), key=lambda item: item[1])}


def get_system_messages(message_datas):
    """ Get messages that have no poster, meaning they're some kind of system message """
    system_messages = []
    for message in message_datas:
        if message.poster:
            continue
        system_messages.append(message.message)
    return system_messages


def get_unique_group_names(system_messages):
    """ Get the unique names that the group has had """
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


def main(file_path):
    messages = get_messagedata(file_path)
    sys_msgs = get_system_messages(messages)
    unique_names = get_unique_group_names(get_system_messages(messages))
    print("done")


if __name__ == '__main__':
    main(r"C:\Users\Benji.Aird\Downloads\WhatsApp Chat with Lumpsuckers & Slimeheads.txt")
