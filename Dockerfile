FROM public.ecr.aws/lambda/python:3.12

ARG ULTRA13_RUNTIME_WHEEL_URL=https://d2w1trq68wilo3.cloudfront.net/downloads/2385ff80af1b02749238cc250d1b21022ebe3385deae1bc4ecb4e02d83412f9b/ultra13_runtime-1.0.0-py3-none-any.whl
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN python -m pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt "${ULTRA13_RUNTIME_WHEEL_URL}"
COPY agent.py handler.py ${LAMBDA_TASK_ROOT}/
CMD ["handler.lambda_handler"]

