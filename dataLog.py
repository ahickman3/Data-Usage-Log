import subprocess
import re
import time
import tkinter
#!/usr/bin/python


class Bandwidth(object):
    # Find time when bandwidth monitor starts
    init_bw = re.findall('\d+', subprocess.check_output('netstat -e').decode(encoding='windows-1252'))

    def __init__(self, frequency, interval):
        self.initTime = time.time()
        self.init_rec = int(Bandwidth.init_bw[0])  #Set bytes recieved since PC was turned on
        self.init_sent = int(Bandwidth.init_bw[1]) #Set bytes sent since PC was turned on
        self.frequency = frequency                 #How often it will check data
        self.interval = interval                   #How long it will check data

    #Timer function that will determine when data will be logged by calling usage
    def do_every(self):
        def g_tick():
            t = time.time()
            count = 0
            while True:
                count += 1
                yield max(t + count * self.frequency - time.time(), 0)

        g = g_tick()
        count = 0
        while True:
            while (count < self.interval):
                count += 1
                time.sleep(next(g))
                self.usage()
            exit()

    #usage will output bytes recieved and sent since program started
    def usage(self):
        bw = re.findall('\d+', subprocess.check_output('netstat -e').decode(encoding='windows-1252'))
        rec = int(bw[0])
        sent = int(bw[1])
        print('{}\nrecieved = {} \nsent = {}\n'.format(time.time(), rec - self.init_rec, sent - self.init_sent))

findBW = Bandwidth(1, 10) # Check bandwidth every second for 10 seconds
findBW.do_every()         # Call timer function that will check bandwidth at the predetermined intervals
