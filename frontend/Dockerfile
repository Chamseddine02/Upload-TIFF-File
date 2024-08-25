# frontend/Dockerfile

FROM node:18

WORKDIR /app

COPY package.json ./

RUN yarn install

COPY . .

RUN yarn build

RUN yarn global add serve

EXPOSE 5000

CMD ["serve", "-s", "build", "-l", "5000"]

