To build this microservice pipleline for nlp processing of emails run:

```
docker-compose up -d --build
```


Once all microservices have booted the service can be tested with:

```
sh local_test/predict.sh data/payload.json
```


To spin up a jupyter notebook for development in one of the microservices container environments, first cd into the microservice directory, then run:

```
docker build . -t tmp_container
docker run -it -p 8888:8888 -v $(pwd):/home/microservice -v $(pwd)/../data:/home/microservice/data tmp_container /bin/bash
pip install jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```

