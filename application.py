from flask import Flask, render_template, request
from botocore.exceptions import ClientError
import uuid
import boto3
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

application = Flask(__name__, template_folder='templates')

# Configurar boto3 para se conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('DBTable')

@application.route('/', methods=['GET', 'POST'])
def form():
    name = None
    faltas = None
    all_entries = []

    if request.method == 'POST':
        name = request.form.get('name')
        faltas = request.form.get('faltas')

        # Gerar um UUID para o item
        item_id = str(uuid.uuid4())

        # Inserir os dados no DynamoDB
        try:
            table.put_item(
                Item={
                    'id': item_id,
                    'name': name,
                    'faltas': faltas
                }
            )
            logging.info("Dados inseridos com sucesso no DynamoDB")
        except ClientError as e:
            logging.error(e)
            return "Erro ao inserir dados no DynamoDB", 500

    # Recuperar todos os dados do DynamoDB para exibição
    try:
        response = table.scan()
        all_entries = response.get('Items', [])
    except ClientError as e:
        logging.error(e)
        return "Erro ao recuperar dados do DynamoDB", 500

    return render_template('form.html', name=name, faltas=faltas, entries=all_entries)

if __name__ == '__main__':
    application.run(debug=True, port=80, host='0.0.0.0')
