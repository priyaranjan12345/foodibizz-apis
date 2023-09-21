# foodibizz-apis
    - commands need to run the app

    - sudo docker compose up --build
    - sudo docker compose up // after added volumes
    - sudo docker build . // default
    - sudo docker build -t softdev678/foodibizz:1.0.0 . // softdev678 -> docker user name
    - sudo docker run -p 8000:8000 softdev678/foodibizz
    - sudo docker login
    - sudo docker push softdev678/foodibizz:1.0.0
    - sudo docker compose -f docker-compose.development.yaml --build
    - sudo docker compose -f docker-compose.production.yaml up --build -d
    - docker stop my_container // stop docker container
    - sudo docker ps // show all running dockers

# release 1.0
    create, update, delete and get Items
    generate order and store order items

