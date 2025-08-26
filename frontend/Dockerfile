# Next.js frontend Dockerfile

FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Next.js 개발 서버 실행 (개발용)
CMD ["npm", "run", "dev"]