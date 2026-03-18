FROM python:3.11-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY flaskr ./flaskr
COPY entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set Flask app
ENV FLASK_APP=flaskr
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run entrypoint script
CMD ["./entrypoint.sh"]
