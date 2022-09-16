from main_proc import upload_and_gen_dataframe
from sql_capture_inserter import insert_captures

insert_captures(upload_and_gen_dataframe(folder=None))
print("main function PERFORMED")