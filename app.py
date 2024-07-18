from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace 'your-region' with your actual region
table = dynamodb.Table('Preferences')

@app.route('/store_preference', methods=['POST'])
def store_preference():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        genres = data.get('Genres')
        tags = data.get('Tags')
        print(user_id, genres, tags)
        if not user_id or not genres or not tags:
            return jsonify({'error': 'Missing userId, Genres or Tags'}), 400

        # Put item into DynamoDB table
        table.put_item(
            Item={
                'userId': user_id,
                'Genres': set(genres),
                'Tags': set(tags)
            }
        )

        return jsonify({'message': 'Preference stored successfully'}), 200

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not found'}), 500
    except PartialCredentialsError:
        return jsonify({'error': 'Incomplete AWS credentials'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4202)
