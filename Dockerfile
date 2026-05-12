FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

RUN chmod +x start.sh

CMD ["./start.sh"]
