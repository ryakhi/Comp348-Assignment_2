#By Ryan Anthony Khireddine

import socketserver #Imports the module for the server side. The following code is based off the source: https://docs.python.org/3/library/socketserver.html#examples
import sys #For sys.exit
import os #For os.system("clear")

#I used this source: https://docs.python.org/3/library/socketserver.html#examples

HOST, PORT = "localhost", 9999 #These are the configuration details which uses the local host for the development and port 9999
DATA_FILE = "data.txt"
 
CUSTOMER_DB = {} #This will hold the customer data in a dictionary
 
def validate_phone_format(phone_str): #Function that I created to check if the phone number format is valid. This function simplifies my code later on
    phone_number_length = 8
    valid_line_indexes = ["394", "426", "901", "514"] #Saving the valid first 3 numbers of the phone number
    stripped_phone = phone_str.strip()
 
    if not stripped_phone: #An empty phone number is valid
        return True
 
    if len(stripped_phone) != phone_number_length or stripped_phone[3] != "-": #If the phone number is longer than 8 digits or if the 4th digit is not a -
        return False
    
    prefix_phone_number = stripped_phone[:3]
    suffix_phone_number = stripped_phone[4:]
 
    if not prefix_phone_number.isdigit() or not suffix_phone_number.isdigit(): #If the first 3 digits and last 4 digits are not numbers 
        return False
    
    if prefix_phone_number not in valid_line_indexes:
        return False
    
    return True
 
def validate_record(record_parts, line_number): #Validates a single record line from the data.txt file for the needed fields and types
    if len(record_parts) != 4:
        print(f"DB read error: Record skipped [{'|'.join(record_parts)}]")
        return None
 
    name, age_str, address, phone_str = record_parts
 
    if not name.strip(): #If the name field is empty or only whitespace
        print(f"DB read error: Record skipped [null key field]: {'|'.join(record_parts)}")
        return None
 
    try: #Checks if the age is a positive integer
        age = int(age_str.strip())
        if age < 0 or age > 120:
            raise ValueError
    except ValueError:
        print(f"DB read error: Record skipped [invalid age field]: {line_number}")
        return None
    
    if not validate_phone_format(phone_str): #If the phone number does not obey the formatting constraint 
        print(f"DB read error: Record skipped [invalid phone field]: {line_number}")
        return None
    
    return{ #The record is valid now
        'age' : age,
        'address' : address.strip(),
        'phone' : phone_str.strip()
    }
 
def load_database(): #This function will read the data.txt and validate each record before putting the info in the customer dictionary
    customer_count = 0
    bad_record_count = 0
 
    print(f"Loading database from {DATA_FILE} ...")
 
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                parts = [p.strip() for p in line.strip().split('|')] #I separate each character with |
 
                if not any(parts) or (len(parts) == 1 and not parts [0]): #This skips lines that only contain whitespace after they were stripped
                    continue
 
                valid_data = validate_record(parts, line_number)
 
                if valid_data:
                    name = parts[0].strip()
                    capitalized_name = name.capitalize()
                    if capitalized_name in CUSTOMER_DB: #Checks for duplicate names at load time
                        print(f"DB read error: Record skipped [key/record already exists]: {'|'.join(parts)}")
                        bad_record_count += 1
                    else:
                        CUSTOMER_DB[capitalized_name] = valid_data #Adds them in the dictionary, and uses their name as key
                        customer_count += 1 #I save the number of valid customers
 
                else:
                    bad_record_count += 1 #I save the number of non valid customers
 
    except FileNotFoundError: #If it cannot find the data.txt file
        print(f"Python DB Server (ERROR): {DATA_FILE} not found. Starting with an empty database.")
        return
 
    print(f"Python DB Server is now running... \nLoaded {customer_count} records and rejected {bad_record_count} bad records")
 
def find_customer(name): #This function is for option 1: if the user wants to find a customer by their name
    capitalized_name = name.capitalize()
    if capitalized_name in CUSTOMER_DB:
        record = CUSTOMER_DB[capitalized_name]
        customer_info = f"{capitalized_name}|{record['age']}|{record['address']}|{record['phone']}" #Saves the customer's info in the following format: NAME|AGE|ADDRESS|PHONE
        return f"\n{customer_info}"
    else:
        return f"\n{capitalized_name} not found in database"
    
def add_customer(name, age_str, address, phone_str): #For option 2: if the user wants to add a customer
    try: #Checks if the age is a positive integer
        age = int(age_str.strip())
        if age < 0 or age > 120:
            raise ValueError
    except ValueError:
        return f"DB add error: record contains invalid age: [{age_str}]" #References age_str since age may not have been assigned
 
    if not validate_phone_format(phone_str): 
        return f"DB add error: Record contains invalid phone number: [{phone_str}]"
    
    capitalized_name = name.capitalize()
    if capitalized_name in CUSTOMER_DB: #Checks if the persons name is already in the database
        return f"{capitalized_name} already stored in the database"
    else:
        CUSTOMER_DB[capitalized_name] = {
        'age' : age,
        'address' : address.strip(),
        'phone' : phone_str.strip()
        }
        return f"{capitalized_name}|{age}|{address}|{phone_str} added to database"
 
def delete_customer(name): #FOr option 3: if the user wants to delete a customer
    capitalized_name = name.capitalize()
    if capitalized_name in CUSTOMER_DB: 
        del CUSTOMER_DB[capitalized_name]
        return f"{capitalized_name} deleted from database"
    else:
        return f"Customer named {capitalized_name} does not exist"
    
def update_field(name, field, new_value_str): #For options 4, 5, and 6: of the user decides to update a certain field
    capitalized_name = name.capitalize()
 
    if capitalized_name not in CUSTOMER_DB: #If thr name the user inputted is not in the dictionary
        return f"{capitalized_name} not found. Unable to update"
    
    new_value = new_value_str #Initializes the new_value variable which will be used to save the age as an int
    if field == 'age': #For option 4: updating the age
        try:
            if new_value != '':
                new_value = int(new_value_str) #Converts the generic new value string to an int for the age
                if new_value  < 0 or new_value > 120:
                    raise ValueError
        except ValueError:
            return f"DB update error: attempt to update using invalid age [{new_value}]"
        
    elif field == 'phone': #FOr option 5: updating the phone number
        if new_value and not validate_phone_format(new_value): #Checks if the new value is null or if it respects the ohone number constraints
            return f"DB update error: attempt to update using invalid phone number: [{new_value}]"
        
    CUSTOMER_DB[capitalized_name][field] = new_value #Updates the database
    return f"Customer updated. {capitalized_name}'s {field} is now set to {new_value_str}"
 
def print_report():#For option 7 and prints a formatted report
    global CUSTOMER_DB #I convert the database to global to make it easier to make changes to it 
 
    if not CUSTOMER_DB: #If the dictionary is empty
        return "DB Report: The database is empty"
 
    sorted_names = sorted(CUSTOMER_DB.keys()) #Sorts the dictionary in alphabetical order
 
    header = ( #TO properly format the titles of the colums
        "\n++\n++ DB Report\n++\n\n"
        f"{'Name':<10} {'Age':<5} {'Address':<28} {'Phone':<19}" #{}:< is a format specifier that I got from the source: https://docs.python.org/3/tutorial/inputoutput.html
    )
    separator = ( #To properly format the --- under the title
        f"{'----':<10} {'---':<5} {'-------':<28} {'-----':<19}"
    )
 
    DB_report_format = f"{header}\n{separator}" #Formats the header
    report_lines = []
 
    for name in sorted_names: #Sorts through the array
        record = CUSTOMER_DB[name]
        line = (
            f"{name.capitalize():<10} "
            f"{str(record.get('age', '')):<5} "
            f"{record.get('address', ''):<28} "
            f"{record.get('phone', ''):<19}"
        )
        report_lines.append(line)
 
    return DB_report_format + "\n" + "\n".join(report_lines) + "\n"
 
class myTCPHandler(socketserver.BaseRequestHandler): #Defines the handler that will process the client's requests. Inspired myself off of https://docs.python.org/3/library/socketserver.html#examples
 
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request_string = self.data.decode()
        print(f"Server: Received request: {request_string}")
        
        request_parts = [p.strip() for p in request_string.split('|')] #Parses the request string
        action = request_parts[0]
 
        response_data = "Error: Unknown action or misformed request." #I initize the default request string here in case stuff do not go as planned
 
        #THe dispatch logic is here:
        if action == "FIND" and len(request_parts) ==2: #For option 1
            name = request_parts[1]
            response_data = find_customer(name)
 
        elif action == "ADD" and len(request_parts) == 5: #For option 2
            name, age, address, phone = request_parts[1:5]
            response_data = add_customer(name, age, address, phone)
 
        elif action == "DELETE" and len(request_parts) == 2: #For option 3
            name = request_parts[1]
            response_data = delete_customer(name)
 
        elif action == "UPDATE_AGE" and len(request_parts) == 3: #FOr option 4
            name, new_age = request_parts[1], request_parts[2]
            response_data = update_field(name, 'age', new_age)
        
        elif action == "UPDATE_ADDRESS" and len(request_parts) == 3: #For option 5
            name, new_address = request_parts[1], request_parts[2]
            response_data = update_field(name, 'address', new_address)
 
        elif action == "UPDATE_PHONE" and len(request_parts) == 3: #FOr option 6
            name, new_phone = request_parts[1], request_parts[2]
            response_data = update_field(name, 'phone', new_phone)
 
        elif action == "REPORT" and len(request_parts) == 1:
            response_data = print_report()
 
        self.request.sendall(response_data.encode()) #Sends the final response back to the client. I used this source to find how to do the oppoiste of decoding, which is encoding: https://docs.python.org/3/library/stdtypes.html#str.encode
 
 
if __name__ == "__main__": #Defines the server and sets up the main loop
    load_database()
 
    try:
        with socketserver.TCPServer((HOST, PORT), myTCPHandler) as server: #Creates the server and binds the localhost on port 9999
            print("Python DB server is now running...")
            server.serve_forever() #Activates the server and it will run in an infinite loop
    except Exception as e: 
        print(f"Server failed to start: {e}")
        sys.exit(1)