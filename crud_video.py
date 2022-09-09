import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from decimal import Decimal

# INPUT: 
# OUTPUT: 

def insert_video(number, duracao, data, id_local, nome_local, nome_arquivo, url, analisado=None, produtos=None, valor_total=None, perfil=None, genero=None, tipo_furto=None, recorrente=None, obs=None, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            #'dynamodb', endpoint_url="http://localhost:8000")
            'dynamodb', region_name="us-east-1") # mudar para sao paulo
 
    table = dynamodb.Table('FlaggedVideos')
    response = table.put_item(
        Item={
            'index_id': number,
            'duracao': duracao,
            'data': data,
            'id_local': id_local, # ainda precisa ser incluido na rotina de automacao
            'nome_local': nome_local,
            'nome_arquivo': nome_arquivo,
            'url': url,
            'analisado': analisado,
            'produtos': produtos,
            'valor_total': valor_total,
            'perfil': perfil,
            'genero': genero,
            'tipo_furto': tipo_furto,
            'recorrente': recorrente,
            'obs': obs, 
        }
    )
    return response
'''
# deletar video no db (MUDAR DE USUARIO PARA VIDEO)
def delete_user(name, occupation, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            #'dynamodb', endpoint_url="http://localhost:8000")
            'dynamodb', region_name="us-east-1")
 
    table = dynamodb.Table('Users')
 
    try:
        response = table.delete_item(
            Key={
                'name': name,
                'occupation': occupation
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

# modificar video no db (MUDAR DE USUARIO PARA VIDEO)
def update_user(name, occupation, hobby, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            #'dynamodb', endpoint_url="http://localhost:8000")
            'dynamodb', region_name="us-east-1")
 
    table = dynamodb.Table('Users')
 
    response = table.update_item(
        Key={
            'name': name,
            'occupation': occupation
        },
        UpdateExpression="set hobby=:h",
        ExpressionAttributeValues={
            ':h': hobby
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

    # consultar um video no db (MUDAR DE USUARIO PARA VIDEO)
    def get_user(name, occupation, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            #'dynamodb', endpoint_url="http://localhost:8000")
            'dynamodb', region_name="us-east-1")
 
    table = dynamodb.Table('Users')
 
    try:
        response = table.get_item(Key={'name': name, 'occupation': occupation})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']'''

if __name__ == '__main__':

    # inserir video no db
    '''video_resp = insert_video("1", "ponto xyz", "21/03/2022", "17h49", "34", "video_exemplo_1234.avi")
    print("Insert video succeeded:")
    pprint(video_resp, sort_dicts=False)'''

    # deletar video no db (MUDAR DE USUARIO PARA VIDEO)
    '''delete_response = delete_user("Thamires", "Student")
    if delete_response:
        print("Delete user succeeded:")
        pprint(delete_response, sort_dicts=False)'''

    # modificar video no db (MUDAR DE USUARIO PARA VIDEO)
    '''update_response = update_user("Thamires", "Student", "Read books")
    print("Update user succeeded:")
    pprint(update_response, sort_dicts=False)'''

    # consultar
    '''user = get_user("Thamires", "Student")
    if user:
        print("Get user succeeded:")
        pprint(user, sort_dicts=False)'''
    pass