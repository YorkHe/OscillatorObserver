from libs.oscilloscope.tek import TDS1012B
import datetime
from threading import Thread
from Queue import Queue

class Worker(Thread):
     def __init__(self, tasks):
          Thread.__init__(self)
          self.tasks = tasks
          self.daemon = True
          self.start()

     def run(self):
          while True:
               func, args, kwargs = self.tasks.get()
               try:
                    func(*args, **kwargs)
               except Exception, e:
                    print(e)
               self.tasks.task_done()

class ThreadPool:
     def __init__(self, num_threads):
          self.tasks = Queue(num_threads)
          for _ in range(num_threads):
               Worker(self.tasks)

     def add_task(self, func, *args, **kwargs):
          self.tasks.put((func, args, kwargs))

     def wait_completion(self):
          self.tasks.join()

device = TDS1012B()

device.set_channel(1)

device.get_scale_parameters(device.channel1)

total = 0
start_time = datetime.datetime.now()

pool = ThreadPool(4)

i = 0

def output(x, y):
     for _x, _y in zip(x,y):
          outfile.write(str(_x) + '\t' + str(_y) + '\n')
          outfile.close()

try:
     device.write('data:source ch1')
     device.write('data:encdg ascii')
     while True:
          print("Now output file" + str(total) + ".")
          outfile = open("data/0103/"+str(i)+".data", 'w+')
          e = device.get_wave_form(device.channel1)
          x, y = device.wave.get_wave()
          pool.add_task(output, x, y)
          i = i + 1

except KeyboardInterrupt:
     end_time = datetime.datetime.now()
     print "Program Interrupted."
     print "Time: " + str(end_time-start_time)
     print "Collected: " + str(total)