import pandas as pd

# 데이터 로딩
weighted_average_path = r'C:\Users\linva\Downloads\weighted_average_results.xlsx'  # 실제 파일 경로로 수정
weights_path = r'C:\Users\linva\Downloads\남성 가중치.xlsx'  # 실제 파일 경로로 수정

weighted_average_data = pd.read_excel(weighted_average_path, index_col=0)

# 남성 가중치 정의
weights_dict = {
    "보험": 8.6, "지갑": 0.5, "우산": 0.2, "가방": 2.7, "시계": 0.6, "휴지": 1.3, "샴푸": 1, "비누": 0.3, "치약": 0.9, 
    "이발": 0.3, "기숙사": 0.9, "도시락": 0.6, "소주": 4.2, "맥주": 7.8, "막걸리": 0.8, "커피": 8.8, "쌀국수": 0.6, 
    "피자": 4.1, "햄버거": 4.3, "치킨": 8.6, "떡볶이": 3.1, "김밥": 3.4, "라면": 3.1, "스파게티": 1.5, "돈까스": 2.2, 
    "볶음밥": 0.9, "탕수육": 2.1, "짜장면": 2.2, "짬뽕": 2.4, "초밥": 2.7, "칼국수": 2.7, "냉면": 2.4, "돼지갈비": 6.1, 
    "삼겹살": 17, "불고기": 1.1, "등록금": 10, "ott": 8, "스터디카페": 0.8, "pc방": 0.3, "노래방": 0.5, "당구장": 0.5, 
    "컴퓨터": 3, "tv": 1.9, "스마트폰": 10.4, "버스": 7.8, "지하철": 3.9, "자전거": 0.5, "병원비": 20.5, "마스크": 1.6, 
    "약국": 5.8, "선풍기": 0.4, "에어컨": 1.5, "냉장고": 2.4, "난방비": 1.6, "도시가스": 11.5, "관리비": 21.8, "수도요금": 7.6, 
    "월세": 44.9, "패션": 22, "담배": 9.3, "음료": 4, "운동화": 4.4, "편의점": 5.8, "김치": 1.3, "카레": 0.2, "고추장": 0.3, 
    "소금": 0.2, "설탕": 0.3, "과자": 9.4, "상추": 0.6, "사과": 2.3, "식용유": 0.8, "계란": 3, "우유": 3.4, "햄": 4.7, 
    "닭": 1.5, "빵": 6.8, "시리얼": 0.4, "쌀": 5.3, "밀가루": 0.1
}

# 실제 데이터 프레임 열 이름과 가중치 딕셔너리 키를 비교하여 공통된 열 선택
common_columns = [col for col in weighted_average_data.columns if col.split('_trend_ratio')[0] in weights_dict]

# 공통된 열만 필터링하고 가중치 곱하기
filtered_data = weighted_average_data[common_columns].copy()
for column in filtered_data.columns:
    base_column = column.split('_trend_ratio')[0]
    filtered_data[column] *= weights_dict[base_column]

# 결과 저장
output_file_path = r'C:\Users\linva\Downloads\filtered_weighted_average_results_with_weights.xlsx'  # 저장할 파일 경로로 수정
filtered_data.to_excel(output_file_path)

print(f"Filtered weighted average results with weights saved to {output_file_path}")
