# Pythonではじめる数理最適化、岩永 et,al、オーム社、2021
# Chap.6 Webアプリケーションの開発
# pp. 196-201 6.3(2) 数理モデルのモジュール化

# 単体のプログラム(modeling.py)をクラス化する。
# Copyright: Kamio Hiroshi (2025)

# モジュール problem.py
import pandas as pd
import pulp


class CarGroupProblem():
    '''
    学生の乗車グループ分け問題を解く数理モデルのPythonクラス
    '''
    def __init__(self, students_df, cars_df, name = 'ClubCarProblem'):
        # 初期化メソッド
        self.students_df = students_df
        self.cars_df = cars_df
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        ## 学生の乗車グループ分け問題（0-1整数計画問題）のインスタンス作成
        prob = pulp.LpProblem(self.name, pulp.LpMinimize)


        ## リスト
        # 学生のリスト
        list_students = self.students_df['student_id'].to_list()

        # 車のリスト
        list_cars = self.cars_df['car_id'].to_list()

        # 学年のリスト
        list_grade = [1, 2, 3, 4]

        # 学生と車のペアリスト
        list_have_car_students = [(student, car) for student in list_students for car in list_cars]

        # 免許を持っている学生のリスト
        list_have_license_students = self.students_df[self.students_df['license'] == 1]['student_id']

        # 学年がgradeである学生のリスト
        list_students_in_grade = {grade: self.students_df[self.students_df['grade'] == grade]['student_id'] for grade in list_grade}

        # 男性と女性のリスト
        list_male_students = self.students_df[self.students_df['gender'] == 0]['student_id']
        list_female_students = self.students_df[self.students_df['gender'] == 1]['student_id']


        ## 定数
        # 車の乗車定員
        capacity_of_car = self.cars_df['capacity'].to_list()


        ## 変数
        # 学生をどの車に割り当てるかを変数とする。
        x = pulp.LpVariable.dicts('x', list_have_car_students, cat = 'Binary')

        ## 制約条件
        # 1) 各学生を１つの車に割り当てる。
        for student in list_students:
            prob += pulp.lpSum([x[student, car] for car in list_cars]) == 1

        # 2) 法規制に関する制約：各車には乗車定員より多く乗ることはできない。
        for car in list_cars:
            prob += pulp.lpSum([x[student, car] for student in list_students]) <= capacity_of_car[car]

        # 3) 法規制に関する制約：各車にドライバとして運転免許証を保持している者を１人以上割り当てる。
        for car in list_cars:
            prob += pulp.lpSum([x[student, car] for student in list_have_license_students]) >= 1

        # 4) 懇親を目的とした制約：各車に各学年の学生を１人以上割り当てる。
        for car in list_cars:
            for grade in list_grade:
                prob += pulp.lpSum([x[student, car] for student in list_students_in_grade[grade]]) >= 1

        # 5)ジェンダーバランスを考慮した制約：各車に男性を１人以上割り当てる。
        for car in list_cars:
            prob += pulp.lpSum([x[student, car] for student in list_male_students]) >= 1

        # 6)ジェンダーバランスを考慮した制約：各車に女性を１人以上割り当てる。
        for car in list_cars:
            prob += pulp.lpSum([x[student, car] for student in list_female_students]) >= 1

        # 最適化後に利用するデータを返却する。
        return {
                'prob': prob,
                'variable': {'x': x},
                'list': {
                    'students': list_students,
                    'cars': list_cars,
                    },
               }

    def solve(self):
        '''
        最適化問題を解くメソッド
        '''
        ## 問題を解く。
        # self.prob['prob']がpulpモジュールのprobオブジェクト。
        # なので、ここでのsolveはprobオブジェクトのメソッド。
        status = self.prob['prob'].solve()

        ## 最適化結果を格納する。
        x = self.prob['variable']['x']
        list_students = self.prob['list']['students']
        list_cars = self.prob['list']['cars']

        car2students = {car: [student for student in list_students if x[student, car].value() == 1] for car in list_cars}

        student2car = {student: car for car , ss in car2students.items() for student in ss}

        solution_df = pd.DataFrame(list(student2car.items()), columns = ['student_id', 'car_id'])

        return solution_df


if __name__ == "__main__":
    # データの読み込み
    students_df = pd.read_csv('resource/students.csv')
    cars_df = pd.read_csv('resource/cars.csv')

    # 数理モデル　インスタンスの作成
    prob = CarGroupProblem(students_df, cars_df)

    # 問題を解く
    solution_df = prob.solve()

    # 結果の表示
    print(f'Solution: \n {solution_df}')
