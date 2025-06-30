FROM apache/superset:latest

COPY superset_config.py /app/pythonpath/
COPY dashboards/dashboard_export_20250630T172417.zip /app/dashboards/

USER root
RUN apt-get update && \
    apt-get install -y jq curl && \
    rm -rf /var/lib/apt/lists/*

USER superset
RUN pip install psycopg2-binary

# Create an entrypoint script
USER root
RUN echo '#!/bin/bash\n\
superset fab create-admin \
    --username "$ADMIN_USERNAME" \
    --firstname Superset \
    --lastname Admin \
    --email "$ADMIN_EMAIL" \
    --password "$ADMIN_PASSWORD"\n\
superset db upgrade\n\
superset superset init\n\
/usr/bin/run-server.sh' > /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

USER superset
ENTRYPOINT ["/app/docker-entrypoint.sh"]