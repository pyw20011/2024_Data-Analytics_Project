import pandas as pd

# 데이터 로딩
file1_path = r'C:\Users\linva\Downloads\result1_news.xlsx'  # 실제 파일 경로로 수정
file2_path = r'C:\Users\linva\Downloads\result2_naver.xlsx'  # 실제 파일 경로로 수정
file3_path = r'C:\Users\linva\Downloads\result3_google.xlsx'  # 실제 파일 경로로 수정

data1 = pd.read_excel(file1_path, index_col=0)
data2 = pd.read_excel(file2_path, index_col=0)
data3 = pd.read_excel(file3_path, index_col=0)

# 가중치 정의
weights = [50, 32.5, 17.5]

# 행 이름이 같은지 확인
if not (data1.index.equals(data2.index) and data2.index.equals(data3.index)):
    raise ValueError("DataFrames have different row indexes. Please ensure all DataFrames have the same row indexes.")

# 날짜와 품목 이름을 제외한 숫자 데이터만 선택
numeric_data1 = data1.select_dtypes(include=[float, int])
numeric_data2 = data2.select_dtypes(include=[float, int])
numeric_data3 = data3.select_dtypes(include=[float, int])

# 가중치를 곱한 후 가중평균 계산
weighted_data1 = numeric_data1 * weights[0]
weighted_data2 = numeric_data2 * weights[1]
weighted_data3 = numeric_data3 * weights[2]

# 가중평균 계산
weighted_average = (weighted_data1 + weighted_data2 + weighted_data3) / sum(weights)

# 날짜와 품목 이름 복사
result = data1.copy()
result.update(weighted_average)

# 결과 저장
output_file_path = r'C:\Users\linva\Downloads\weighted_average_results.xlsx'  # 저장할 파일 경로로 수정
result.to_excel(output_file_path)

print(f"Weighted average results saved to {output_file_path}")
