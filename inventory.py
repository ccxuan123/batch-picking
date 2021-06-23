import pandas as pd

class Inventory:
    def __init__(self, stock_path, order_path, batch_path):
        self.stock_path = stock_path
        self.order_path = order_path
        self.batch_path = batch_path
    
    def get_all_stock(self):
        return pd.read_csv(self.stock_path)

    def get_all_batch(self):
        return pd.read_csv(self.batch_path)

    def get_all_order(self):
        return pd.read_csv(self.order_path)

    def get_sku_list(self):
        df_stock = self.get_all_stock()
        return df_stock['SKU'].tolist()

    def get_location_list(self):
        df_stock = self.get_all_stock()
        return df_stock["Location"].tolist()

    """ print stock in dataframe """
    def display_current_stock(self):
        df_stock = self.get_all_stock()
        print(df_stock)

    ''' print all orders '''
    def display_all_order(self):
        df_order = self.get_all_order()
        print(df_order)    

    ''' print all batch '''
    def display_all_batch(self):
        df_batch = self.get_all_batch()
        print(df_batch)    

    def display_available_items(self):
        df_stock = self.get_all_stock()
        pass

    def create_order(self):
        df_stock = self.get_all_stock()
        print(df_stock[['SKU', 'Item Name', 'Price']])
        pass

    def display_order_status(self):
        df_order = self.get_all_order()
        print(df_order[["Order No.", "Status"]])

    def update_order_status(self, status, order_num):
        # order_num is in list
        # status is string
        df_order = self.get_all_order()
        try:
            for i in order_num:
                order_row = df_order[df_order["Order No."] == i]
                order_row_index = list(order_row.index)[0]
                df_order.at[order_row_index, 'Status']=status
            df_order.to_csv('db/order_list.csv', sep=',', index=False)
        except:
            print("invalid order list")
        #print(self.df_order)
        pass

    ''' not complete '''
    def get_new_order_df(self):
        df_order = self.get_all_order()
        return df_order.loc[df_order["Status"] == "new"]
        #return filter["Order No."].tolist()

    ''' generate new entry in batch list '''
    def compile_first_5_order_into_batch(self):
        df_batch = self.get_all_batch()
        quantity=[]
        orders = self.get_new_order_df()
        first_5_orders = orders[0:5]
        first_5_order_list = list(first_5_orders['Order No.'])
        if(len(orders) != 0):
            self.update_order_status('processing',first_5_order_list)
            for sku in self.get_sku_list():
                quantity.append(sum(first_5_orders[sku].tolist()))
            new_batch_num = list(df_batch['Batch No.'])[-1]+1
            new_batch_row_df= pd.DataFrame({
                "Batch No.": [new_batch_num],
                "Status": ["new"],
                "TS001": [quantity[0]],
                "TS002": [quantity[1]],
                "TS003": [quantity[2]],
                "TS004": [quantity[3]],
                "TS005": [quantity[4]],
                "TS006": [quantity[5]],
                "TS007": [quantity[6]],
                "TS008": [quantity[7]],
                "TS009": [quantity[8]],
                "CP001": [quantity[9]],
                "CP002": [quantity[10]],
                "CP003": [quantity[11]],
                "Order 1": [first_5_order_list[0]],
                "Order 2": [first_5_order_list[1]],
                "Order 3": [first_5_order_list[2]],
                "Order 4": [first_5_order_list[3]],
                "Order 5": [first_5_order_list[4]],
            })
            new_df = df_batch.append(new_batch_row_df, ignore_index=True)
            new_df.to_csv('db/batch_list.csv', sep=',', index=False)
            print(f'Add a new batch: {new_batch_num}')
        else:
            print("No new orders")
        #self.df_batch.to_csv("db/batch_list.csv", sep=",", header=None, mode="a")
        #if len(new_order_list) > 5:
        #    new_order_list = new_order_list[0:5]   

        #for i in new_order_list:      
        #    order_data = self.df_order.loc[self.df_order["Order No."] == i]
        #    print(order_data)
        pass

    ''' print packing list & update order list to packing '''
    def print_packing_list_new(self):
        df_batch = self.get_all_batch()
        if 'new' in df_batch.values:
            new_batch = df_batch.loc[df_batch['Status'] == 'new']
            first_batch_list = list(new_batch.iloc[0])
        
            pack_list = {
                'SKU': self.get_sku_list(),
                'Location': self.get_location_list(),
                'Quantity': first_batch_list[2:14]
            }
            self.update_order_status('packing',first_batch_list[14:])
            self.update_batch_status('packing',first_batch_list[0] )
            pack_df = pd.DataFrame(pack_list)
            print("Batch No.:" + str(first_batch_list[0]))
            print("Orders:" + str(first_batch_list[14:] ))
            print(pack_df)
        else:
            print("No unprocess batch")
    
    def print_packing_list(self, batch_num):
        df_batch = self.get_all_batch()
        if batch_num in df_batch.values:
            selected_batch = df_batch.loc[df_batch['Batch No.'] == batch_num]
            selected_batch_list = list(selected_batch.iloc[0])
            pack_list = {
                    'SKU': self.get_sku_list(),
                    'Location': self.get_location_list(),
                    'Quantity': selected_batch_list[2:14]
                }
            #self.update_order_status('packing',selected_batch_list[14:])
            pack_df = pd.DataFrame(pack_list)
            print("Packing list")
            print("Batch No.:" + str(selected_batch_list[0]))
            print("Orders:" + str(selected_batch_list[14:] ))
            print(pack_df)
            if (selected_batch_list[1] == 'complete'):
                print("This batch is complete")
            else:
                self.update_order_status('packing',selected_batch_list[14:])
        else:
            print('Invalid batch number')

    
    def update_batch_status(self, status, batch_num):
        df_batch = self.get_all_batch()
        if batch_num in df_batch.values:
            selected_batch = df_batch.loc[df_batch['Batch No.'] == batch_num]
            selected_batch_index = list(selected_batch.index)[0]
            df_batch.at[selected_batch_index, 'Status'] = status
            df_batch.to_csv('db/batch_list.csv', sep=',', index=False)
        else:
            print("invalid batch number")
        pass

    def update_batch_is_complete(self, batch_num):
        df_batch = self.get_all_batch()
        if batch_num in df_batch.values:
            selected_batch = df_batch.loc[df_batch['Batch No.'] == batch_num]
            selected_order_list = list(selected_batch.iloc[0])[14:]
            selected_batch_item_quantity = list(selected_batch.iloc[0])[2:14]
            self.update_order_status('complete', selected_order_list)
            self.update_batch_status('complete', batch_num)
            self.deduct_stock_quantity(selected_batch_item_quantity)
            print(f"Update {batch_num} status to complete")
        else:
            print('Invalid batch number')
        
    def deduct_stock_quantity(self, quantity_list):
        df_stock = self.get_all_stock()
        ori_quantity_list = list(df_stock['Quantity'])
        new_quantity_list=[]
        for i in range(len(ori_quantity_list)):
            new_quantity_list.append(ori_quantity_list[i]-quantity_list[i])
        
        for i in range(len(ori_quantity_list)):
            df_stock.at[i,'Quantity']=new_quantity_list[i]
        df_stock.to_csv('db/current_stock.csv', sep=',', index=False)
        pass

if __name__ == "__main__":
    CURRENTSTOCK_PATH = "db/current_stock.csv"
    ORDERLIST_PATH = "db/order_list.csv"
    BATCHLIST_PATH = "db/batch_list.csv"
    stock = Inventory(CURRENTSTOCK_PATH, ORDERLIST_PATH, BATCHLIST_PATH)

    quantity = [10, 3, 3, 5, 3, 1, 7, 3, 2, 2, 1, 5]
    #stock.compile_first_5_order_into_batch()
    #stock.print_packing_list_new()
    #stock.update_batch_is_complete(200002)
    #stock.print_packing_list(200003)
    #stock.deduct_stock_quantity(quantity)
    #stock.create_order()
    df = pd.read_csv(CURRENTSTOCK_PATH)
    print('full dataframe')
    print(df)
    for i in range (df.shape[0]):
        print(list(df.iloc[i]))







    

        
