# Comp348-Assignment_2
This is a client-server database system in Python with TCP socket communication, data validation, and CRUD management for client directories in memory

**Note: Only server.py and client.py are included. data.txt is not included. You must supply your own before starting the server (see format below).

data.txt Format:
One record per line, fields separated by |:
Name|Age|Address|Phone
Example:
John|34|123 ABC Street|394-3245
Sue|45|Happy Lane|426-3245
Goop||

Validation Rules for the data.txt:
Name — required, must not be empty
Age — must be an integer between 0 and 120; empty is accepted
Address — no constraints
Phone — must follow the format ###-#### where the first 3 digits are one of 394, 426, 901, or 514; empty is accepted
Records with a missing name, invalid age, invalid phone, wrong number of fields, or a duplicate name are skipped and reported on startup

How to Run:
Start the server in the background first, then launch the client in the same directory:
bashpython server.py &
python client.py

To stop the server:
bashps -aux          # find the server process ID
kill <PID>

Notes:
The server runs indefinitely until manually killed, so restarting the client reconnects to the existing server session
All validation and error checking is done on the server side
The database exists in memory only, so changes are not written back to data.txt
