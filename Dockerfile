FROM python:3

LABEL Author="Sallahuddin"

ENV PYTHONBUFFERED 1

RUN mkdir /ecommerceproj
WORKDIR /ecommerceproj

COPY ./ecommerceproj /ecommerceproj

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /ecommerceproj/entrypoint.sh
RUN chmod +x /ecommerceproj/entrypoint.sh

ENTRYPOINT ["/ecommerceproj/entrypoint.sh"]
