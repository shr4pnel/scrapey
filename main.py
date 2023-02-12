import messages
import visualisation


def main(file_path):
    messagedata = messages.get_messagedata(file_path)
    sys_msgs = messages.get_system_messages(messagedata)
    unique_names = messages.get_unique_group_names(messages.get_system_messages(messagedata))
    messages_per_day = messages.get_messages_per_day(messagedata)
    post_counts = messages.get_post_counts(messagedata)
    hour_counts = messages.get_average_busiest_hour(messagedata)
    # visualisation
    post_count_plot = visualisation.get_bar_graph(post_counts.keys(), post_counts.values(), "Post Counts")
    post_count_plot.show()
    print("done")


if __name__ == '__main__':
    main(r"C:\Users\Benji.Aird\Downloads\WhatsApp Chat with Lumpsuckers & Slimeheads.txt")