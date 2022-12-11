FROM python:3.8-slim
RUN pip install streamlit
COPY ./app.py /app/app.py
COPY ./model /app/model
WORKDIR /app
EXPOSE 80
RUN streamlit run app.py --server.port 80