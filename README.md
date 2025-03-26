# Firewall-agent-checker



# Setup
## Configure Resources
### Deploy Azure Resources
- Azure OpenAI service
- Azure OpenAI model deployments (e.g. gpt-4o& gpt-4o-mini)
- Azure Storage Account
- Azure AI Search Service

### Upload Data
- Create a container in the Azure storage account
- create a risk folder and upload the "general_network_risks"
- create a test folder and upload the "testdata_existing_rules"

### Create AI search index
- Use the import function in AI Search to index the general network risks
- Make sure to use the CSV parser method
- Modify the index and make sure to adjust the retrievable, searchable fields etc.

## Create virtual environment
### 1. If you're not already in the folder where you want the environment:
```bash
cd /path/to/your/project
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment
On macOS/Linux/WSL:
```bash
source .venv/bin/activate
```

On Windows CMD:
```cmd
.venv\Scripts\activate.bat
```

On Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

## Install requirements
```bash
pip install -r requirements.txt
```

## Fill out .env variables
Example for .env file is shown in the file "env.example"


