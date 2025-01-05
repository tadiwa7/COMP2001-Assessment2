# Use the official Python 3.9 slim image as the base image
FROM python:3.9-slim

# Set environment variable for Microsoft ODBC drivers
ENV ACCEPT_EULA=Y

# Update package list and install necessary dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    gnupg \
    unixodbc-dev

# Add Microsoft ODBC drivers and tools
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends --allow-unauthenticated \
    msodbcsql17 \
    mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Copy all files from the current directory to the container
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies from the requirements.txt file
RUN pip install -r requirements.txt

# Clean up unnecessary files to reduce image size
RUN apt-get -y clean

# Expose the port on which your app runs
EXPOSE 8080

# Set the default command to run your Flask app
CMD ["python", "app.py"]
