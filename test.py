from CompanyCSVLoader import CompanyCSVLoader
from CompanyDescriptionGenerator import CompanyDescriptionGenerator
# Suppose you have:
loader = CompanyCSVLoader("Top Growing Companies in USA - AgilePR Company Directory.csv")
loader.load_data()

# 1. Create a smaller subset of the data_by_company for testing:
max_test_companies = 1000  # adjust as needed
test_data = dict(list(loader.data_by_company.items())[:max_test_companies])


# 2. Initialize the generator with the loaded data
generator = CompanyDescriptionGenerator(test_data, "API Key")

# 3. Generate descriptions for all companies
all_descriptions = generator.generate_all_descriptions()


