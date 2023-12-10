# Use an official PHP image as the base image with the desired version
FROM php:7.4.33-apache

# Set the working directory to /var/www/html
WORKDIR /var/www/html

# Copy your PHP files into the container
COPY chall.php /var/www/html/

# Optionally, you can copy other necessary files
COPY flag.txt /var/www/html/

# The following line is optional and can be used to install additional PHP extensions
# RUN docker-php-ext-install <extension_name>

# The CMD instruction provides the default command to run on container start
CMD ["apache2-foreground"]
