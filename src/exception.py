## Refer to custom exception error handling documentation

import sys ## Built-in module in python
from logger import logging

def error_messages_details(error, error_detail: sys):  ## parameter : actualerror and error ki detailed information.

    _, _, exc_tb= error_detail.exc_info()  ## exc_tb : traceback : kaha ya konsi file pe exception aya ya konsi line pe exception aya krke 

    file_name = exc_tb.tb_frame.f_code.co_filename  ## file ka name/path

    error_message= "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
   )
    return error_message


class CustomException(Exception): ## custom error class and hum built-in exception ko customize kar rahe hain.
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  ## ye jo error message hai Exception class me bhi store krwa diye hai, Parent Exception ko message dene ka reason hai ki Python ke built-in exception system ko bhi pata rahe ki error kya hai.
        self.error_message = error_messages_details(error_message, error_detail= error_detail)

    def __str__(self):
        return self.error_message  ## print all the error message


## check weather everything working fine or not 
if __name__=="__main__":

    try: 
        a = 1/0
    except Exception as e:
        logging.info("logging has started")
        raise CustomException(e, sys)