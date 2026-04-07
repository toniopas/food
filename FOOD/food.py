class Food:
    """ class food """
    __name = None
    __calories = None
    __fat = None
    __carbs = None
    __proteins = None

    def get_name(self):
        """ function : get the food name """
        return self.__name

    def set_name(self,name):
        """ function : set the food name """
        self.__name = name

    def get_calories(self):
        """ function : get the property named calories of the food """
        

    def set_calories(self,calories):
        """ function : set the property named calories of the food """
        

    def get_fat(self):
        """ function : get the property named fat of the food """
        

    def set_fat(self,fat):
        """ function : set the property named fat of the food """
        

    def get_carbs(self):
        """ function : get the property named carbs of the food """
        

    def set_carbs(self,carbs):
        """ function : set the property named carbs of the food """
        

    def get_proteins(self):
        """ function : get the property named proteins of the food """
    
    
    def set_proteins(self,proteins):
        """ function : get the property named proteins of the food """
        

    def retrieve_food_infos(self,food_name):
        """ function : scrap the properties of the food from a website given its name
        
        - think of making the URL a global variable
        - check whether the request succeed before trying to parse the payload
        - if not succesfull, raise an error
        
        """
        

    def display_food_infos(self):
        """ function : display the properties of the food 
        the outlook should be similar to this:
                ------------------------------------------------
                name	    calories	fat	    carbs	proteins
                tomate	    21.0		0.3	    4.6	    0.8
                ------------------------------------------------
        """
    
    

    def save_to_csv_file(self, file_name):
        """ function : save the properties of the food in a csv file 
        - use function with for file opening
        """


    def is_fat(self):
        """ function : return true or false whether the food has more than 20% of fat 
        - define a fat threshold and write the function accordingly
        """
        
