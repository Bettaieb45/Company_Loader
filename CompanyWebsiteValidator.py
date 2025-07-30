import pandas as pd
from urllib.parse import urlparse

class CompanyWebsiteValidator:
    """
    A class to load a CSV containing companies' data and validate the 'website' column.
    
    Attributes:
        csv_path (str): The path to the CSV file.
        df (pd.DataFrame): A DataFrame holding the CSV data.
    """
    
    def __init__(self, csv_path):
        """
        Initialize the validator with the path to the CSV file.
        
        Args:
            csv_path (str): The file path for the CSV.
        """
        self.csv_path = csv_path
        self.df = None

    def load_csv(self):
        """
        Load the CSV into a pandas DataFrame.
        """
        self.df = pd.read_csv(self.csv_path)
        print(f"CSV loaded with {len(self.df)} rows.")

    def is_valid_url(self, url):
        """
        Check if a URL is valid by ensuring it has a scheme and netloc.
        
        A valid URL is expected to have a scheme (http/https) and a network location.
        If a scheme is missing, 'http://' is prefixed and the URL is re-checked.
        
        Args:
            url (str): The URL string to check.
        
        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        # Handle missing or empty URLs
        if pd.isna(url) or url.strip() == "":
            return False
        
        # First parse
        parsed = urlparse(url)
        # If there is no scheme, try prefixing 'http://'
        if not parsed.scheme:
            url = "http://" + url
            parsed = urlparse(url)
        
        # A URL is considered valid if both scheme and network location are present
        return bool(parsed.scheme) and bool(parsed.netloc)

    def validate_websites(self):
        """
        Validate the website column by applying the is_valid_url check.
        
        Creates a new column 'is_valid_website' in the DataFrame, with True for valid
        websites and False for invalid ones. Returns a DataFrame filtered to show only
        the rows with invalid website entries.
        
        Returns:
            pd.DataFrame: Filtered DataFrame containing rows with invalid website URLs.
        """
        # Ensure the CSV data is loaded
        if self.df is None:
            self.load_csv()
            
        # Validate each website value in the 'website' column
        self.df['is_valid_website'] = self.df['website'].apply(lambda x: self.is_valid_url(str(x)))
        
        # Filter rows that are invalid (i.e. where the URL did not pass validation)
        invalid_df = self.df[self.df['is_valid_website'] == False]
        return invalid_df


# Example usage:
if __name__ == "__main__":
    # Path to the CSV file (adjust if needed)
    csv_file = "Top Growing Companies in USA - AgilePR Company Directory.csv"
    
    # Create an instance of the validator
    validator = CompanyWebsiteValidator(csv_file)
    
    # Load the CSV file
    validator.load_csv()
    
    # Validate the website URLs and get a DataFrame of rows with invalid websites
    invalid_websites_df = validator.validate_websites()
    
    # Display some relevant columns for inspection
    if not invalid_websites_df.empty:
        print("Rows with invalid website URLs:")
        print(invalid_websites_df[['Rank', 'listing_title', 'website']])
    else:
        print("All websites appear to be correctly formatted.")
