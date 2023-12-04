FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY application.py requirements.txt /app/
COPY resources/ /app/resources/
RUN mv application.py main.py
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80


# sudo docker build -t python_flask_restful_docker_image .
# sudo docker run --rm -it -p 80:80 --name python_flask_restful_docker_container python_flask_restful_docker_image
# sudo docker run --rm -d  -p 80:80 --name python_flask_restful_docker_container python_flask_restful_docker_image
# docker exec -it python_flask_restful_docker_container sh

# docker images
# docker rmi <IMAGE>
# docker rm <CONTAINER>
# docker container prune

# docker ps -a

# docker save -o python_flask_restful_docker_image.tar python_flask_restful_docker_image
# docker load -i python_flask_restful_docker_image.tar


# create an EC2 linux 2 instance on AWS
# ssh -i .ssh/agmsulutions.pem ec2-user@ec2-54-167-40-40.compute-1.amazonaws.com
# sudo yum update -y
# sudo amazon-linux-extras install docker
# sudo service docker start
# mkdir downloads
# cd downloads

# in python app terminal 
# scp -i /Users/salmanmajidi/.ssh/agmsulutions.pem -r Dockerfile application.py requirements.txt resources ec2-user@ec2-54-167-40-40.compute-1.amazonaws.com:/home/ec2-user/downloads


# sudo certbot -n -d ec2-54-167-40-40.compute-1.amazonaws.com --nginx --agree-tos --email geeekfa@gmail.com


