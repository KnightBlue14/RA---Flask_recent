FROM python
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD ret_auth.py /
ADD tasks.py /
ADD server.py /
EXPOSE 5000
ENV PYTHONUNBUFFERED=1
CMD ["python","./server.py"]