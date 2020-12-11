To spin up a jupyter notebook for development on of the container environments cd into the container:

```
docker build . -t tmp_container
docker run -it -p 8888:8888 -v $(pwd):/home/microservice -v $(pwd)/../data:/home/microservice/data tmp_container /bin/bash
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```