## PythonからAPIを利用するプログラム

import requests


# APIのエンドポイント
url = 'http://127.0.0.1:5000/api'

# リクエストで渡すデータ
send_files = {
    'students': open('resource/students.csv', 'r'),
    'cars': open('resource/cars.csv', 'r'),
}

# POSTリクエスト
response = requests.post(url, files = send_files)

# 結果の保存(`requests.text`でレスポンス内容にアクセス可能)
with open('resource/solution_requests.csv', 'w') as response_file:
    response_file.write(response.text)
