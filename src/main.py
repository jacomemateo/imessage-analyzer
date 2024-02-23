from imessage_analysis import iMessageAnalysis
import matplotlib.pyplot as plt
import pandas as pd
import webview
import getpass
import shutil
import os

chat_db = "res/chat.db" # Location of database
self_number = "Me" # Self identifyer
n = None # Number of messages to return, set to None to retrun everything
stop_list = "res/SmartStoplist.txt" # Path to the stoplist file

handle_identifyer = 89 # The identifyer of the person you want to analyse the
# messages of, i'll probably make u able to select this by contact name later on

output_dir = "out/"

def fetch_chat_db():
    username = getpass.getuser()
    path = "/Users/" + username + "/Library/Messages/chat.db"

    shutil.copyfile(path, "res/chat.db")


if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)

    inpt = input("Enter YES if you would like to fetch the chat.db file: ")
    if inpt == "YES":
        fetch_chat_db()

    inpt = input("Enter YES if you want to re-calculate, otherwise program will look for files in out/ dir: ")
    if inpt == "YES":
        ma = iMessageAnalysis(chat_db, handle_identifyer, n, self_number, stop_list)

        hour_freq = ma.hour_frequency()
        word_freq = ma.word_frequency()
        emoji_freq = ma.emoji_frequency()
        date_freq = ma.day_frequency()

        hour_freq.to_csv(output_dir+'hour.csv')
        word_freq.to_csv(output_dir+'words.csv')
        emoji_freq.to_csv(output_dir+'emojis.csv')
        date_freq.to_csv(output_dir+"day2_freq.csv")


    hour_freq = pd.read_csv(output_dir+'hour.csv')
    word_freq = pd.read_csv(output_dir+'words.csv')
    emoji_freq = pd.read_csv(output_dir+'emojis.csv')
    date_freq  = pd.read_csv(output_dir+"day2_freq.csv")

    html_table1 = hour_freq.to_html(index=False)
    html_table2 = word_freq.head(20).to_html(index=False)
    html_table3 = emoji_freq.head(20).to_html(index=False)

    plt.figure(figsize=(17, 12))

    plt.bar(date_freq['date'], date_freq['messages_sent'])
    plt.xlabel('Date')
    plt.ylabel('Messages Sent')
    plt.title('Messages Sent Over Time')

    n = 10  # Show every nth date
    plt.xticks(date_freq['date'][::n], date_freq['date'][::n], rotation=45) 

    # Save the plot as an image
    plt.savefig(output_dir+'bar_chart.png')


    html_content = f"""
    <html>
    <head>
    <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
        <style>
        .table-container {{
            display: flex;
        }}
        table {{
            margin-right: 20px;
        }}
        </style>
    </head>
    <body>
        <img src="/Users/mateo/Code/Adri/out/bar_chart.png" alt="Not working">
        <div class="table-container" style="margin:auto">
        {html_table1}
        {html_table2}
        {html_table3}
        </div>
    </body>
    </html>
    """

    webview.create_window('iMessage Analysis', html=html_content, min_size=(1200, 1000))

    webview.start()