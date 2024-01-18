# Credit Card Fault Detection Model devlopment and deployment in AWS sagemaker

This project contains 4 folders:
    1. data => it contains the credit card transaction data
    2. notebooks => it contains the Exploratory Data Analysis, model devolopment jupyter notebooks
    3. visuals => it contains the model results and EDA consolidated html page.
    4. deployment => it contains all the code required to deploy the model devloped in AWS sagemaker

## How to use:

1. create a virtual environment using: python -m venv .venv

2. activate .venv based on your os (linux/mac: .venv/bin/activate, windows: .venv\Scripts\activate.bat)

3. install all the libraries provided in service-requiremnts.txt using: pip install -r service-requirements.txt

4. start with notebooks and explore the EDA.ipynb containing data analysis and CreditCardFraud.ipynb containing three approaches for model devolopment and finalised one model.

5. Stored the finalised model as model.pkl and fault specs in specs.json in a folder named model. And stored all the visuals of EDA.ipynb in visuals folder.

6. Now follow the Model_Creation_Report.pdf to see all the results and the instructions for deployemnt of model.

7. All the code required to deploy the model is in deployment folder and instructions are provided in Model_Creation_Report.pdf

