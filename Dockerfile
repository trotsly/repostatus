FROM python:3.7

# copy contents of project into docker
COPY ./ /app/

# Install repostatus
RUN cd app && python setup.py install

# Install dependencies
RUN cd app/web && pip install -r requirements.txt

# Install uvicorn and other tools
RUN pip install uvicorn gunicorn uvloop httptools

WORKDIR /app/web/

CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5055", "--reload", "--workers=6", "-k", "uvicorn.workers.UvicornWorker" , "--access-logfile", "-"]