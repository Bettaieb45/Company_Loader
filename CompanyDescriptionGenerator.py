import csv
from openai import OpenAI
from utils.format_employee_count import format_employee_count

class CompanyDescriptionGenerator:
    """
    Generates HTML-formatted marketing descriptions and SEO metadata for companies,
    and saves them to a CSV file.
    """
    def __init__(self, data_by_company, openai_api_key):
        self.data_by_company = data_by_company
        self.client = OpenAI(api_key=openai_api_key)
        self.results = []

    def _build_prompt(self, row_data):
        company_name = row_data.get('listing_title', '')
        raw_employee_str = row_data.get('employee_number', '')
        website_url = row_data.get('website', '')
        state = row_data.get('state', '')
        city = row_data.get('city', '')
        industry = row_data.get('industry', '')
        founded_year = row_data.get('founded', '')
        summary = row_data.get('short_description', '')

        employee_count = format_employee_count(raw_employee_str)

        prompt = f"""
You are a marketing and SEO copywriter. Generate the following three things for the company described below:

1. A <strong>clean HTML-formatted description</strong> in 2–3 paragraphs followed by a bulleted "Key Highlights" section.
2. A concise and catchy <strong>meta title</strong> (max 60 characters).
3. A <strong>meta description</strong> (max 160 characters) that summarizes the company for search engines in a friendly but professional tone.

The HTML output should include:
- Two or three <p> paragraphs describing the company
- A <h3> titled "Company Highlights:"
- A <ul> list with:
    - Specialization
    - Key Offerings
    - Service Area
    - Recognition

The output should be returned <strong>as JSON</strong> in the following format:

{{
  "meta_title": "...",
  "meta_description": "...",
  "description_html": "..."
}}

Company Info:
- Name: {company_name}
- Employees: {employee_count}
- Website: {website_url}
- State: {state}
- City: {city}
- Industry: {industry}
- Founded: {founded_year}
- Summary: {summary}
"""
        return prompt.strip()

    def generate_company_description(self, row_data):
        prompt = self._build_prompt(row_data)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        try:
            import json
            # Sanitize: ensure the model returns a clean JSON block
            first_brace = content.find('{')
            last_brace = content.rfind('}')
            json_str = content[first_brace:last_brace+1]
            parsed = json.loads(json_str)
            return parsed
        except Exception as e:
            print(f"Failed to parse response for {row_data.get('listing_title', '')}: {e}")
            print("Raw content was:\n", content[:300])  # show the first 300 characters for debugging
            return {
                "meta_title": "",
                "meta_description": "",
                "description_html": "[Error parsing response]"
            }


    def generate_all_descriptions(self, output_file="company_descriptions.csv"):
        fieldnames = [
            "Company Name", "State", "City", "Employee Count",
            "Industry", "Website", "Founded",
            "Meta Title", "Meta Description", "Description (HTML)"
        ]

        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

                for company_name, row_data in self.data_by_company.items():
                    print(f"Generating for: {company_name}")
                    result = self.generate_company_description(row_data)
                    
                    row = {
                        "Company Name": company_name,
                        "State": row_data.get('state', ''),
                        "City": row_data.get('city', ''),
                        "Employee Count": format_employee_count(row_data.get('employee_number', '')),
                        "Industry": row_data.get('industry', ''),
                        "Website": row_data.get('website', ''),
                        "Founded": row_data.get('founded', ''),
                        "Meta Title": result["meta_title"],
                        "Meta Description": result["meta_description"],
                        "Description (HTML)": result["description_html"]
                    }

                    writer.writerow(row)
                    self.results.append(row)

            print(f"Descriptions saved to {output_file}")

        except Exception as e:
            print(f"Error writing CSV: {e}")


    def save_results_to_csv(self, output_file="company_descriptions.csv"):
        try:
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = [
                    "Company Name", "State", "City", "Employee Count",
                    "Industry", "Website", "Founded",
                    "Meta Title", "Meta Description", "Description (HTML)"
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in self.results:
                    writer.writerow(row)
            print(f"Descriptions saved to {output_file}")
        except Exception as e:
            print(f"Error writing CSV: {e}")
