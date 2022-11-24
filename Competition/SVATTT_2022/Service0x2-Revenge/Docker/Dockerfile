FROM ubuntu:focal

RUN apt-get update && \
	apt-get install -y socat && \
	apt-get clean && \
	useradd -m user

ADD share/ /home/user/
ADD glibc/libc-2.31.so /usr/lib/x86_64-linux-gnu/libc.so.6
ADD glibc/ld-2.31.so /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2

RUN chown -R user:user /home/user && \
	chmod +x /home/user/*

USER user
WORKDIR /home/user

ENTRYPOINT ["/home/user/run.sh"]