from imessage_tools import *
from nltk.stem.snowball import SnowballStemmer
import matplotlib.pyplot as plt
import re

# Path to the chat.db file
chat_db = "chat.db"

# Phone number or label for "you"
self_number = "Me"

# Number of messages to return
n = None

# Path to the stoplist file
stop_list = "SmartStoplist.txt"

def print_date(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")

def display(messages):
    data = messages[:20]
    word_plot = []
    values_plot = []
    for word in data:
        word_plot.append(word[0])
        values_plot.append(word[1])

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(word_plot, values_plot, color ='maroon', 
            width = 0.4)

    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.title(":D")
    plt.show()

def word_frequency(messages, from_me=None):
    tokenized_count = {}

    # snow_stemmer = SnowballStemmer(language='english')

    # Load in stop words
    stop_words = [""]
    with open(stop_list) as f:
        for line in f:
            stop_words.append(line.strip())


    # Itterate thru every message
    for message in messages:
        if from_me != None:
            if message['is_from_me'] != from_me: 
                continue

        # Itterate thru every word in each message
        for word in message['body'].split():
            word = word.lower() # Make lowercase
            word = re.sub(r'[^\w\']+', '', word) # Remove all non a-Z charachters, non numbers but keep '

            # Skip if in stop words
            if word in stop_words:
                continue

            # word = snow_stemmer.stem(word)

            # Add to list
            if word.lower() not in tokenized_count:
                tokenized_count[word] = 1
            else:
                tokenized_count[word] = tokenized_count[word]+1
        
    # Return an array of tuples sorted by the word count in reverse order
    return sorted(tokenized_count.items(), key=lambda x: x[1], reverse=True)

def emoji_frequency(messages, from_me=None):
    exclude_list = ["￼", "�", "♂", "♀", "🏻", "🏼", "🏽", "🏾", "🏾"]

    emoji_freq = {}
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
        u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
        u"\U0001F700-\U0001F77F"  # Alchemical Symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbat Symbols
        u"\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE)


    for message in messages:
        matches = emoji_pattern.findall(message['body'])

        if from_me!=None:
            if message['is_from_me'] != from_me:
                continue

        # If there's no matches then skip the message
        if len(matches) == 0:
            continue

        flatenned_matches = ""
        for i in matches:
            flatenned_matches += i

        # Itterate thru every emoji in each message
        for emoji in flatenned_matches:
            if emoji in exclude_list:
                continue

            # Add to list
            if emoji not in emoji_freq:
                emoji_freq[emoji] = 1
            else:
                emoji_freq[emoji] = emoji_freq[emoji]+1
    
    # Return an array of tuples sorted by the word count in reverse order
    return sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)

def save_to_file(messages, filename, count=None):
    file = open(filename, "+w")

    if count == None:
        count = len(messages)

    for i in range(count):
        file.write( f"{messages[i][0]}, {messages[i][1]}\n" )

if __name__ == "__main__":
    messages = read_messages(chat_db, n=n, self_number=self_number, human_readable_date=True, handle_identifyer=89)
    
    # adri_word_count = word_frequency(messages, from_me=False)
    # save_to_file(adri_word_count, "adri_messages.csv")

    # mateo_word_count = word_frequency(messages, from_me=True)
    # save_to_file(mateo_word_count, "mateo_messages.csv")

    # combined_word_count = word_frequency(messages)
    # save_to_file(combined_word_count, "combined_messages.csv")

    adri_word_count = emoji_frequency(messages, from_me=False)
    save_to_file(adri_word_count, "adri_messages.csv")

    mateo_word_count = emoji_frequency(messages, from_me=True)
    save_to_file(mateo_word_count, "mateo_messages.csv")

    combined_word_count = emoji_frequency(messages)
    save_to_file(combined_word_count, "combined_messages.csv")