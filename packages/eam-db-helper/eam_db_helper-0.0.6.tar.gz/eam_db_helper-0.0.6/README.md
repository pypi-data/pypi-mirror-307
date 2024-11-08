# This package is used as a layer above MS cosmos db python sdk to interact with data in ms cosmos db sql api.


DatabaseHelper:


DatabaseHelper.get_results():

This method is ussed to get the results from the cosmos db. It takes the query and the parameters of the query as input and returns the results as a list. 



DatabaseHelper.get_result():

This method is used to get the result from the cosmos db. It takes the query and the parameters of the query as input and returns the result as a dictionary.




DatabaseHelper.get_column():

This method is used to get the column from the cosmos db. It takes the query and the parameters of the query as input and returns the column as a list.




DatabaseHelper.delete_item():

This method is used to delete the item from the cosmos db. It takes the item id, as well as the partition key (type) as input and returns None.




DatabaseHelper.upsert():

This method is used to upsert the item in the cosmos db. It takes the item as input and returns None.


