import os
import re
import time
import requests
import pdfplumber
import pandas as pd
from googlesearch import search

class MixtureAnalyzer:
    def __init__(self, output_file='mixture_composition_results.csv'):
        self.output_file = output_file
        self.results = []
        # 預設的代表性配方 (當爬蟲失敗時的回退機制)
        self.expert_knowledge = {
            "E471": "Mono- and diglycerides (90%), Free fatty acids (7%), Glycerin (3%)",
            "E440": "Galacturonic acid (>65%), Rhamnose, Galactose",
            "E1001": "Choline chloride (98%), Water (2%)",
            "E1442": "Hydroxypropyl distarch phosphate (Modified Starch 100%)",
            "E415": "Xanthan gum (Polysaccharide complex 100%)"
        }

    def get_sds_pdf_links(self, query_name, limit=2):
        """ 第一階：搜尋 SDS PDF """
        print(f"🔍 正在搜尋 {query_name} 的 SDS 來源...")
        query = f'"{query_name}" SDS Section 3 composition filetype:pdf'
        links = []
        try:
            for url in search(query, num_results=limit):
                if url.endswith('.pdf'):
                    links.append(url)
            return links
        except Exception as e:
            print(f"⚠️ 搜尋受阻: {e}")
            return []

    def download_and_parse_pdf(self, url):
        """ 第二階：下載並解析 PDF 第 3 章節 """
        temp_pdf = "temp_sds.pdf"
        try:
            response = requests.get(url, timeout=15)
            with open(temp_pdf, 'wb') as f:
                f.write(response.content)
            
            composition_text = ""
            with pdfplumber.open(temp_pdf) as pdf:
                # 通常成分在第 2-4 頁
                for page in pdf.pages[1:4]:
                    text = page.extract_text()
                    if text and ("Section 3" in text or "Composition" in text):
                        # 嘗試抓取表格
                        table = page.extract_table()
                        if table:
                            composition_text = str(table)
                            break
                        composition_text = text
            
            os.remove(temp_pdf)
            return composition_text[:500] # 只取關鍵段落
        except:
            return None

    def run_analysis(self, additive_list):
        """ 執行主邏輯 """
        for item in additive_list:
            e_num = item.get('e_number', 'Unknown')
            name = item.get('name', '')
            print(f"\n🧪 處理對象: {e_num} - {name}")

            # 1. 嘗試從專家知識庫獲取 (最快)
            formula = self.expert_knowledge.get(e_num, "Scanning SDS...")

            # 2. 如果沒有預設，則啟動爬蟲
            sds_info = "No SDS data found"
            if formula == "Scanning SDS...":
                pdf_links = self.get_sds_pdf_links(name)
                if pdf_links:
                    parsed_content = self.download_and_parse_pdf(pdf_links[0])
                    if parsed_content:
                        sds_info = parsed_content
                formula = sds_info

            self.results.append({
                '混合物名稱': f"{e_num} - {name}",
                '純物質名稱與比例': formula,
                '來源/別稱': f"SDS Link: {pdf_links[0]}" if 'pdf_links' in locals() and pdf_links else "Internal Expert DB"
            })
            time.sleep(2) # 防止被 Google 封鎖

        # 儲存結果
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 分析完成！結果已存至 {self.output_file}")

# --- 執行示範 ---
if __name__ == "__main__":
    # 你可以從你的 top_1000_additives.csv 讀取這些
    test_list = [
        {'e_number': 'E471', 'name': 'Mono- and diglycerides of fatty acids'},
        {'e_number': 'E1001', 'name': 'Choline salts'},
        {'e_number': 'E440', 'name': 'Pectin'}
    ]
    
    analyzer = MixtureAnalyzer()
    analyzer.run_analysis(test_list)