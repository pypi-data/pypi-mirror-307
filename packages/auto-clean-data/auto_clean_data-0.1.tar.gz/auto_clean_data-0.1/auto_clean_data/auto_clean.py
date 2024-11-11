import pandas as pd
import os
import json
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import sqlite3
import pymysql
import psycopg2


class Auto_Clean_Data:
    def __init__(self, path):
        self.path = path
        self.data = None
        self.encoded_data = None
        
    def check_dir(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")
    
    def read_file(self):
        self.check_dir()
        try:
            if self.path.endswith(".csv"):
                self.data = pd.read_csv(self.path)
            elif self.path.endswith(".tsv"):
                self.data = pd.read_csv(self.path, sep='\t')
            elif self.path.endswith(".xlsx") or self.path.endswith(".xls"):
                self.data = pd.read_excel(self.path)
            elif self.path.endswith(".json"):
                with open(self.path, 'r') as f:
                    self.data = pd.json_normalize(json.load(f))
            elif self.path.endswith(".txt"):
                self.data = pd.read_csv(self.path, delimiter="\t")
            elif self.path.endswith(".sqlite") or self.path.endswith(".db"):
                conn = sqlite3.connect(self.path)
                self.data = pd.read_sql("SELECT * FROM main", conn)
                conn.close()
            elif self.path.endswith(".sql"):
                conn = sqlite3.connect(self.path) 
                self.data = pd.read_sql("SELECT * FROM your_table_name", conn)
                conn.close()
            elif self.path.endswith(".mysql"):
                conn = pymysql.connect(host="localhost", user="root", password="", database="your_db")
                self.data = pd.read_sql("SELECT * FROM your_table_name", conn)
                conn.close()
            elif self.path.endswith(".psql"):
                conn = psycopg2.connect(dbname="your_db", user="user", password="password", host="localhost")
                self.data = pd.read_sql("SELECT * FROM your_table_name", conn)
                conn.close()
            elif self.path.endswith(".parquet"):
                self.data = pd.read_parquet(self.path)
            elif self.path.endswith(".feather"):
                self.data = pd.read_feather(self.path)
            elif self.path.endswith(".h5"):
                self.data = pd.read_hdf(self.path)
            else:
                raise ValueError("Unsupported file format. Supported formats: CSV, TSV, Excel, JSON, TXT, SQLite, MySQL, PostgreSQL, Parquet, Feather, HDF5.")
            return self.data
        except Exception as e:
            print(f"An error occurred: {e}. Please enter a valid dataset.")
            return None
            
    def data_analyze(self):
        if self.data is not None and not self.data.empty:
            columns = [i for i in self.data.columns]
            missing_counts = [self.data[col].isna().sum() for col in columns]

            total_missing = sum(missing_counts)
            total_data = self.data.size  
            non_missing = total_data - total_missing
            return missing_counts, total_missing, total_data, non_missing
        else:
            print("No data to analyze or the dataset is empty. Please load a valid dataset.")
            return None, None, None, None

    def clean_data(self):
        if self.data is not None and not self.data.empty:
            categorical_columns = self.data.select_dtypes(include="object").columns
            numerical_columns = self.data.select_dtypes(include="number").columns

            label_encoder = LabelEncoder()
            self.data.drop_duplicates(inplace=True)

            if len(self.data) < 1000:
                knn_imputer = KNNImputer(n_neighbors=5)
                if len(numerical_columns) > 0:
                    self.data[numerical_columns] = knn_imputer.fit_transform(self.data[numerical_columns])
            else:
                imputer = IterativeImputer(max_iter=10, random_state=0)
                if len(numerical_columns) > 0:
                    self.data[numerical_columns] = imputer.fit_transform(self.data[numerical_columns])

            self.encoded_data = self.data.copy()
            for column in categorical_columns:
                if self.data[column].isnull().sum() > 0:
                    knn_imputer = KNNImputer(n_neighbors=5)
                    temp_column = self.data[column].astype('category').cat.codes
                    temp_column = temp_column.values.reshape(-1, 1)
                    self.data[column] = knn_imputer.fit_transform(temp_column).flatten()
                self.encoded_data[column] = label_encoder.fit_transform(self.data[column].astype(str))

            print("Data cleaning completed.")
            return self.data, self.encoded_data
        else:
            print("No data to clean or the dataset is empty. Please load a valid dataset.")
            return None

    def save_data(self, save_path):
        if self.data is not None and not self.data.empty:
            try:
                dataset_name = os.path.splitext(os.path.basename(self.path))[0]
                main_folder_path = os.path.join(save_path, dataset_name)
                os.makedirs(main_folder_path, exist_ok=True)

                if self.path.endswith(".csv"):
                    self.data.to_csv(os.path.join(main_folder_path, 'cleaned_data.csv'), index=False)
                    self.encoded_data.to_csv(os.path.join(main_folder_path, 'encoded_data.csv'), index=False)
                elif self.path.endswith(".xlsx") or self.path.endswith(".xls"):
                    self.data.to_excel(os.path.join(main_folder_path, 'cleaned_data.xlsx'), index=False)
                    self.encoded_data.to_excel(os.path.join(main_folder_path, 'encoded_data.xlsx'), index=False)
                elif self.path.endswith(".tsv"):
                    self.data.to_csv(os.path.join(main_folder_path, 'cleaned_data.tsv'), sep='\t', index=False)
                    self.encoded_data.to_csv(os.path.join(main_folder_path, 'encoded_data.tsv'), sep='\t', index=False)
                elif self.path.endswith(".json"):
                    self.data.to_json(os.path.join(main_folder_path, 'cleaned_data.json'), orient='records', lines=True)
                    self.encoded_data.to_json(os.path.join(main_folder_path, 'encoded_data.json'), orient='records', lines=True)
                elif self.path.endswith(".txt"):
                    self.data.to_csv(os.path.join(main_folder_path, 'cleaned_data.txt'), sep='\t', index=False)
                    self.encoded_data.to_csv(os.path.join(main_folder_path, 'encoded_data.txt'), sep='\t', index=False)
                elif self.path.endswith(".sqlite") or self.path.endswith(".db"):
                    conn = sqlite3.connect(os.path.join(main_folder_path, 'cleaned_data.db'))
                    self.data.to_sql('main', conn, index=False, if_exists='replace')
                    self.encoded_data.to_sql('encoded_data', conn, index=False, if_exists='replace')
                    conn.close()
                elif self.path.endswith(".mysql"):
                    conn = pymysql.connect(host="localhost", user="root", password="", database="your_db")
                    self.data.to_sql('main', conn, index=False, if_exists='replace')
                    self.encoded_data.to_sql('encoded_data', conn, index=False, if_exists='replace')
                    conn.close()
                elif self.path.endswith(".psql"):
                    conn = psycopg2.connect(dbname="your_db", user="user", password="password", host="localhost")
                    self.data.to_sql('main', conn, index=False, if_exists='replace')
                    self.encoded_data.to_sql('encoded_data', conn, index=False, if_exists='replace')
                    conn.close()
                elif self.path.endswith(".parquet"):
                    self.data.to_parquet(os.path.join(main_folder_path, 'cleaned_data.parquet'))
                    self.encoded_data.to_parquet(os.path.join(main_folder_path, 'encoded_data.parquet'))
                elif self.path.endswith(".feather"):
                    self.data.to_feather(os.path.join(main_folder_path, 'cleaned_data.feather'))
                    self.encoded_data.to_feather(os.path.join(main_folder_path, 'encoded_data.feather'))
                elif self.path.endswith(".h5"):
                    self.data.to_hdf(os.path.join(main_folder_path, 'cleaned_data.h5'), key='df', mode='w')
                    self.encoded_data.to_hdf(os.path.join(main_folder_path, 'encoded_data.h5'), key='df', mode='w')
                else:
                    raise ValueError("Unsupported file format. Please use .csv, .xlsx, .tsv, .json, .txt, .sqlite, .mysql, .psql, .parquet, .feather, .h5.")
                
                print(f"Data saved to '{main_folder_path}' successfully!")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("No data to save. Please clean the data first.")

    def execute_all(self, save_path):
        self.read_file()
        self.clean_data()
        self.save_data(save_path)
    
    def execute(self, save_path):
        self.read_file()
        missing_counts, total_missing, total_data, non_missing = self.data_analyze()
        if missing_counts:
            print(f"Missing data per column: {missing_counts}")
            print(f"Total Missing Data: {total_missing} / {total_data} = {(total_missing/total_data)*100:.2f}%")
        self.clean_data()
        self.save_data(save_path)

class Auto_Clean_Folder:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.missing_data_info = []

    def process_folder(self, current_folder, cleaned_folder):
        for entry in os.listdir(current_folder):
            entry_path = os.path.join(current_folder, entry)

            if os.path.isfile(entry_path) and entry.endswith((".csv", ".tsv", ".xlsx", ".xls", ".json", ".txt", ".sqlite", ".db", ".mysql", ".psql", ".parquet", ".feather", ".h5")):
                print(f"\nProcessing file: {entry_path}")
                cleaner = Auto_Clean_Data(entry_path)
                cleaner.read_file()  # Make sure data is read before analyzing
                missing_counts, total_missing, total_data, non_missing = cleaner.data_analyze()
                if missing_counts:
                    missing_percentage = (total_missing / total_data) * 100
                    dataset_name = os.path.basename(entry_path)
                    self.missing_data_info.append({'Dataset': dataset_name, 'Missing Percentage': missing_percentage})
                cleaner.execute_all(cleaned_folder)

            elif os.path.isdir(entry_path):
                self.process_folder(entry_path, cleaned_folder)

    def create_missing_data_df(self):
        return pd.DataFrame(self.missing_data_info)

    def process_all_files(self):
        cleaned_folder = os.path.join(self.folder_path, "cleaned_data")
        if not os.path.exists(cleaned_folder):
            os.makedirs(cleaned_folder)
        
        self.process_folder(self.folder_path, cleaned_folder)
        
        missing_data_df = self.create_missing_data_df()
        if not missing_data_df.empty:
            print("\nMissing Data Percentage in Each Dataset:")
            print(missing_data_df)
        else:
            print("No datasets with missing data found.")

