FROM python:3

LABEL Author="Sallahuddin"

ENV PYTHONBUFFERED 1
#Making the working directory for project
RUN mkdir /ecommerceproj
WORKDIR /ecommerceproj
#Copying project to the working directory
COPY ./ecommerceproj /ecommerceproj
#Copying and running the requirements file
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#Copying and modifying permissions of shell script
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /ecommerceproj/entrypoint.sh
RUN chmod +x /ecommerceproj/entrypoint.sh
#Running shell script
ENTRYPOINT ["/ecommerceproj/entrypoint.sh"]
