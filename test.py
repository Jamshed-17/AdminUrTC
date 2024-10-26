from BackEnd import run_continuously
import schedule




def check_new_question():
    print("NEW QUEST!")

schedule.every(1).second.do(check_new_question)
stop_run_continuously = run_continuously()
# Start the background thread
"""while True:
    print("WHIIILE")
    stop_run_continuously = run_continuously()
    # Do some other things...
    time.sleep(10)
"""