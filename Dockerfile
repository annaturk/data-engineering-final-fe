# Use an official Python runtime as a parent image
FROM python:3.8-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on by default
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "frontend.py"]
