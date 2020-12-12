To build this microservice pipleline for nlp processing of emails git clone this repo, cd into the repo, then run:

```
docker-compose up -d --build
```


Once all microservices have booted, the service can be tested with:

```
sh local_test/predict.sh data/payload_oil_and_gas.json
sh local_test/predict.sh data/payload_not_oil_and_gas.json
```


To spin up a jupyter notebook for development in one of the microservices container environments, first cd into the microservice directory, then run:

```
docker build . -t temp_container
docker run -it -p 8888:8888 -v $(pwd):/home/microservice -v $(pwd)/../data:/home/microservice/data temp_container /bin/bash
pip install jupyter
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```

