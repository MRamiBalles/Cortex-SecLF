FROM node:20-alpine

WORKDIR /app

# Install dependencies (will benefit from caching)
COPY package.json package-lock.json* ./

# If package-lock.json doesn't exist yet (initial setup), this might fail or warn, 
# but we will run npm install inside the container or volume mount mainly in dev.
# For production build properly. For dev, we rely on volume mount mostly.
RUN npm install

# Copy source
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
