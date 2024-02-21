from imessage_tools import *
from freq_list import FreqList
import re

class iMessageAnalysis:
    def __init__(self, chat_db, handle_identifyer, n, self_number, stop_list):
        self.messages = read_messages(chat_db, n=n, self_number=self_number, human_readable_date=True, handle_identifyer=handle_identifyer)

        # Load in stop words
        stop_words = []
        with open(stop_list) as f:
            for line in f:
                stop_words.append(line.strip())

        self.exclude_list = ["￼", "�", "♂", "♀", "🏻", "🏼", "🏽", "🏾", "🏾"]

        # Compiling regex object for emoji analysis function here so that it's not recompiled everytime the function is run
        self.emoji_pattern = re.compile("["
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

    def print_messages(self, n=None):
        if n == None:
            n = len(self.messages)

        for i in range(n):
            message = self.messages[i]['body']
            date = self.messages[i]['date']

            date_str = date.strftime("%Y-%m-%d %H:%M:%S")

            print(f"{(date_str)}  {message}")

    def word_frequency(self, from_me=None):
        word_freq = {}

        # Itterate thru every message
        for message in self.messages:
            if from_me != None:
                if message['is_from_me'] != from_me: 
                    continue

            # Itterate thru every word in each message
            for word in message['body'].split():
                word = word.lower() # Make lowercase
                word = re.sub(r'[^\w\']+', '', word) # Remove all non a-Z charachters, non numbers but keep (')

                # Skip if in stop words
                if word in self.stop_words:
                    continue

                # Add to list
                if word.lower() not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] = word_freq[word]+1
            
        # Return an array of tuples sorted by the word count in reverse order
        word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        word_freq = FreqList(word_freq)

        return word_freq

    def emoji_frequency(self, from_me=None):
        emoji_freq = {}

        for message in self.messages:
            matches = self.emoji_pattern.findall(message['body'])

            if from_me != None:
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
                if emoji in self.exclude_list:
                    continue

                # Add to list
                if emoji not in emoji_freq:
                    emoji_freq[emoji] = 1
                else:
                    emoji_freq[emoji] = emoji_freq[emoji]+1
        
        # Return an array of tuples sorted by the word count in reverse order
        emoji_freq = sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)
        emoji_freq = FreqList(emoji_freq)

        return emoji_freq