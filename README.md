# Ledger CryptoStatus

Ledger CryptoStatus is an application that allows users to upload CSV files exported from the Ledger Live App. The application performs the following functions:

1. **Upload Form**: Users can upload CSV files.
2. **File Validation**: The uploaded file is checked to ensure it has the correct structure.
3. **Data Filtering**: Users can filter the data by a specific ticker.

This tool helps users manage and analyze their cryptocurrency transactions efficiently.

## Running with Docker

To run the application using Docker, use the following command:

```sh
docker run -d -p 5000:5000 --name ledgerlive-csv-inspector legnagolibera/ledgerlive-csv-inspector:latest
```

The application will be accessible at `http://localhost:5000`.