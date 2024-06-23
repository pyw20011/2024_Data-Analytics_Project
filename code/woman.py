import pandas as pd

# 데이터 로딩
weighted_average_path = r'C:\Users\linva\Downloads\weighted_average_results.xlsx'  # 실제 파일 경로로 수정

weighted_average_data = pd.read_excel(weighted_average_path, index_col=0)

# 새로 주어진 남성 가중치 정의
weights_dict = {
    "부동산": 0.8, "보험": 12.3, "헤어샵": 9.5, "화장품": 8.9, "장신구": 1, "샴푸": 1, "바디워시": 0.5, "여행": 11.9,
    "커피": 11.4, "파스타": 1.5, "김밥": 3.4, "떡볶이": 3.1, "학원": 27.6, "학습지": 3.5, "ott": 8, "수신료": 2.4,
    "문제집": 1.2, "반려동물": 5.9, "컴퓨터": 3, "tv": 1.9, "영화": 1, "스마트폰": 10.4, "통신요금": 29.8, "항공": 3.9,
    "택배": 1.9, "휘발유": 24.1, "승용차": 13.1, "병원비": 20.5, "영양제": 8.9, "한의원": 3.7, "세탁": 3.9, "냉장고": 2.4,
    "부엌": 4.6, "레인지": 0.7, "밥솥": 0.5, "가구": 11.3, "난방비": 1.6, "도시가스": 11.5, "전기료": 16.1, "쓰레기봉투": 0.7,
    "수도요금": 7.6, "리모델링": 9.3, "패션": 26.2, "음료": 4, "김치": 1.3, "조미료": 0.5, "식초": 0.1, "카레": 0.2, "고추장": 0.3,
    "양념": 0.5, "간장": 0.4, "된장": 0.4, "소금": 0.2, "참깨": 0.6, "고춧가루": 1.6, "파프리카": 0.6, "감자": 0.6, "콩나물": 0.5,
    "버섯": 0.9, "양파": 0.7, "대파": 0.9, "마늘": 1.3, "오이": 0.6, "고추": 0.6, "열무": 0.2, "배추": 1.3, "상추": 0.6,
    "시금치": 0.3, "바나나": 0.8, "쌀": 5.3, "귤": 1.8, "딸기": 1.5, "사과": 2.3, "브로콜리": 0.2, "오렌지": 0.4, "우유": 3.4,
    "복숭아": 1, "포도": 1.4, "식용유": 0.8, "미역": 0.3
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
