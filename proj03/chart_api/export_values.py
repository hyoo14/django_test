import pandas as pd
import json

def export_value(file_path):
    #authors = pd.read_excel("맘스터치권한세팅.xlsx")
    authors = pd.read_excel(file_path)
    #print(authors)
    # 판다스가 컬럼 읽어오면서 머지된 컬럼의 벨류들을 읽어오지 못 함.. 그래서 각각 row 1, 2, 3에서 머지되지 않고 벨류가 비어버린 컬럼 채워주는 과정
    # 그룹 컬럼 머지 반영 (row = 1)
    for i in range(1, authors.shape[1]): #time complexity O(col)
        if pd.isna(authors.iloc[1, i]) and pd.notna(authors.iloc[1, i - 1]):
            authors.iloc[1, i] = authors.iloc[1, i - 1]

    # 세부그룹 컬럼 머지 반영 (row = 2)
    for i in range(1, authors.shape[1]):
        if pd.isna(authors.iloc[2, i]) and pd.notna(authors.iloc[2, i - 1]):
            authors.iloc[2, i] = authors.iloc[2, i - 1]

    # 직책 컬럼 머지 반영 (row = 3)
    for i in range(1, authors.shape[1]):
        if pd.isna(authors.iloc[3, i]) and pd.notna(authors.iloc[3, i - 1]):
            authors.iloc[3, i] = authors.iloc[3, i - 1]

    # 그룹.세부그룹.직책으로 직책명 업데이트
    for i in range(6, authors.shape[1]):
        authors.iloc[3, i] = authors.iloc[1, i] + "." + authors.iloc[2, i] + "." + authors.iloc[3, i]

    ## 출력값 딕셔너리 생성
    # no_author_dict = {}
    # for col in range(6, authors.shape[1]): #time complexity( O( col * row ) )
    #     no_author_dict[authors.iloc[3, col]] = []
    #     for row in range(4, len(authors)):
    #         if authors.iloc[row, col] != 'O':
    #             no_author_dict[authors.iloc[3, col]].append(authors.iloc[row, 3])

    authors = authors.drop(authors.index[0:3])

    # 출력값 딕션어리 생성
    no_author_dict = {}
    for col in range(6, authors.shape[1]):
        no_author_dict[authors.iloc[0, col]] = authors[authors.iloc[:, col].isna()].iloc[:, 3].tolist()

    ## 직전 코드 설명 ##
    # authors.drop(authors.index[0:3]) #drop(0), drop(1), drop(2)를 한줄로 축약(NaN찾기 위해 앞의 0,1,2 row(NaN많은 row)지움)

    # authors.iloc[:, col].isna()     #col(숫자)번째 컬럼중에서 NaN(Not a Number)인 경우 true.
    # authors[  ]                     #위의 true인 경우 row들 집합
    # .iloc[:, 3]                     #중에서 3번째 컬럼(권한 코드명)
    # .tolist()                       #들을 list로 만듬

    # json 변환 위한 dict생성
    return_dict = {}
    return_dict["settings"] = []

    for key in no_author_dict.keys():
        element_dict = {}
        element_dict["group"] = key
        element_dict["blockings"] = no_author_dict[key]

        return_dict["settings"].append(element_dict)

    #print(return_dict)
    #return return_dict
    return json.dumps(return_dict)


if __name__ == "__main__":
    #커맨드 라인에서 추가로 입력받는 방법
    #file_path = input()

    #실행할 때 바로 받아오는(가져오는) 방법
    import sys
    file_path = sys.argv[1]
    print(file_path)
    print( export_value(file_path) )