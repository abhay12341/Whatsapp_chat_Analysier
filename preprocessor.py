import re
import pandas as pd
def process(data):
    pattern=r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[APap][Mm]'

    messages=re.split(pattern,data)[1:]
     
    date = re.findall(pattern, data)
    dates = [re.sub(r'\u202f', '', entry) for entry in date]

    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M%p')
    df.rename(columns={'message_date':'date'},inplace=True)
    df.head()
    
    users = []
    messages = []

# Clean and split the 'message' column
    for message in df['user_message']:
        if isinstance(message, str):  # Check if it's a string
          ent = re.split('([\w\s]+):\s', message)
          if ent[1:]:
            users.append(ent[1])
            messages.append(ent[2])
          else:
            users.append('group_notification')
            messages.append(ent[0])
        else:
           users.append('non_string_value')
           messages.append('non_string_value')

# Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)
# Display the DataFrame

    df['only_date']=df['date'].dt.date
    df['year']=df['date'].dt.year  
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()   
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period=[]
    # 
    for hour in df['hour']:
       next_hour = (hour + 1) % 24
       period.append(f'{hour % 12 if hour % 12 != 0 else 12}:{next_hour % 12 if next_hour % 12 != 0 else 12} {"AM" if hour < 12 else "PM"} - {next_hour % 12 if next_hour % 12 != 0 else 12}:{(next_hour + 1) % 12 if (next_hour + 1) % 12 != 0 else 12} {"AM" if next_hour < 12 else "PM"}')

    df['period'] = period


    return df
