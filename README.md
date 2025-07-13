# About BoxScoreARC
This code is source of the application that provide NBA game's **Box Score in Arbitrary Range of game Clock**.  
User can specify any start and end point of the game clock and display the box score between them.  

# OSS
client: Vue (typescript)  
backend server: Django (python)  
database: PostgreSQL

# Build
### preparation
※ it's for windows, so please read according to your environment.  
1. If you need, put certificate in `traefik/certs`. default is self-signed certificate configured with `traefik/certs/openssl.cnf`.
    * Put SSL/TLS certificate issued by CA
    * Put your own self-signed certificate
        1. Edit `traefik/certs/openssl.cnf`
        1. Run following commands in Docker environment
            ```sh
            docker run --rm `
              -v "${PWD}/traefik/certs:/etc/traefik/certs" `
              alpine:latest `
              sh -c "apk add --no-cache openssl && \
                     openssl req -x509 -nodes -days 365 \
                       -newkey rsa:2048 \
                       -keyout /etc/traefik/certs/self.key \
                       -out /etc/traefik/certs/self.crt \
                       -config /etc/traefik/certs/openssl.cnf"
            ```
### for production
1. Run following commands in Docker environment  
    ```sh
    docker compose --profile prod up --build -d
    ```
### for development
※ it's for vscode in windows, so please read according to your environment.  
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
1. Run following commands in Docker environment  
    ```sh
    docker compose --profile dev up --build -d
    ```
