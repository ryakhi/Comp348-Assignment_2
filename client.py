#By Ryan Anthony Khireddine

import socket #Imports the module for the client side
import sys #For sys.exit
import os #For os.system("clear")

HOST, PORT = "localhost", 9999 #The configuration details that match the server side

def socket_connection_and_data(data_to_send):
    print(f"\nRequesting: {data_to_send.split('|')[0]}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #Creates a socket
        try:
            sock.connect((HOST, PORT)) #Connects to the server
            sock.sendall(data_to_send.encode()) #Sends data to the server
            received = sock.recv(65536)
            server_response = received.decode()
            print(f"\nServer response: {server_response}") #Displays the server response
            return True

        except ConnectionRefusedError: #Exception if the server is not running or using the right port
            print(f"Error: Could not connect to server at {HOST}: {PORT}. Please make sure server.py is running.")
        except OSError as e:
            print(f"AN I/O or socket error has occured: {e}")
        except Exception as e: #For any exception
            print(f"An error occured: {e}")
            return False


def run_client(): #Holds my main menu loop

    while True: #Loops until the user selects option 8 to exit
        os.system('clear') #Clears the terminal

        print("""Python DB Menu
\n1. Find Customer 
2. Add Customer
3. Delete Customer
4. Update Customer Age
5. Update Customer Address
6. Update Customer Phone
7. Print Report
8. Exit""")

        option_string = input("Select: ") #Will take the user's input
        request_data = None #Holds the action string
        try:
            option = int(option_string) #Casts the user input as an int for the switch case
        except ValueError: #In case the user inputs something invalid, I change it to 0 so it activates the default case in the switch statement
            option = 0

        match option: #Switch for what the user chooses from the main menu
            case 1: ##If the user wants to find a customer
                customer_name = input("Customer Name: ")
                request_data = f"FIND|{customer_name}" #Looks for the customer name in the string

            case 2: #If the user wants to add a customer
                customer_name = input("Customer Name: ")
                customer_age = input("Customer Age: ")
                customer_address = input("Customer Address: ")
                customer_phone = input("Customer Phone: ")
                request_data = f"ADD|{customer_name}|{customer_age}|{customer_address}|{customer_phone}"

            case 3: #If the user wants to delete the name
                customer_name = input("Customer Name: ")
                request_data = f"DELETE|{customer_name}"  
    
            case 4: #If the user wants to update the age
                customer_name = input("Customer Name: ")
                customer_age = input("Customer Age: ")
                request_data = f"UPDATE_AGE|{customer_name}|{customer_age}"
        
            case 5: #If the user wants to update the address
                customer_name = input("Customer Name: ")
                customer_address = input("Customer Address: ")
                request_data = f"UPDATE_ADDRESS|{customer_name}|{customer_address}"
            
            case 6: #If the user wants to update the phone number
                customer_name = input("Customer Name: ")
                customer_phone = input("Customer Phone: ")
                request_data = f"UPDATE_PHONE|{customer_name}|{customer_phone}"

            case 7: #If the user wants the report to be printed
                request_data = "REPORT"

            case 8: #If the user wants to exit the program
                print("Exiting program. Good bye!")
                sys.exit(0) #Exits the client application

            case _:
                print("\nYou chose an invalid option. Please try again with a valid number between 1 and 8!")
                request_data = None #Skips the communication step because there is no need

        if request_data:
            socket_connection_and_data(request_data) #This will connect, send the request, and display the server response

        input("\nPress any key to continue...") #When the user presses a key, it will start the loop again

if __name__ == "__main__": #Makes sure the code runs only if its in the file directly
    run_client() 