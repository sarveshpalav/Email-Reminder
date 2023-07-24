# Use an official Node.js runtime as a base image with version 16
FROM node:16-alpine

#This command sets the working directory inside the Docker container to /app. The following commands will be executed relative to this directory.
WORKDIR /app
#This line sets an environment variable PATH inside the container. It adds the /app/node_modules/.bin directory to the front of the PATH, which allows any executable binaries installed in that directory to be executed directly without specifying their full path.
ENV PATH /app/node_modules/.bin:$PATH


#This command copies the package.json file from the local client directory (assuming it exists relative to the Dockerfile location) to the current working directory (/app) in the Docker container. The ./ denotes the current directory.
COPY client/package.json ./

RUN npm i -g react-scripts

#This command installs Node.js dependencies for the application inside the Docker container. 
RUN npm install

RUN npm update


RUN chmod a+x /app/node_modules/.bin/react-scripts


#The line COPY client/ ./ in the Dockerfile copies the entire contents of the client directory (assuming it exists relative to the Dockerfile location) into the current working directory (/app) inside the Docker container.
COPY client/ ./



# Expose the port your React app will run on (change it to your app's port if needed)
EXPOSE 3000

# Start the app using a production-ready web server
CMD ["npm", "start"]