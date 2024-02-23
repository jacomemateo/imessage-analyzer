from imessage_tools import *
import pandas as pd
import re

class iMessageAnalysis:
    def __init__(self, chat_db, handle_identifyer, n, self_number, stop_list):
        self.messages = read_messages(chat_db, n=n, self_number=self_number, human_readable_date=True, handle_identifyer=handle_identifyer)

        # Load in stop words
        self.stop_words = []
        with open(stop_list) as f:
            for line in f:
                self.stop_words.append(line.strip())

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

    def hour_frequency(self, from_me=None):
        hour_freq = {}

        for message in self.messages:
            if from_me != None:
                if message['is_from_me'] != from_me: 
                    continue
            
            hour = message['date'].hour

            if hour not in hour_freq:
                    hour_freq[hour] = 1
            else:
                hour_freq[hour] = hour_freq[hour]+1

        hour_freq = sorted(hour_freq.items(), key=lambda x: x[0])        

        sum = 0

        for hour in hour_freq:
            sum += hour[1]

        hour_dict = {}
        hour_dict['hour'] = []
        hour_dict['percent'] = []
        
        for i in range(len(hour_freq)):
            time = hour_freq[i][0]
            percent = hour_freq[i][1]/sum

            hour_dict['hour'].append(time)
            hour_dict['percent'].append(percent)
        
        hour_freq = pd.DataFrame(hour_dict)
        hour_freq.set_index('hour', inplace=True)
        return hour_freq

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
                if word in self.stop_words or word == '':
                    continue

                # Add to list
                if word.lower() not in word_freq:
                    word_freq[word] = 1
                else:
                    word_freq[word] = word_freq[word]+1
            
        # Return an array of tuples sorted by the word count in reverse order
        word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        word_dict = {}
        word_dict['word'] = []
        word_dict['count'] = []

        for i in range(len(word_freq)):
            word_dict['word'].append(word_freq[i][0])
            word_dict['count'].append(word_freq[i][1])

        word_freq = pd.DataFrame(word_dict)
        word_freq.set_index('word', inplace=True)


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
                if emoji in self.exclude_list or emoji == '\ufe0f':
                    continue

                # Add to list
                if emoji not in emoji_freq:
                    emoji_freq[emoji] = 1
                else:
                    emoji_freq[emoji] = emoji_freq[emoji]+1
        
        # Return an array of tuples sorted by the word count in reverse order
        emoji_freq = sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)

        emoji_dict = {}
        emoji_dict['emoji'] = []
        emoji_dict['count'] = []

        for emoji in emoji_freq:
            emoji_dict['emoji'].append(emoji[0])
            emoji_dict['count'].append(emoji[1])

        emoji_freq = pd.DataFrame(emoji_dict)
        emoji_freq.set_index('emoji', inplace=True)

        return emoji_freq
    
    def day_frequency(self, from_me=None):
        dates_freq = {}

        for message in self.messages:
            date = message['date'].date()

            if date not in dates_freq:
                dates_freq[date] = 1
            else:
                dates_freq[date] = dates_freq[date]+1
        
        min_date = min(dates_freq.keys())
        max_date = max(dates_freq.keys())

        print(f'{min_date} {max_date}')

        date_difference =  (max_date-min_date).days + 1 # timedelta obj

        all_dates = [min_date]

        for i in range(1, date_difference):
            all_dates.append(all_dates[i-1] + datetime.timedelta(days=1))

        dates_dict = {}
        dates_dict['date'] = []
        dates_dict['messages_sent'] = []


        for date in all_dates:
            if date not in dates_freq:
                dates_dict['date'].append(date)
                dates_dict['messages_sent'].append(0)
            else:
                dates_dict['date'].append(date)
                dates_dict['messages_sent'].append(dates_freq[date])

        dates_freq = pd.DataFrame(dates_dict)
        dates_freq.set_index('date', inplace=True)

        return dates_freq
        
