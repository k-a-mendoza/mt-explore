
class ExampleDatabaseInterface:
    """
    an example database interface. All databases fed into mt-explore must
    follow this pattern
    
    """
    
    
    def __init__(self):
        pass
    
    def get_record(self,project : str,station : str,type : str = 'mtpy'):
        """
        returns an mtpy object given a project and station string code
        
        Parameters
        ==========
        
        project : str
        
            the desired project code of the queried station
        
        station : str
            the desired station string
            
        type : str
            the type of object to yield. mt-explore will assign this variable 'mtpy', 
            so make sure any interface that depends on the ExampleDatabaseInterface
            can take these arguments
            
        Returns
        =======
        mtpy_obj : MT
            an mtpy.core.MT object representing the project and station desired
        
        """
        pass
    
    def get_df(self):
        """
        returns a pandas dataframe representation of the databases's station data
        
        Returns
        =======
        dataframe : pd.DataFrame
            a pandas dataframe with columns:
                station, project, latitude, longitude
            must also have a sensible .index
        
        """
        pass