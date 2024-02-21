from imessage_analysis import iMessageAnalysis
import os

chat_db = "chat.db" # Location of database
self_number = "Me" # Self identifyer
n = 500 # Number of messages to return, set to None to retrun everything
stop_list = "SmartStoplist.txt" # Path to the stoplist file

handle_identifyer = 89 # The identifyer of the person you want to analyse the
# messages of, i'll probably make u able to select this by contact name later on

output_dir = "output/"

if __name__ == "__main__":
    os.makedirs("test", exist_ok=True)

    ma = iMessageAnalysis(chat_db, handle_identifyer, n, self_number, stop_list)

    # adri_word_count = word_frequency(messages, from_me=False)
    # save_to_file(adri_word_count, "adri_messages.csv")

    # mateo_word_count = word_frequency(messages, from_me=True)
    # save_to_file(mateo_word_count, "mateo_messages.csv")

    # combined_word_count = word_frequency(messages)
    # save_to_file(combined_word_count, "combined_messages.csv")

    adri_word_count = ma.emoji_frequency(from_me=False).save(output_dir+"adri_messages.csv")
    mateo_word_count = ma.emoji_frequency(from_me=True).save(output_dir+"mateo_messages.csv")
    combined_word_count = ma.emoji_frequency().save(output_dir+"combined_messages.csv")