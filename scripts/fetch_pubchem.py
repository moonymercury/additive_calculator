import pubchempy as pcp
import pandas as pd
import time
import os
import re
import socket

def safe_fetch(search_term, retries=3):
    for attempt in range(retries):
        try:
            socket.setdefaulttimeout(30) 
            return pcp.get_compounds(search_term, 'name')
        except Exception as e:
            if attempt < retries - 1: time.sleep(5)
            else: raise e

def clean_name_for_search(name):
    name = re.sub(r'^E\d+[a-z]?\s*[-–]\s*', '', str(name), flags=re.IGNORECASE)
    if " - " in name:
        # 嘗試只抓前半部或後半部
        name = name.split(" - ")[0]
    return re.sub(r'\(.*?\)', '', name).strip()

def fetch_comprehensive_data(input_file='top_1000_additives.csv', output_file='molecular_features.csv'):
    df_input = pd.read_csv(input_file)
    
    # 建立唯一索引
    df_input['unique_key'] = df_input.apply(
        lambda x: x['e_number'] if x['e_number'] != "NON-E" else clean_name_for_search(x['search_name']), axis=1
    )
    
    # [關鍵修正]：按 unique_key 分組，並收集該組內所有「清洗後」的唯一名稱
    print(f"📊 正在收集各類別的候选搜尋詞...")
    tasks = df_input.groupby('unique_key')['search_name'].apply(lambda x: list(set([clean_name_for_search(n) for n in x]))).reset_index()
    
    # 優先排序：讓包含英文關鍵字或純 ASCII 的名稱排在前面，增加命中率
    def prioritize_names(name_list):
        return sorted(name_list, key=lambda x: (not x.isascii(), "acid" not in x.lower(), len(x)))

    if os.path.exists(output_file):
        df_done = pd.read_csv(output_file)
        done_keys = set(df_done['unique_key'].tolist())
    else:
        df_done = pd.DataFrame()
        done_keys = set()

    new_results = []

    for i, row in tasks.iterrows():
        u_key = row['unique_key']
        if u_key in done_keys: continue
            
        print(f"[{i+1}/{len(tasks)}] 正在處理: {u_key}...")
        
        # 準備候選清單：1. E-number, 2. 排序後的名稱
        candidates = [u_key] if u_key.startswith('E') else []
        candidates.extend(prioritize_names(row['search_name']))
        
        found_compound = None
        match_type = "No Match"
        
        # 逐一嘗試直到命中
        for term in candidates:
            if len(term) < 2: continue
            try:
                res = safe_fetch(term)
                if res:
                    found_compound = res[0]
                    match_type = f"Match ({term})"
                    break
            except: continue
            time.sleep(0.5)

        res_data = {
            'unique_key': u_key,
            'cas_number': "Unknown",
            'smiles': None,
            'is_complex_mixture': True,
            'match_method': match_type
        }

        if found_compound:
            cas = "Unknown"
            for s in (found_compound.synonyms or []):
                if re.match(r'^\d{2,7}-\d{2}-\d$', s):
                    cas = s; break
            
            res_data.update({
                'cas_number': cas,
                'smiles': found_compound.smiles,
                'mw': found_compound.molecular_weight,
                'xlogp': found_compound.xlogp,
                'is_complex_mixture': False
            })
            print(f"   ✅ 命中! 使用 [{match_type}] -> CAS: {cas}")
        else:
            print(f"   📦 無法找到結構，標記為複雜混合物")

        new_results.append(res_data)
        
        # 每 10 筆存檔一次
        if (i + 1) % 10 == 0:
            df_done = pd.concat([df_done, pd.DataFrame(new_results)], ignore_index=True)
            df_done.to_csv(output_file, index=False)
            new_results = []

    if new_results:
        df_done = pd.concat([df_done, pd.DataFrame(new_results)], ignore_index=True)
        df_done.to_csv(output_file, index=False)

    # 最後合併回 1.6 萬筆的完整資料
    final_output = df_input.merge(df_done, on='unique_key', how='left')
    final_output.to_csv('molecular_features_final.csv', index=False)
    print("\n🎉 全量資料庫對齊完成！")

if __name__ == "__main__":
    fetch_comprehensive_data()