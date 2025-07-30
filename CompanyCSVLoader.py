import csv

class CompanyCSVLoader:
    def __init__(self, csv_file_path):
        """
        :param csv_file_path: The path to the CSV file containing company data.
        """
        self.csv_file_path = csv_file_path
        # This dictionary will map company name -> row data
        self.data_by_company = {}

    def load_data(self):
        """
        Reads the CSV file and populates self.data_by_company
        so that each key is the company name, and the value is
        a dictionary of the other columns.
        """
        with open(self.csv_file_path, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"Reading CSV file: {self.csv_file_path}")
            print(f"CSV file contains the following columns: {reader.fieldnames}")
            for row in reader:
                company_name = row.get('listing_title')
                
                if company_name:
                    # Store the entire row in a nested dictionary,
                    # keyed by the company's name.
                    self.data_by_company[company_name] = row

# Example Usage:
# loader = CompanyCSVLoader("path/to/Top Growing Companies in USA - AgilePR Company Directory.csv")
# loader.load_data()
# print(loader.data_by_company["Vytalize Health"])
