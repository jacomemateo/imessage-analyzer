import sqlite3
import datetime
import pytz

second = 1000000000

def get_chat_mapping(db_location):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()

    cursor.execute("SELECT room_name, display_name FROM chat")
    result_set = cursor.fetchall()

    mapping = {room_name: display_name for room_name, display_name in result_set}

    conn.close()

    return mapping

def apple_date_to_datetime(date):
    jan2001 = datetime.datetime.fromisoformat('2001-01-01')
    jan2001 = jan2001.replace(tzinfo=pytz.UTC)

    new_date = jan2001 + datetime.timedelta(seconds=date/second)

    eastern_timezone = pytz.timezone('US/Eastern')
    new_date = new_date.astimezone(eastern_timezone)

    return new_date

def read_messages(db_location, n=10, self_number='Me', human_readable_date=True, handle_identifyer=1):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()

    query = """
    SELECT message.ROWID, message.date, message.text, message.attributedBody, message.handle_id, message.is_from_me, message.cache_roomnames
    FROM message
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    """

    query += f"WHERE message.handle_id = {handle_identifyer}"

    if n is not None:
        query += f" ORDER BY message.date DESC LIMIT {n}"


    results = cursor.execute(query).fetchall()
    messages = []

    for result in results:
        rowid, date, text, attributed_body, handle_id, is_from_me, cache_roomname = result

        if handle_id is None:
            phone_number = self_number
        else:
            phone_number = handle_id

        if text is not None:
            body = text
        elif attributed_body is None:
            continue
        else:
            attributed_body = attributed_body.decode('utf-8', errors='replace')

            if "NSNumber" in str(attributed_body):
                attributed_body = str(attributed_body).split("NSNumber")[0]
                if "NSString" in attributed_body:
                    attributed_body = str(attributed_body).split("NSString")[1]
                    if "NSDictionary" in attributed_body:
                        attributed_body = str(attributed_body).split("NSDictionary")[0]
                        attributed_body = attributed_body[6:-12]
                        body = attributed_body

        if "Loved “" in body or "Emphasized “" in body or "Laughed at “" in body or "Liked “" in body or "Disliked “" in body or "Questioned “" in body or "20 Questions" == body or "Cup Pong" == body or "Mancala" == body:
            continue

        if human_readable_date:
            date = apple_date_to_datetime(date)

        mapping = get_chat_mapping(db_location)

        try:
            mapped_name = mapping[cache_roomname]
        except:
            mapped_name = None

        messages.append(
            {"rowid": rowid, "date": date, "body": body, "phone_number": phone_number, "is_from_me": is_from_me,
            "cache_roomname": cache_roomname, 'group_chat_name' : mapped_name})

    conn.close()
    return messages