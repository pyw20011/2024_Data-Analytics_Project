import pandas as pd

# 데이터 로딩
file_path = r'C:\Users\linva\Downloads\prophet_trends_2024_google_fixed.xlsx'  
data = pd.read_excel(file_path)

# 열 이름에서 '_results' 제거
data.columns = [col.replace('_results', '') for col in data.columns]

# 열 이름을 가나다순으로 정렬
data_sorted = data.reindex(sorted(data.columns), axis=1)

# 결과 저장
output_file_path = r'C:\Users\linva\Downloads\sorted_prophet_trends_2024_google_fixed.xlsx'  # 저장할 파일 경로로 수정
data_sorted.to_excel(output_file_path, index=False)

print(f"Sorted data saved to {output_file_path}")
