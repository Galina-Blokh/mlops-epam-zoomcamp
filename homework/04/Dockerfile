FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip & pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN mkdir "output"

RUN pipenv install --system --deploy

COPY ["aws_cred.txt", "aws_cred.txt"]

COPY [ "python_script.py", "python_script.py" ]

ENTRYPOINT [ "python", "python_script.py" ]