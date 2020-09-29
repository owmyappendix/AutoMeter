# AutoMeter
AutoMeter is a simple python program that allows the automation of throughput testing on a network of linux machines running the B.A.T.M.A.N interface
# Note
This program and the documentation was created with a secific use case in mind for a research project. Your use case may differ greatly. My setup was a fleet of ten raspberry pi Zeros running raspberry pi OS Buster and setup up as a mesh netowrk using the  B.A.T.M.A.N advanced interface.

# Configuring before transferring to pi:

The program should work just fine as is but you might want to change some of the following to save some time and make it run how you want. I highly recommend putting in the mac address, the other two, up to you

* To automate mac address, comment out line 71 and comment in line 70, changing 00:00:00:00:00:00:00:00 to the mac you want in the function definition

* The function asks for a name for the test each time in order to allow keeping track of many tests without exporting after each one. To disable this comment out lines 72 and 73

* I opened the file with the append argument in order to add to the bottom of the file if it already exists. I did this to prevent accidentally overwriting data but if you would rather have a new, empty file each time you run the program, change the a to a w in line 69

**Notes:**

* The program writes to a TAB separated file called throughputmeter_results.txt.
* The last value in each line is the average
* I chose to leave off all labels, everything is converted to MB/s
* The program displays the output of throughputmeter in the terminal. For some reason, the MB/s is slightly different from if you take the Mbps value and divide by 8. Instead it is divided by 8.38 for some reason. I chose to just convert the bits per second value to MB/s.
* Sometimes, when running the program I got 0.0 returned. This is not an error. I traced it back and it just means the result was so small, it got rounded off

# Running:
* just copy autometer.py to your bridge with scp, navigate to the folder it is in, and run:
  - python autometer.py
* When done with tests, scp the .txt to host machine
  - scp pi@base.local:/home/pi/Desktop/throughputmeter_results.txt .
    - Replace base with name of pi
    - If you want the txt file in a directory other than the one you are in, replace the period with a path
* Open the .txt in a spreadsheet program or text editor
* Copy results into google sheets

