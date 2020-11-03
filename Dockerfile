FROM python:3.7

# copy contents of project into docker
COPY ./ /app/

# Install repostatus
RUN cd app && python setup.py install

# Install dependencies
RUN cd app/web && pip install -r requirements.txt

# Install uvicorn
RUN pip install uvicorn

WORKDIR app/web/
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5055", "--access-log"]