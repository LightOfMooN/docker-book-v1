FROM node:14-alpine
WORKDIR /app
EXPOSE 3000
ENV CI=true
COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
