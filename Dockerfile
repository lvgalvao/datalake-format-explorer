FROM localstack/localstack

# Define a versão do LocalStack
ENV LOCALSTACK_VERSION=0.13.0.1

# Instala as ferramentas AWS CLI para interagir com o LocalStack (opcional)
RUN pip install awscli-local
