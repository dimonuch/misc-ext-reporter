FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pandas \
#   we can't leave without you, dear less!    
    less \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /misc-ext-reporter

CMD ["/bin/bash"]