from modules.banking import bank_scrapping
from modules import misc, embedding, web_searching
import asyncio, os



os.system("cls" if os.name == "nt" else "clear")

print(r"""  ______ _                        _____                _____ _    _          _____ _   _ 
 |  ____(_)                      |_   _|   /\         / ____| |  | |   /\   |_   _| \ | |
 | |__   _ _ __   __ _ _ __   ___  | |    /  \ ______| |    | |__| |  /  \    | | |  \| |
 |  __| | | '_ \ / _` | '_ \ / __| | |   / /\ \______| |    |  __  | / /\ \   | | | . ` |
 | |    | | | | | (_| | | | | (__ _| |_ / ____ \     | |____| |  | |/ ____ \ _| |_| |\  |
 |_|    |_|_| |_|\__,_|_| |_|\___|_____/_/    \_\     \_____|_|  |_/_/    \_\_____|_| \_|
                                                                                         
                                                                                         """)
asyncio.run(bank_scrapping())


user_input= input("Prompt >> ")

