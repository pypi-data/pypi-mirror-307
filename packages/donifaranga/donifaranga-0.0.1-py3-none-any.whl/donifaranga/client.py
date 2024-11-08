import pandas as pd
import numpy as np
from utils import load_dataset
import os
from  termcolor import colored
import sys
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import load_model
import joblib
import pickle
import requests


#------------------------------------------
def send_model_to_server(server_url,model_filename,model_file,data):
    with open(model_filename, 'rb') as model_file:
        filename = os.path.basename(model_filename)
        files = {'model': model_file}
        response = requests.post(server_url, files=files, data=data) #,stream=True)

        if response.status_code == 200 and response.headers.get('Content-Type') != 'application/json':
            extension = os.path.splitext(filename)[1]
            with open(os.path.join(source_models_path,'global_model'+extension),'wb') as gl_model:
                for chunck in response.iter_content(chunk_size=8192):
                    gl_model.write(chunck)
                print(colored(f"\t|>> Global model downloaded successfully !\n", 'green'))
        else:
            print(response.json())

#------------------------------------------
def train():
    
    agg_methods = {'1':"Federated Averaging (FedAvg)", '2':"Federated Matched Averaging (FedMA)", '3':"All Model Averaging (AMA)", '4': "One Model Selection (OMS)", '5':"Best Models Averaging (BMA)", '6': "FedProx", '7': "Hybrid Approaches"}
    models = {'1': 'Linear Regression Model', '2': 'Mutli-Layer Perceptron (MLP)', '3': 'Long-Short Term Memory (LSTM)'}
    all_models = { '1': LinearRegression(), '2': MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=500), '3': Sequential() }

    print("------------------------------------------")
    print(" MANUAL TRAINNING OF THE CLIENT MODEL")
    print("------------------------------------------")


    print('|> Before the traning please specify the central server full access url:')
    print('\n\t|>> ',end="")
    server_url = input("").strip().replace(' ', '')
    server_url = server_url if server_url != "" else "http://localhost:5000/api/receive_model"
    print(colored(f"\t|>>  {server_url}\n",'blue'))

    print('|> Your client ID:')
    print('\n\t|>> ',end="")
    client_id = input("").strip()
    client_id = 'Client-'+client_id if client_id != "" else "Client-01"
    print(colored(f"\t|>>  {client_id}\n",'blue'))

    print('|> Your client ID:')
    print('\n\t|>> ',end="")
    client_id = input("").strip()
    client_id = 'Client-'+client_id if client_id != "" else "Client-01"
    print(colored(f"\t|>>  {client_id}\n",'blue'))

    print('|> Please specify the type or categorie of the dataset to use (stock price data, feedback data,...):')
    print('--')
    for index,name in cats.items():
        print(index,". "+name)
    print('\n\t|>> ',end="")
    cat_index = input("").strip()
    cat = cats[cat_index] if cat_index in cats.keys() else "general"
    print(colored(f"\t|>> {cat}\n", 'blue'))

    print('|> Provide the full path to the dataset:')
    dataset_path = input("").strip()
    dataset_path = dataset_path if dataset_path != "" else "/home/donifaranga/datasets/default.csv"
    print(colored(f"\t|>>  {dataset_path}\n",'blue'))

    source_dataset = os.path.join(dataset_path,cat)

    model_extension = '.joblib'


    if not os.path.exists(source_dataset):
        os.makedirs(source_dataset)

    print('|> Select the a model for training:')
    print('--')
    for index,name in models.items():
        print(index,". "+name)
    print('\n\t|>> ',end="")
    model_index = input("").strip()
    model_index = model_index if model_index in models.keys() else "2"
    print(colored(f"\t|>> {models[model_index]}\n", 'blue'))

    print('|> Specify the full path where you want to save the trained model (the global model will be saved there too):')
    models_path = input("").strip()
    models_path = models_path if models_path != "" else "/home/donifaranga/models"
    print(colored(f"\t|>>  {models_path}\n",'blue'))

    source_models_path = os.path.join(models_path,cat)

    if not os.path.exists(source_models_path):
        os.makedirs(source_models_path)

    print('|> Select the federated learning aggregate method:')
    print('--')
    for index,name in agg_methods.items():
        print(index,". "+name)
    print('\n\t|>> ',end="")
    agg_index = input("").strip()
    agg_index = agg_index if agg_index in agg_methods.keys() else "1"
    print(colored(f"\t|>> {agg_methods[agg_index]}\n", 'blue'))

    print()


    try:

        dataframes = []

        for data_src in os.listdir(source_dataset):
            data_path = os.path.join(source_dataset,data_src)
            if data_src.startswith('.') == False and os.path.isfile(data_path):
                dataset = load_dataset(data_path)
                dataframes.append(dataset)

        dataset = pd.concat(dataframes, ignore_index=True)
        print(dataset)
        # print('\n|> Checking if there are too many missing values:')
        # print(dataset.isnull().sum())
        dataset.dropna(inplace=True)
        dataset.drop_duplicates(inplace=True)
        # dataset = dataset[(dataset[['Open', 'Close', 'High', 'Low', 'Volume']] >= 0).all(axis=1)]
        # dataset['Adj Close'] = dataset['Close'] * adjustment_factor

        # print('\n|> Filter out non-trading days:')
        # non_trading_days = dataset[dataset['Volume'] == 0]
        # print(non_trading_days)

        print()

        print('|> For the supervised learning please provide the target column correct name (as it appears in the dataset):')
        target_column = input("").strip()
        print(colored(f"\t|>>  {target_column}\n",'blue'))

        

        X = dataset.drop(target_column)
        y = dataset[target_column]

        scaler = MinMaxScaler(feature_range=(0, 1))
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))

        scaler_filename = os.path.join(source_models_path, 'scaler.joblib')
        joblib.dump(scaler, scaler_filename)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, shuffle=False)

        # -----------------
        # REGRESSION
        # -----------------
        if model_index == '1':
            print("|> [Training]: Regression model")
            regressor = all_models[model_index] #LinearRegression()
            regressor.fit(X_train, y_train)

            y_pred = regressor.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mean_actual = np.mean(y_test)
            accuracy = mse #(rmse / mean_actual) * 100 if mean_actual != 0 else mse
            print(colored(f'\t|>> Linear Regression MSE: {accuracy}','blue'))

            lr_model_filename = os.path.join(source_models_path,'linear_regression_model'+model_extension)

            data = {'cat': cat_index, 'id': client_id, 'filename': filename,'agg':agg_index,'model_type':model_index,'accuracy':accuracy}

            if lr_model_filename.endswith('.pkl'):
                with open(lr_model_filename, 'wb') as file:
                    pickle.dump(regressor, file)
                    send_model_to_server(server_url,lr_model_filename,regressor,data)
            elif lr_model_filename.endswith('.joblib'):
                joblib.dump(regressor, lr_model_filename)
                send_model_to_server(server_url,lr_model_filename,regressor,data)
            else:
                print(colored(f"|> Error: Failed to save the trained model",'red'))

        # -----------------
        # MLP
        # -----------------
        elif model_index == '2':
            print("|> [Training]: MLP model")
            mlp = all_models[model_index] #MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=500)
            mlp.fit(X_train, y_train.ravel())

            # Predict on the test set
            y_pred_mlp = mlp.predict(X_test)

            # Evaluate performance
            mse_mlp = mean_squared_error(y_test, y_pred_mlp)
            rmse = np.sqrt(mse_mlp)
            mean_actual = np.mean(y_test)
            accuracy = mse_mlp #(rmse / mean_actual) * 100 if mean_actual != 0 else mse_mlp
            print(colored(f'\t|>> Neural Network MLP MSE: {accuracy}','blue'))

            mlp_model_filename = os.path.join(source_models_path,'mlp_model'+model_extension)

            data = {'cat': cat_index, 'id': client_id, 'filename': filename,'agg':agg_index,'model_type':model_index,'accuracy':accuracy}

            if mlp_model_filename.endswith('.pkl'):
                with open(mlp_model_filename, 'wb') as file:
                    pickle.dump(mlp, file)
                    send_model_to_server(server_url,mlp_model_filename,mlp,data)
            elif mlp_model_filename.endswith('.joblib'):
                joblib.dump(mlp, mlp_model_filename)
                send_model_to_server(server_url,mlp_model_filename,mlp,data)
            else:
                print(colored(f"|> Error: Failed to save the trained model",'red'))



        # -----------------
        # LSTM
        # -----------------
        elif model_index == '3':
            print("|> [Training]: LSTM model")
            X_train_lstm = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
            X_test_lstm = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
            model = Sequential()

            # Add an LSTM layer with 50 units and a Dense output layer
            model.add(LSTM(units=50, return_sequences=False, input_shape=(1, X_train.shape[1])))
            model.add(Dense(1))

            # Compile the model
            model.compile(optimizer='adam', loss='mean_squared_error')

            all_models['3'] = model

            # Train the model
            model.fit(X_train_lstm, y_train, epochs=10, batch_size=32)

            # Predict on the test set
            y_pred_lstm = model.predict(X_test_lstm)

            # Evaluate performance
            mse_lstm = mean_squared_error(y_test, y_pred_lstm)
            rmse = np.sqrt(mse_lstm)
            mean_actual = np.mean(y_test)
            accuracy = mse_lstm #(rmse / mean_actual) * 100 if mean_actual != 0 else mse_lstm
            print(f'\tLSTM MSE: {accuracy}')

            lstm_model_filename = os.path.join(source_models_path,'lstm_model.keras')

            model.save(lstm_model_filename)

            data = {'cat': cat_index, 'id': client_id, 'filename': filename,'agg':agg_index,'model_type':model_index,'accuracy':accuracy}

            if lstm_model_filename.endswith('.pkl'):
                with open(lstm_model_filename, 'wb') as file:
                    pickle.dump(mlp, file)
                    send_model_to_server(server_url,lstm_model_filename,mlp,data)
            elif lstm_model_filename.endswith('.joblib'):
                joblib.dump(mlp, lstm_model_filename)
                send_model_to_server(server_url,lstm_model_filename,mlp,data)
            else:
                print(colored(f"|> Error: Failed to save the trained model",'red'))


        # dataset['Close'].plot()
        # plt.show()

    except Exception as e:
        print(colored(f"|> Error occured during the process: {e}",'red'))

    print('\n---------------[END]\n')




