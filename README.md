# About BoxScoreARC
This code is source of the application that provide NBA game's Box Score in Arbitrary Range of game Clock.  
User can specify any start and end point of the game clock and display the box score between them.  

# OSS
client: Vue (typescript)  
backend server: Django (python)  
database: Clickhouse

# Build
### for production
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
