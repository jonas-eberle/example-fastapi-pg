FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install databases[postgresql]
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
