# Use a specific version, and let Docker detect the architecture
FROM node:22-bullseye-slim AS builder

# Set the working directory (This creates /app)
WORKDIR /app

# Copy ONLY package files to cache the 'npm install' layer
COPY package*.json ./

# Clean cache and install (Agnostic to host OS)
RUN npm cache clean --force && npm install --no-audit --no-fund --loglevel=error

# Now copy the rest of the code
COPY . .
RUN npm run build

# Final Stage: Serve the static React files with Nginx
FROM nginx:alpine
# VITE builds to 'dist', not 'build'
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]