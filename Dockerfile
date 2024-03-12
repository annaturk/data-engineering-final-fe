# Use an official Python runtime as a parent image
FROM python:3.7.7

ENV PORT 8501
EXPOSE 8501
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install streamlit psycopg2 pandas plotly prophet matplotlib

CMD ["streamlit", "run", "frontend.py"]
