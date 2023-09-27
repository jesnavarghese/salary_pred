from flask import Flask, render_template , request
import pandas as pd

app = Flask(__name__)

import pickle

with open('model_and_encoders.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

model=loaded_data['model']
encoder=loaded_data['label_encoders']
scaler=loaded_data['scale']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    work_year=request.form['input1']
    experience_level=request.form['input2']
    employment_type=request.form['input3']
    job_title=request.form['input4']
    salary=request.form['input5']
    salary_currency=request.form['input6']
    remote_ratio=request.form['input7']
    company_location=request.form['input8']
    company_size=request.form['input9']

    new_data=[[work_year,experience_level,employment_type,job_title,salary,salary_currency,remote_ratio,company_location,company_size]]
    
    columns=['work_year','experience_level','employment_type','job_title','salary','salary_currency','remote_ratio','company_location','company_size']

    df = pd.DataFrame(new_data,columns=columns)

    # Define data types for specific columns using a dictionary
    dtype_dict = {'work_year': int, 'salary': int, 'remote_ratio': int}

    # Create the DataFrame with specified data types
    new_df = pd.DataFrame(new_data, columns=columns)

    # Convert specific columns to the specified data types
    new_df = new_df.astype(dtype_dict)

    for col in new_df.select_dtypes(include=['object']):
        new_df[col] = encoder[col].transform(new_df[col])

    scld = scaler.transform(new_df)

    return render_template('index.html', result=str(model.predict(scld)))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
