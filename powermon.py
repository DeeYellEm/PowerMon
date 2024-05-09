###!/usr/bin/env python3
import sys, time, logging
from datetime import datetime, timedelta
import os.path
# from datetime import datetime

# d1 = datetime.strptime("2015-08-10 19:33:27", "%Y-%m-%d %H:%M:%S")
# d2 = datetime.strptime("2015-08-10 20:34:27", "%Y-%m-%d %H:%M:%S")

# diff = d2-d1
# print("Difference: ", diff)

# now = datetime.now()
# print("now =", now)

# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
# print("date and time:",date_time)

def main(args):
    return 0

if __name__ == "__main__":


    # Globals
    rootPath = "/home/darrin/PowerMon/"
    filename = "lastDateTime.txt"
    uptimeFile = "uptime.txt"
    outagePath = "Outages/"

    # logging - Set level=logging.DEBUG to get debug messages
    logging.basicConfig(filename=rootPath+'powermon.log', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    #logging.warning('This will get logged to a file')

    # Be sure that lastDateTime.txt exists in case this is the first run
    if not os.path.isfile(rootPath+filename):
        # Last timecheck does NOT exist.  Create it.  Should only be true on first run
        #print("Note: Creating lastDateTime.txt")
        f = open(rootPath+filename, "w")
        f.write(curTime)
        logging.info("Initial write to create file: [%s]", str(curTime))
        f.close()

    # Now, we know that since we're being called, there's an outage situation.  So, handle that.
    now = datetime.now()
    startTime = now
    curTime = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.info("Logging outage: %s", str(curTime))
    # Calculate the difference between curTime and lastDateTime
    # Open timecheck
    if os.path.isfile(rootPath+filename):

        f = open(rootPath+filename, "r")
        # Read the timecheck
        last = str(f.readline().strip())
        #print("Read from file: [", last, "].")
        lastDateTime = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
        #Close timecheck
        f.close()

    diffTime = now - lastDateTime
    #print ("diffTime is: ", diffTime)
    timeDelta = diffTime.total_seconds()
    #print("timeDelta is:", timeDelta)
    timeDeltaSplit = str(diffTime).split(".")

    # We have had a power outage.  Write a PowerOutage filename
    # Check for the Outages directory and writeable
    if os.path.exists(rootPath+outagePath):
        if os.access(rootPath+outagePath, os.W_OK):
            curOutageString = now.strftime("%Y-%m-%d_%H:%M:%S")
            f = open(rootPath+outagePath+curOutageString, "w")
            f.write(curOutageString+"|"+timeDeltaSplit[0])
            f.close()

        else:
            noError = False
            logging.error("Unable to access Outage directory: [%s]", str(rootPath+outagePath))
    else:
        logging.error("Unable to find Outage directory: [%s]", str(rootPath+outagePath))

    noError = True
    while(noError):
        # This loop simply moves the currentTime file contents along once per minute
        now = datetime.now()
        curTime = now.strftime("%Y-%m-%d %H:%M:%S")
        #print("curTime:",curTime)

        # Whether we had an outage or not, we need to update to the current time in the timecheck file before we sleep again
        if os.path.exists(rootPath+filename):
            if os.access(rootPath+filename, os.W_OK):
                f = open(rootPath+filename, "w")
                f.write(curTime)
                #print("Note: Updating timecheck to curTime: [", str(curTime), "].")
                f.close()
            else:
                noError = False
                logging.error("Unable to access: %s", str(rootPath+filename))
        else:
            logging.error("Unable to find %s", str(rootPath+filename))


        uptime = str(now - startTime).split(".")[0]
        # For convenience, write the current uptime to a file to make it more easily accessible outside this script
        if os.path.exists(rootPath):
            f = open(rootPath+uptimeFile, "w")
            f.write(uptime)
            f.close()
        else:
            logging.error("Unable to find rootPath: [%s].", rootPath)

        logging.debug("Snoozing...[@%s]",uptime)
        time.sleep(60)

    sys.exit(main(sys.argv))
