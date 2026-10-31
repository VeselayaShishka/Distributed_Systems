# The base image supplies Python and a small Linux user space.
FROM python:3.13.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy dependencies first: changing app.py need not reinstall them.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Run the service as a dedicated, non-root user.
RUN useradd --create-home --shell /usr/sbin/nologin appuser
COPY --chown=appuser:appuser app.py stories.py ./
USER appuser

# Documentation of the listening port; docker run -p publishes it.
EXPOSE 5000

# One process, one application thread: our dictionary is process-local state.
# 0.0.0.0 accepts traffic arriving through the container's network interface.
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--threads=1", "app:app"]
