

from subprocess import Popen, PIPE # Used to run native OS commads in python

#takes a mac address and runs "sudo batctl throughputmeter <mac>"
def runthroughput(mac):

        
        scan_command = ['sudo','batctl','throughputmeter', mac]
        #print("ran batctl n")

        scan_process = Popen(scan_command, stdout=PIPE, stderr=PIPE)
        # Returns the 'success' and 'error' output.
        (raw_output, raw_error) = scan_process.communicate() 
        # Block all execution, until the scanning completes.
        scan_process.wait()
        # Returns all output in a dictionary.
        return {'output':raw_output,'error':raw_error}

def getspeed(raw_cell_string):
    raw_cells = raw_cell_string.split('(') # Divide raw string into raw cells. hopefully just one with speed value
    raw_cells.pop(0) # Remove 'test'
    if(len(raw_cells) > 0): # Continue execution, if atleast one node is detected.
        # Array will hold all parsed cells as dictionaries.
        speed_info = [cell.split()[0] for cell in raw_cells]
        # Return list of addresses
        speed = float(speed_info[0])   #convert to float
        return speed
    else:
        print("destination unreachable (speed function)")
        return False

def getunits(raw_cell_string):
    raw_cells = raw_cell_string.split(' ') # Divide raw string into raw cells. last one should be units
    del raw_cells[0:8]
    unit = raw_cells[0][:-2]
    if(len(raw_cells) > 0): # Continue execution, if atleast one node is detected.
        if unit == 'Mbps':
            return 'M'
        elif unit == 'Kbps':
            return 'K'
        elif unit == 'Bps':
            return 'b'
        else:
            return 'unit error'
        return unit
    else:
        print("destination unreachable (units function)")
        return False


def convert_units(speed, bits):
    if bits == 'M':
        speed = speed/8    #convert from Mbps to MB/s
    elif bits == 'K':
        speed = speed/8000    #convert form Kbps to MB/s
    else:
        speed = speed/8000000    #convert from bps to MB/s (yikes)
    return speed


def main():
    results = open("throughputmeter_results.txt", "a")  #open results file for appending
    #mac = 'b8:27:eb:c4:a8:ab'
    mac = input("Enter the mac address to run meter to: ")
    label = input("Enter name for test: ")
    results.write(label)
    results.write("\t")
    print("\n")
    print("starting")
    print("\n")
    ctr = 0
    fail = 0
    while (ctr < 20):
        raw_scan_output = runthroughput(mac)['output']
        raw_scan_output = raw_scan_output.decode('utf-8') #convert to correct format
        print(raw_scan_output)
        units = getunits(raw_scan_output) #extract and return units from command output
        speed = getspeed(raw_scan_output)  #extract and return speed from command output
        if units == 'M': #check if units were in Mbps
            speed = convert_units(speed, 'M')
            speed = round(speed, 3)
            speed_str = str(speed)  #change speed back to string for writing
            results.write(speed_str)
            results.write("\t")
            ctr += 1
        elif units == 'K': #check if units were in Kbps
            speed = convert_units(speed, 'K')
            speed = round(speed, 3)
            speed_str = str(speed)  #change speed back to string for writing
            results.write(speed_str)
            results.write("\t")
            ctr += 1
        elif units == 'b': #check if units were in bps
            fail += 1
        else:
            print("error getting speed")
            fail += 1
    fail_str = str(fail)
    results.write(fail_str)
    results.write("\t")
    results.write("\n")
    results.write("\n")
    results.write("\n")
    results.close()
    
main()
