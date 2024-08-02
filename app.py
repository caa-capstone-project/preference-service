from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace 'your-region' with your actual region
table = dynamodb.Table('Preferences')

@app.route('/preference', methods=['POST'])
def store_preference():
    try:
        data = request.get_json()
        print("Request: ", data)   
        user_id = data.get('userId')
        genres = data.get('genres')
        if not user_id or not genres:
            return jsonify({'error': 'Missing userId or genres'}), 400

        # Put item into DynamoDB table
        table.put_item(
            Item={
                'userId': user_id,
                'Genres': genres
            }
        )

        return jsonify({'message': 'Preference stored successfully'}), 200

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not found'}), 500
    except PartialCredentialsError:
        return jsonify({'error': 'Incomplete AWS credentials'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/preference/<string:userId>', methods=['GET'])
def get_preference(userId):
    try:
        userId = int(userId)  # Convert userId to a number

        response = table.get_item(
            Key={
                'userId': userId
            }
        )
        
        if 'Item' in response:
            return jsonify(response['Item']), 200
        else:
            return jsonify({'message': 'Preference not found'}), 404

    except ValueError:
        return jsonify({'error': 'Invalid userId format'}), 400
    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not found'}), 500
    except PartialCredentialsError:
        return jsonify({'error': 'Incomplete AWS credentials'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4202)
