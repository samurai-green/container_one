FROM alpine:3.14

RUN apk add python3 py3-pip

RUN addgroup -S ghost && adduser -S ghost -G ghost
#RUN groupadd ghost && useradd ghost -g ghost -G ghost

USER ghost

WORKDIR /home/ghost/app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "app.py" ]
