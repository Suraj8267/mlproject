## Refer to logger python documentation


## ye logging ka setup code hai. Iska kaam hai ki jab tumhare project mein koi important information/error aaye, Python usko ek .log file mein save kare.

import logging  ## for logging all the information
import os  ## os ka use folder/file paths banane aur folders create karne ke liye ho raha hai.
from datetime import datetime  ## Current date aur time lene ke liye.

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # Ye current date/time se filename bana raha hai and strftime() ka matlab hai: Date/time ko apne desired format mein convert karna.

logs_path = os.path.join(os.getcwd(), "logs")
'''
os.getcwd() : Ye batata hai: Abhi Python kis folder mein kaam kar raha hai. 
Result example : E:\MLPROJECT\logs
'''

os.makedirs(logs_path, exist_ok= True)  ## os.makedirs E:\MLPROJECT\logs...isko as a folder bna dega and exist_ok = True : Agar folder pehle se bana hua hai, to error mat dena.

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


## Python, logs ko is file mein save karna aur is format mein save karna.
logging.basicConfig(
    filename= LOG_FILE_PATH,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO,
)

## check weather everything working fine or not 
# if __name__=="__main__":
#     logging.info("logging started")