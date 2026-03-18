# Build stage
FROM node:24-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build (no build-time args needed anymore)
RUN npm run build

# Runtime stage
FROM node:24-alpine

WORKDIR /app

# Install simple http server
RUN npm install -g serve

# Copy built assets from builder
COPY --from=builder /app/dist ./dist

# Copy entrypoint script
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 3000

# Start server with entrypoint
CMD ["./entrypoint.sh"]
