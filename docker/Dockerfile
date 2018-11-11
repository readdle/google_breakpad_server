# Use an official Python runtime as a parent image
FROM ubuntu

RUN apt-get update && \
 	apt-get install -y git && \
 	apt-get install -y build-essential && \
	apt-get install -y python && \
	apt-get install -y curl


RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

ENV PATH="/depot_tools:${PATH}"	


RUN \
	mkdir breakpad && cd breakpad && \
	fetch breakpad && \
	cd src && \
	./configure && make && \
	make install



# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app


# Install app
RUN git clone https://github.com/albertaleksieiev/google_breakpad_server
RUN cd google_breakpad_server && git pull

# Run app.py when the container launches
CMD ["python", "google_breakpad_server/server.py","8003"]
