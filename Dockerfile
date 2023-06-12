FROM node:14-alpine as builder

# install and cache app dependencies
COPY front/package.json front/package-lock.json ./
RUN npm install --only=prod&& mkdir /react-frontend && mv ./node_modules ./react-frontend

WORKDIR /react-frontend

COPY front/ .

RUN npm run-script build

# ------------------------------------------------------
# Production Build
# ------------------------------------------------------
FROM nginx:1.16.0-alpine
COPY --from=builder /react-frontend/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
