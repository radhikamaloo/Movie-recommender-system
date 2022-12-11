FROM python:3.8-slim
RUN python -m venv .venv
RUN .venv/bin/pip install streamlit
COPY ./app.py /app/app.py
COPY ./model /app/model
WORKDIR /app
EXPOSE 8501
CMD streamlit run app.py