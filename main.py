import requests
import random
import time
import os
from colorama import Fore, init

# Initialize colorama for Windows
init(autoreset=True)

time.sleep(1)

channel_id = input("Enter Channel ID (Not Server)        :   ").strip()
time2 = int(input("Set the time to send the messages    :   "))
time1 = int(input("Set the time to delete messages      :   "))

time.sleep(1)

# Clear console
os.system('cls' if os.name == 'nt' else 'clear')

# Read messages with UTF-8 encoding
with open("message.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

# Read authorization token
with open("token.txt", "r", encoding="utf-8") as f:
    authorization = f.readline().strip()

headers = {'Authorization': authorization}

while True:
    payload = {'content': random.choice(words)}
    
    # Send message
    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload, headers=headers)
    if r.status_code == 200:
        print(Fore.WHITE + "Sent message: ")
        print(Fore.YELLOW + payload['content'])
    else:
        print(Fore.RED + f"Failed to send message: {r.status_code}")
        continue
    
    # Wait before deleting
    time.sleep(time1)
    
    # Get messages from channel
    response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            message_id = messages[0]['id']
            
            # Delete message
            delete_response = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=headers)
            if delete_response.status_code == 204:
                print(Fore.GREEN + f"Message with ID {message_id} deleted successfully")
            else:
                print(Fore.RED + f"Failed to delete message {message_id}: {delete_response.status_code}")
        else:
            print(Fore.RED + "No messages found in the channel.")
    else:
        print(Fore.RED + f"Failed to get messages: {response.status_code}")
    
    # Wait before sending the next message
    time.sleep(time2)
