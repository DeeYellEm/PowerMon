###!/usr/bin/env python3
import sys, time, logging, shutil
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
    uptimeFile = "uptime.txt"
    outagePath = "Outages/"
    htmlDir = "/var/www/html/powermon/"
    listFile = "outageTable.html"

    # logging - Set level=logging.DEBUG to get debug messages
    logging.basicConfig(filename=rootPath+'powermon.log', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    #logging.warning('This will get logged to a file')

    # Get the uptime
    if os.path.exists(rootPath+uptimeFile):
        f = open(rootPath+uptimeFile, "r")
        # Read the uptime
        uptime = str(f.readline().strip())
        ti_m = os.path.getmtime(rootPath+uptimeFile)
        m_ti = time.ctime(ti_m)
        f.close()
    # Check for the Outages directory and writeable
    if os.path.exists(rootPath+outagePath):
        if os.access(rootPath+outagePath, os.W_OK):
            l = open(rootPath+listFile, "w")
            l.write("    <table class=\"table\">\n")
            l.write("      <thead>\n")
            l.write("        <tr>\n")
            l.write("          <th scope=\"col\">Date</th>\n")
            l.write("          <th scope=\"col\">Duration</th>\n")
            l.write("        </tr>\n")
            l.write("      </thead>\n")
            l.write("      <tbody>\n")

            dir_list = os.listdir(rootPath+outagePath)
            for file in dir_list:
                #print("Files: ", file,".")
                f = open(rootPath+outagePath+file, "r")
                line = f.readline().split("|")
                l.write("        <tr>\n")
                outline = "        <td>"+str(line[0])+"</td><td>"+str(line[1])+"</td>\n"
                l.write(outline)
                l.write("        </tr>\n")

            l.write("      </tbody>\n")
            l.write("    </table>\n")
            uptimeLine = "<p class=\"fs-5 col-md-8\">Uptime: "+uptime+".</p>\n"
            uptimeLineMod = "<p class=\"fs-5 col-md-8\">Last Modified: "+m_ti+".</p>\n"
            l.write(uptimeLine)
            l.write(uptimeLineMod)
            l.close()
            f.close()

            if os.access(htmlDir, os.W_OK):
                # Copy the listFile to the htmlDir
                print("Copying: "+rootPath+listFile+" to "+htmlDir+listFile+".")
                shutil.copyfile(rootPath+listFile, htmlDir+listFile)
            else:
                logging.error("Unable to access htmlDir: [%s]", htmlDir)

        else:
            logging.error("Unable to access Outage directory: [%s]", str(rootPath+outagePath))
    else:
        logging.error("Unable to find Outage directory: [%s]", str(rootPath+outagePath))

    sys.exit(main(sys.argv))
