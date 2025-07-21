## 6.3(3) pp.202-205 Flaskを用いたAPIの実装

# ライブラリのインポート
from flask import Flask
from flask import request

from problem import CarGroupProblem


# Flaskのアプリケーション（インスタンス）を作成する。
app = Flask(__name__)

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
