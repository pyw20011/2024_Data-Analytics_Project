import pandas as pd

# 데이터 로딩
weighted_average_path = r'C:\Users\linva\Downloads\weighted_average_results.xlsx'  # 실제 파일 경로로 수정

weighted_average_data = pd.read_excel(weighted_average_path, index_col=0)

# 새로 주어진 남성 가중치 정의
weights_dict = {
    "요양": 0.9, "비누": 0.3, "찜질방": 0.6, "보험": 8.6, "샴푸": 1, "치약": 0.9, "헤어샵": 0.7, "염색약": 0.7, "도시락": 0.6, "막걸리": 0.3, "맥주": 4.8, 
    "소주": 2.5, "커피": 2.6, "오렌지": 0.4, "라면": 0.7, "볶음밥": 0.9, "명태": 0.7, "우유": 3.4, "갈치": 1.1, "생선회": 10.3, "칼국수": 2.7, 
    "냉면": 2.4, "고등어": 2, "굴비": 0.9, "해장국": 5, "해물찜": 4.1, "삼계탕": 2.2, "설렁탕": 2, "비빔밥": 2.4, "김치찌개": 4.8, "된장찌개": 4.3, 
    "식용유": 0.8, "관람": 2.3, "화초": 0.7, "tv": 1.9, "신문": 0.4, "입원": 10.2, "치과": 12.9, "한의원": 3.7, "보청기": 0.6, "약국": 3.5, 
    "영양제": 8.9, "세탁": 3.9, "복숭아": 1, "사과": 2.3, "난방비": 1.6, "도시가스": 11.5, "전기료": 16.1, "쓰레기봉투": 0.7, "수도요금": 7.6, "패션": 11.9, 
    "포도": 1.4, "김치": 1.3, "조미료": 0.5, "식초": 0.1, "고구마": 1, "고추장": 0.3, "양념": 0.5, "간장": 0.4, "된장": 0.4, "소금": 0.2, 
    "참깨": 0.6, "고춧가루": 1.6, "미역": 0.3, "감자": 0.6, "콩나물": 0.5, "버섯": 0.9, "양파": 0.7, "대파": 0.9, "마늘": 1.3, "오이": 0.6, 
    "고추": 0.6, "열무": 0.2, "배추": 1.3, "상추": 0.6, "시금치": 0.3, "전세": 54.2, "쌀": 5.3, "귤": 1.8, "딸기": 1.5
}

# 실제 데이터 프레임 열 이름과 가중치 딕셔너리 키를 비교하여 공통된 열 선택
common_columns = [col for col in weighted_average_data.columns if col.split('_trend_ratio')[0] in weights_dict]

# 공통된 열만 필터링하고 가중치 곱하기
filtered_data = weighted_average_data[common_columns].copy()
for column in filtered_data.columns:
    base_column = column.split('_trend_ratio')[0]
    filtered_data[column] *= weights_dict[base_column]

# 결과 저장
output_file_path = r'C:\Users\linva\Downloads\filtered_weighted_average_results_with_new_weights.xlsx'  # 저장할 파일 경로로 수정
filtered_data.to_excel(output_file_path)

print(f"Filtered weighted average results with weights saved to {output_file_path}")

# Get the columns without '_trend_ratio' suffix
filtered_columns = [col.split('_trend_ratio')[0] for col in filtered_data.columns]

# Find missing columns
missing_columns = [key for key in weights_dict.keys() if key not in filtered_columns]

print(f"Missing columns: {missing_columns}")