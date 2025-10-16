# Etapa de construcción - Usar Node.js 20 (LTS)
FROM node:20-alpine as build

WORKDIR /app

# Copiar package.json e instalar dependencias
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# Copiar código fuente y construir
COPY . .
RUN npm run build -- --configuration=production

# Etapa de producción
FROM nginx:alpine

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar build de Angular (nuevo output Angular 17+)
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]