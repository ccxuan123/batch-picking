import tkinter as tk
from inventory import Inventory

def print_instruction():
    print('Batch Picking List Generator\n')
    print('A - Display current stock')
    print('B - Display all order')
    print('C - Display all batch')
    print('D - Compile top 5 new orders to batch')
    print('E - Print packing list for new batch')
    print('F - Print selected batch list')
    print('G - Update batch to complete')

if __name__ == "__main__":
    CURRENTSTOCK_PATH = "db/current_stock.csv"
    ORDERLIST_PATH = "db/order_list.csv"
    BATCHLIST_PATH = "db/batch_list.csv"

    stock = Inventory(CURRENTSTOCK_PATH, ORDERLIST_PATH, BATCHLIST_PATH)
    
    c="y" #Runs the while loop as long as user wants

    # display welcome screen
    print_instruction()

    while(c!= "q" or c!= "Q"):
        c= input("Select the action: ")

        if(c=="q" or c=="Q"):
            break

        elif(c=='A' or c=='a'):
            stock.display_current_stock()
            print()
            print_instruction()

        elif(c=='B' or c=='b'):
            stock.display_all_order()
            print()
            print_instruction()

        elif(c=='C' or c=='c'):
            stock.display_all_batch()
            print()
            print_instruction()
        
        elif(c=='D' or c=='d'):
            stock.compile_first_5_order_into_batch()
            print()
            print_instruction()

        elif(c=='E' or c=='e'):
            stock.print_packing_list_new()
            print()
            print_instruction()
            
        elif(c=='F' or c=='f'):
            batch_num = input("Type the batch number:")
            stock.print_packing_list(int(batch_num))
            print()
            print_instruction()

        elif(c=='G' or c=='g'):
            batch_num = input("Type the completed batch:")
            stock.update_batch_is_complete(int(batch_num))
            print()
            print_instruction()



        


