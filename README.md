# About ClockludeBoxScore
This code is source of the application that provide NBA game's box score with game clock.  
User can specify any start and end point of the game clock and display the box score between them.  

# OSS
client: Vue (typescript)  
backend server: Django (python)  
database: Clickhouse

# Build
Run following commands in Docker environment  
### for production
`docker compose --profile prod up --build -d`
### for development
`docker compose --profile dev up --build -d`
