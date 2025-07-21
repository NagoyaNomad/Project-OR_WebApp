# Pythonではじめる数理最適化、岩永 et,al、オーム社、2021
# Chap.6 Webアプリケーションの開発
# p.p.191-194 (4)数理モデルの実装〜(5)問題を解く

import pandas as pd
import pulp


## csvファイルの読込み。
# 学生データの読込み(pandas.DataFrame型)
students_df = pd.read_csv('resource/students.csv')
## 車データの読込み(pandas.DataFrame型)
cars_df = pd.read_csv('resource/cars.csv')


## 学生の乗車グループ分け問題（0-1整数計画問題）のインスタンス作成
prob = pulp.LpProblem('ClubCarProblem', pulp.LpMinimize)


## リスト
# 学生のリスト
list_students = students_df['student_id'].to_list()

# 車のリスト
list_cars = cars_df['car_id'].to_list()

# 学年のリスト
list_grade = [1, 2, 3, 4]

# 学生と車のペアリスト
list_have_car_students = [(student, car) for student in list_students for car in list_cars]

# 免許を持っている学生のリスト
list_have_license_students = students_df[students_df['license'] == 1]['student_id']

# 学年がgradeである学生のリスト
list_students_in_grade = {grade: students_df[students_df['grade'] == grade]['student_id'] for grade in list_grade}

# 男性と女性のリスト
list_male_students = students_df[students_df['gender'] == 0]['student_id']
list_female_students = students_df[students_df['gender'] == 1]['student_id']


## 定数
# 車の乗車定員
capacity_of_car = cars_df['capacity'].to_list()


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


if __name__ == "__main__":
    # 求解のテスト
    def test_problem():
        '''
        実際の最適化を行う函数（最適化ソルバを使う）
        '''
        status = prob.solve()
        return pulp.LpStatus[status]


    # 結果表示を行う函数
    def set_result_to_dict() -> dict:
        '''
        各車に割り当てられている学生のリストを辞書に格納する（車ID → 割り当てられた学生のリスト）
        parameter:
            None:
        return:
            辞書:
                キー：車ID (int)
                バリュ：乗車する学生リスト：list(int)
        '''
        assign_each_student_a_car = {car: [student for student in list_students if x[student, car].value() == 1] for car in list_cars}

        return assign_each_student_a_car

    def output_capacity_of_car() -> dict:
        '''
        各車の乗車定員を辞書として返す函数
        parameter:
            None:
        return:
            dict:
                key (int): 車ID
                value (int): 乗車定員
        '''
        return dict(zip(cars_df['car_id'], cars_df['capacity']))


    # メインルーチン
    result_status = test_problem()
    print(f'Status: {result_status}')

    # 最適化結果の表示
    if result_status == 'Optimal':
        max_people = output_capacity_of_car()

        for car, number in set_result_to_dict().items():
            print(f'車ID: {car}')
            print(f'学生数(乗車定員): {len(number)}({max_people[car]})')
            print(f'乗車メンバ: {number}')
            print()

