import pandas as pd

def fetch_golden_data(file_path='data/en.openfoodfacts.org.products.csv.gz', 
                      target_categories=['beverages', 'biscuits', 'snacks'], 
                      min_records=500):
    
    use_cols = ['product_name', 'categories_tags', 'ingredients_text', 'additives_tags', 'countries_en']
    
    for cat in target_categories:
        print(f"🚀 正在掃描類別: [{cat}] ...")
        golden_list = []
        
        chunks = pd.read_csv(file_path, sep='\t', compression='gzip', 
                             usecols=use_cols, chunksize=50000, low_memory=False)
        
        for chunk in chunks:
            # 1. 類別過濾
            mask_cat = chunk['categories_tags'].str.contains(cat, case=False, na=False)
            # 2. 完整性過濾：必須有成分表字串，且添加物標籤不能為空
            mask_complete = chunk['ingredients_text'].notna() & chunk['additives_tags'].notna()
            
            filtered = chunk[mask_cat & mask_complete]
            
            if not filtered.empty:
                golden_list.append(filtered)
            
            total_found = sum(len(df) for df in golden_list)
            if total_found >= min_records:
                print(f"✅ 已為 [{cat}] 找到 {total_found} 筆完整數據，停止掃描。")
                break
        
        if golden_list:
            final_df = pd.concat(golden_list)
            # 儲存結果
            output_name = f'data/{cat}_golden_records.csv'
            final_df.to_csv(output_name, index=False)
            print(f"💾 檔案已存至: {output_name}")
        else:
            print(f"❌ 找不到足夠的 [{cat}] 完整數據。")

if __name__ == "__main__":
    # 你可以在這裡一次換多個類別跑
    fetch_golden_data(target_categories=['biscuits', 'dairy', 'frozen-foods'])