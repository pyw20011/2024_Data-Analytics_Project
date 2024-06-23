import pandas as pd
from prophet import Prophet
import numpy as np

# 데이터 로딩
file_path = r'C:\Users\user\Downloads\naver_2022.xlsx'
data = pd.read_excel(file_path)

# 열 이름 확인
print(data.columns)
date_column = '날짜'  # 올바른 날짜 열 이름으로 수정

# 날짜 형식으로 변환하고 인덱스 설정
data[date_column] = pd.to_datetime(data[date_column])
data.set_index(date_column, inplace=True)

# 각 품목의 최소값 찾기 및 결측치 대체
for column in data.columns:
    min_value = data[column].min()
    data[column] = data[column].fillna(min_value)

# 월별 데이터로 묶기 (평균 사용), 'M' 사용
monthly_data = data.resample('M').mean()

# 각 품목에 대해 Prophet 모델을 실행하고 트렌드 값을 추출
trend_data = {}
for column in monthly_data.columns:
    prophet_data = monthly_data[[column]].reset_index().rename(columns={date_column: 'ds', column: 'y'})
    model = Prophet()
    model.fit(prophet_data)
    forecast = model.predict(prophet_data)
    trend_data[column] = forecast['trend'].values  # 트렌드 값만 저장

# 트렌드 데이터를 DataFrame으로 변환
trend_df = pd.DataFrame(trend_data, index=monthly_data.index)

# 2024년 1월부터 4월까지의 비율 계산
start_date = '2024-01-31'
end_date = '2024-04-30'
ratio_data = {}
for column in monthly_data.columns:
    trend_col = trend_df[column]
    actual_col = monthly_data[column]
    ratio = actual_col.loc[start_date:end_date] / trend_col.loc[start_date:end_date]
    ratio_data[f'{column}_trend_ratio'] = ratio

# 비율 데이터를 DataFrame으로 변환
results = pd.DataFrame(ratio_data, index=pd.date_range(start=start_date, end=end_date, freq='M'))

# 음수 값, 무한대 값, -무한대 값을 1로 변경
results = results.replace([np.inf, -np.inf], np.nan).fillna(1)
results[results < 0] = 1

# 결과를 엑셀 파일로 저장
output_path_fixed_excel = r'C:\Users\user\Downloads\prophet_trends_2024_naver_fixed.xlsx'
results.to_excel(output_path_fixed_excel)

print("파일 저장 완료:", output_path_fixed_excel)
