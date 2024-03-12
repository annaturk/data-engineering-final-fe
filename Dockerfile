# Use an official Python runtime as a parent image
FROM python:3.7.7

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install streamlit psycopg2 pandas plotly prophet matplotlib

# Expose the port that Streamlit runs on by default
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "frontend.py"]
