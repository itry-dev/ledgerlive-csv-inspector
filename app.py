from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'



# Private function to define the required CSV headers
def _required_headers():
    return ['Operation Date', 'Status', 'Currency Ticker', 'Operation Type', 'Operation Amount', 'Operation Fees', 'Operation Hash', 'Account Name', 'Account xpub', 'Countervalue Ticker', 'Countervalue at Operation Date', 'Countervalue at CSV Export']

def _emptyPage():
    return render_template('index.html', data=None,tickers=None, selected_ticker=None,upload_file_enabled = 1)

# Route to render the main page
@app.route('/')
def index():
    df = None
    filtered_df = None
    table_data = None
    tickers = None
    selected_ticker = None

    #check if a csv file exists in uploads folder
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], 'transactions.csv')
    if os.path.exists(filePath):
        try:
            # Read CSV file
            df = pd.read_csv(filePath)
        except Exception as e:
            flash(f"Error processing the CSV file: {str(e)}")
            return _emptyPage()
    else:
        return _emptyPage()
    
        
    # Check if the required headers are in the uploaded CSV
    required_headers = _required_headers()
    if not set(required_headers).issubset(df.columns):
        flash('Invalid CSV headers! The uploaded file must contain the following headers: ' + ', '.join(required_headers))
        return _emptyPage()

 
    
    # If the headers match, pass the data to the template
    # Get the unique tickers for the dropdown menu
    tickers = df['Currency Ticker'].unique()

    # Get the selected ticker from the query parameters (default is None)
    selected_ticker = request.args.get('ticker')
    
    # Filter the data if a ticker is selected
    if selected_ticker and selected_ticker != 'all':
        filtered_df = df[df['Currency Ticker'] == selected_ticker]

        # Format the 'Countervalue at Operation Date' column as currency
        cod = pd.to_numeric(filtered_df['Countervalue at Operation Date'], errors='coerce')
        cce = pd.to_numeric(filtered_df['Countervalue at CSV Export'], errors='coerce')
    
        filtered_df['Countervalue at Operation Date'] = cod
        filtered_df['Countervalue at CSV Export'] = cce

        # Convert Operation Date to datetime for proper grouping
        filtered_df['Operation Year'] = pd.to_datetime(filtered_df['Operation Date']).dt.year    
        
        # Group by Ticker and Operation Date
        grouped_df = filtered_df.groupby(['Currency Ticker', 'Operation Type', 'Operation Year']).sum(numeric_only=True).reset_index()

        # Convert the grouped data to a dictionary for easy rendering
        table_data = grouped_df.to_dict(orient='records')        
    

    # Render the HTML template with the table data
    return render_template('index.html', data=table_data, tickers=tickers, selected_ticker=selected_ticker,upload_file_enabled = False)
    

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    if file and file.filename.endswith('.csv'):
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], 'transactions.csv')
        file.save(filePath)        
        df = pd.read_csv(filePath)

        # Check if the required headers are in the uploaded CSV
        required_headers = _required_headers()
        if not set(required_headers).issubset(df.columns):
            flash('Invalid CSV headers! The uploaded file must contain the following headers: ' + ', '.join(required_headers))
            return redirect('/')
        
        
        return redirect('/')
    else:
        flash('Only CSV files are allowed!')
        return redirect('/')        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
