import pandas as pd
import numpy as np
import re
import os

# Define a function to convert date strings
def convert_date(date_str):
    # Replace '오전' with 'AM' and '오후' with 'PM'
    date_str = re.sub(r'오전', 'AM', date_str)
    date_str = re.sub(r'오후', 'PM', date_str)
    return pd.to_datetime(date_str, format='%Y.%m.%d. %p %I:%M', errors='coerce')

# Define a function to process each file
def process_file(file_path, keyword):
    # Load the Excel file
    data = pd.read_excel(file_path)
    
    # Parse the date column with custom conversion function
    data['Date'] = data['Date'].apply(convert_date)
    
    # Drop rows with invalid dates
    data = data.dropna(subset=['Date'])
    
    # Set 'Date' as the index
    data.set_index('Date', inplace=True)
    
    # Ensure the data starts from 2022-01-01
    data = data[data.index >= '2022-01-01']
    
    # Resample the data by week starting from 2022-01-01 and count the number of articles per week
    weekly_article_counts = data.resample('W-SAT', label='left', closed='left', origin='2022-01-01').size()
    
    # Count occurrences of the keyword in the 'Content' column for each week and apply sqrt transformation
    weekly_keyword_counts = data['Content'].resample('W-SAT', label='left', closed='left', origin='2022-01-01').apply(lambda x: np.sqrt(x.str.count(keyword).sum()))
    
    # Combine both counts into a single DataFrame
    weekly_summary = pd.DataFrame({
        'Article Count': weekly_article_counts,
        f'{keyword} Count (sqrt)': weekly_keyword_counts
    })
    
    # Calculate the sum of the sqrt transformed keyword counts for each week
    weekly_summary['Total Keyword Count (sqrt)'] = weekly_summary[f'{keyword} Count (sqrt)']
    
    # Find the maximum value of 'Total Keyword Count (sqrt)'
    max_value = weekly_summary['Total Keyword Count (sqrt)'].max()
    
    # Normalize the values to make the maximum 100
    weekly_summary['Normalized Keyword Count'] = (weekly_summary['Total Keyword Count (sqrt)'] / max_value) * 100 if max_value > 0 else 0
    
    return weekly_summary

# List of keywords
keywords = [
    "볶음밥", "비누", "패션", "김치", "샴푸", "약국", "떡볶이", "치약", "우유", "복숭아", "전기료", "식초", "컴퓨터", "감자", "고추장",
    "오렌지", "tv", "커피", "소금", "난방비", "딸기", "상추", "칼국수", "보험", "간장", "쓰레기봉투", "카레", "고춧가루", "라면", "맥주",
    "양파", "참깨", "시금치", "배추", "양념", "도시락", "ott", "마늘", "버섯", "오이", "김밥", "수도요금", "열무", "영양제", "한의원", "쌀",
    "막걸리", "콩나물", "된장", "병원비", "냉장고", "대파", "음료", "조미료", "포도", "고추", "식용유", "소주", "사과", "냉면", "도시가스", 
    "귤", "스마트폰", "불고기", "돈까스", "우산", "초밥", "빵", "계란", "쌀국수", "스터디카페", "기숙사", "햄버거", "에어컨", "시리얼", 
    "당구장", "마스크", "지하철", "치킨", "설탕", "노래방", "삼겹살", "닭", "햄", "짬뽕", "탕수육", "돼지갈비", "피자", "월세", "휴지", 
    "자전거", "과자", "편의점", "pc방", "시계", "밀가루", "등록금", "가방", "관리비", "버스", "짜장면", "선풍기", "지갑", "스파게티", 
    "이발", "담배", "전세", "삼계탕", "염색약", "신문", "굴비", "설렁탕", "갈치", "비빔밥", "화초", "해장국", "보청기", "입원", 
    "된장찌개", "명태", "찜질방", "요양", "생선회", "김치찌개", "고등어", "치과", "세탁", "관람", "해물찜", "문제집", "화장품", 
    "가구", "학습지", "밥솥", "바디워시", "장신구", "통신요금", "휘발유", "반려동물", "부엌", "레인지", "항공", "영화", "수신료", 
    "부동산", "여행", "택배", "파스타", "바나나", "학원", "리모델링", "승용차", "헤어샵", "운동화", "파프리카", "고구마", "미역", "브로콜리"
]

# Base path for input and output files
base_path = r'C:\Users\linva\Downloads\크롤링all\{}.xlsx'
output_base_dir = r'C:\Users\linva\Downloads\크롤링all_week'

# Ensure the output directory exists
os.makedirs(output_base_dir, exist_ok=True)

# Dictionary to hold the combined data for each keyword
combined_data = {}

# Process each keyword and save the results
for keyword in keywords:
    input_file_path = base_path.format(keyword + '_results')
    output_file_path = os.path.join(output_base_dir, f'{keyword}_weekly_summary.xlsx')
    
    try:
        # Process the file
        results = process_file(input_file_path, keyword)
        
        # Save the results to a new Excel file
        results.to_excel(output_file_path, index=True)
        
        # Store the normalized keyword count in the combined data dictionary
        combined_data[keyword] = results['Normalized Keyword Count']
        
        print(f"Processed data for '{keyword}' saved to '{output_file_path}'")
    except Exception as e:
        print(f"Failed to process '{keyword}': {e}")

# Combine all the data into a single DataFrame
combined_df = pd.concat(combined_data, axis=1)

# Save the combined data to a new Excel file
combined_output_path = os.path.join(output_base_dir, 'combined_weekly_summary.xlsx')
combined_df.to_excel(combined_output_path)

print(f"Combined data saved to '{combined_output_path}'")
