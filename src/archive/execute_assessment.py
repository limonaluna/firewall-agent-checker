import argparse
import os
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://DEPLOYMENT_NAME.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "API_KEY",
)

# Set up argument parser
parser = argparse.ArgumentParser(description='Perform a risk assessment of Azure Firewall rules.')
parser.add_argument('--firewall_rules', type=str, required=True, help='Path to the CSV file containing the current existing firewall rules.')
parser.add_argument('--known_risks', type=str, required=True, help='Path to the CSV file containing known risks and risky ports.')
parser.add_argument('--output', type=str, required=True, help='Path to the output file for the risk assessment report.')

args = parser.parse_args()

# Initialize Azure OpenAI Service client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Read the content of the CSV files
with open(args.firewall_rules, 'r') as file:    
    firewall_rules_content = file.read()
with open(args.known_risks, 'r') as file:    
    known_risks_content = file.read()

# Define the prompt
prompt = f"""
Perform a comprehensive risk assessment of the existing firewall rules for an Azure Firewall. You will be provided with two CSV files:

Your task is:
- To evaluate all provided firewall rules against the known risks and risky ports.
- Tp identify any potential vulnerabilities or misconfigurations
- To Provide a complete report with all your findings about all the risky rules. do not truncate the report.

Instructions:
- For each line from the Firewall Rules for the assessment CSV:evaluate the risk of the firewall rule according to the risk contained in the Known Risks and Risky Ports and IPs CSV
- High Risk Rules have cvss_score greater or equal than 7, up to 10
- Medium Risk Rules have the cvss_score between 4 and 7
- Low Risk Rules have cvss_score than less than 4
- Ensure that your evaluation is thorough and based on the information provided in the CSV files.
- Avoid introducing unsupported information or speculation.
Output in the form of report:
- Do not escape any of the found risky rules, even if the list is long
- Provide content stricktly following this format:
    -The report header contains the Overall Risk Summary: total number of validated rules, overall risk level with number of risky rules split by the severity: High Risk, Medium Risk, Low Risk
    - The report body contains the Risk Summary Table containing ALL found risky rules with columns: Rule Name, Risk Level, Risk Details,Recommendations. Remember to put all rules that were considered as risky, do not skip any. Order by the risk High, Medium, Low.
    - Do not provide any other content, such as Recommendations Overview, Conclusion, etc.
- Provide a full un-trancated report in Markdown format.

Here are the contents of the CSV files:

Firewall Rules for the assessment:
{firewall_rules_content}

Known Risks and Risky Ports and IPs:
{known_risks_content}
"""

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information.\n"
                + prompt,
            }
        ],
    }
]


# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=chat_prompt,
    max_tokens=16384,
    temperature=0,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
)

# Write formatted markdown report to a file
with open(args.output, 'w') as f:
    f.write(completion.choices[0].message.content.strip())

print(f"The risk assessment report output has been written to {args.output}")

total_tokens = completion.usage.total_tokens
print(f"Total tokens used: {total_tokens}")
