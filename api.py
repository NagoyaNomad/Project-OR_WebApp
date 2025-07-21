## 6.3(3) pp.202-205 Flaskを用いたAPIの実装

# ライブラリのインポート
import pandas as pd

from flask import Flask
from flask import request
from flask import make_response

from problem import CarGroupProblem


# Flaskのアプリケーション（インスタンス）を作成する。
app = Flask(__name__)

def preprocess(request):
    '''
    リクエストデータを受け取り、データフレームに変換する函数
    parameter:
        flask.request:
    return:
        (pandas.DataFrame): 生徒のデータフレームと車のデータフレーム
    '''
    # 各ファイルを取得する。
    students = request.files['students']
    cars = request.files['cars']

    # pandasで読み込む。
    students_df = pd.read_csv(students)
    cars_df = pd.read_csv(cars)

    return students_df, cars_df

def postprocess(solution_df):
    '''
    データフレームをcsvに変換する函数
    parameter:
        solution_df (pandas.DataFrame): データフレーム形式の最適化結果
    return:
        (Flask.responce): クライアント側に返すレスポンスデータ(csvファイル)
    '''
    solution_csv = solution_df.to_csv(index = False)

    response = make_response()

    response.data = solution_csv
    response.headers['Content-Type'] = 'text/csv'

    return response


# 最適化問題を解くAPI用の函数
@app.route('/api', methods = ['POST'])
def solve():
    # 1. リクエスト受信
    students_df, cars_df = preprocess(request)

    # 2. 最適化実行
    solution_df = CarGroupProblem(students_df, cars_df).solve()

    # 3. レスポンス返送
    response = postprocess(solution_df)
    return response
