# About BoxScoreARC
This code is source of the application that provide NBA game's **Box Score in Arbitrary Range of game Clock**.  
User can specify any start and end point of the game clock and display the box score between them.  

# OSS
client: Vue (typescript)  
backend server: Django (python)  
database: Clickhouse

# Build
### for production
1. create env file `client/env.development` and add following text in the file.
   ```
   VUE_APP_API_BASE_URL=http://<<your host name>>:1026/api
   ```
1. Run following commands in Docker environment  
    ```sh
    docker compose --profile prod up --build -d
    ```
### for development
1. if build in linux envivonment, you need to run following command before docker compose up.  
    ```sh
    chmod +x ./server/entrypoint.sh
    ```
1. Run following commands in Docker environment  
    ```sh
    docker compose --profile dev up --build -d
    ```

if edit source code, recomend to do following step (it's for vscode in windows, so please read according to your environment. ).  
1. Open folder BoxScoreArc in vscode
1. Open new terminal in vscode
1. Run following commands to install packages for client 
    ```sh
    cd .\client\
    npm install
    cd ..
    ```
1. Run following commands to install packages for server 
    ```sh
    cd .\server\
    py -m venv env
    .\env\Scripts\Activate.ps1
    pip install --no-cache-dir -r .\requirements.txt
    deactivate
    cd ..
    ```
1. enable virtual environment python packages in vscode
    1. `Ctrl+Shift+P` and click `Python: Select Interpreter`
    1. select `Python <<version>> ('env': venv) .\server\env\Scripts\python.exe`
    1. restart vscode
