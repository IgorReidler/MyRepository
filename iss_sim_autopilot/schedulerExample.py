import sched, time
from multiprocessing import Process

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    # do your stuff
    s.enter(3, 1, do_something, (sc,))

def run_job()
    p1 = Process(target=run_crawler_schedule)
    p2 = Process(target=run_fix)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


s.enter(3, 1, do_something, (s,))
s.run()

