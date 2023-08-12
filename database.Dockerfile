# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Environment variables for PostgreSQL configuration
ENV POSTGRES_DB email_reminder_db
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin

# Expose the default PostgreSQL port
EXPOSE 5432