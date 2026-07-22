FROM python:alpine

RUN pip install --upgrade pip

RUN adduser -D -u 1010 worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker run.py .
COPY --chown=worker:worker requirements.txt .

RUN pip install --user -r requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker ./app app
CMD ["python", "run.py"]