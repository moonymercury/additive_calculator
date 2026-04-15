# 🍏 MASA-Project: Molecular Additive Synergy Analysis
**食品添加物之分子協同效應與法規設計漏洞研究**

## 📌 研究願景
現行食品安全法規採取「單一物質限量」制，本研究旨在透過 **Dry Lab (計算毒理學)** 方法，證明多種添加物併用時產生的「雞尾酒效應」與「代謝路徑競爭」，並量化其對人體產生的額外負擔。

---

## 🛠 研究開發流程 (Research Pipeline)

### 第一階段：單分子特徵研究 (Single-Molecule Research)
1. **資料標準化**: 將 1000+ 種添加物名稱轉換為國際通用 SMILES 碼。
2. **特徵工程**: 提取脂溶性 (XLogP)、極性表面積 (TPSA) 及氫鍵受體數。
3. **化學空間映射**: 透過無監督學習 (PCA) 識別性質重疊的添加物群落。

### 第二階段：混合物交互分析與多分子合作危害模型 (Mixture & Cooperative HazardAnalysis)
1. 代謝競爭與路徑壅塞 (Metabolic Competition & Congestion)酵素競爭預測: 
    - 基於分子結構相似度，建立多重添加物對肝臟 CYP450 (如 CYP3A4) 系統的競爭模型。
    - `結構相似度量化`: 導入 Morgan Fingerprints (2048-bit) 與 Tanimoto Coefficient 建立相似度矩陣。
    - `競爭風險定義`: 當添加物間之結構相似度 $T > 0.7$ 時，定義為「高代謝競爭潛力組」，模擬其導致代謝排泄速率減慢之風險。
2. 生物屏障通透性增強 (Barrier Permeability Enhancement)特洛伊木馬效應: 
    - `識別界面活性添加物`（如乳化劑 Polysorbate 80、脂肪酸鹽類），評估其對腸道上皮細胞 緊密連接 (Tight Junctions) 的暫時性破壞。
    - `吸收率修正`: 建立加權算法，模擬當通透性增強者存在時，其他低吸收率毒性物質如何「合作」滲透進入血液循環。
3. 代謝級聯與抗氧化耗竭 (Redox & Antioxidant Depletion)GSH 儲備模擬: 
    - 識別需經由結合反應 (Conjugation) 代謝的添加物，評估其對體內 麩胱甘肽 (GSH) 的集體消耗。
    - `氧化壓力連鎖反應`: 模擬當 A 物質耗盡細胞防禦後，B 物質產生的自由基如何造成指數級的細胞損傷。
4. 溶解度誘導與載體效應 (Solubility & Carrier Facilitation)膠束傳運模型 (Micelle Transport): 
    - 計算`疏水性物質` ($XLogP > 3$) 在油脂類或表面活性劑存在下的溶解度變化。
    - `生物利用度提升`: 研究混合物如何形成穩定的膠束，避開首關效應並透過淋巴系統增加生物利用度。
5. 危害指數 (HI) 與設計漏洞分析 (Regulatory Gap Detection)累積危害指數 (HI) 模擬: 
    - 實作 $HI = \sum (C_i / L_i)$ 指標，分析市售食品中「單項指標合格、總合風險超標」的設計漏洞。
    - `隱性超標預警`: 結合市售產品之大數據 (Open Food Facts)，自動化標記出符合法規但具備「多重合作危害」特徵的高風險組合。
6. 機制驗證：分子對接 (In-silico Molecular Docking)受體交互驗證: 
    - 使用 `AutoDock Vina` 模擬混合物中的多個分子如何同時結合於生物受體的活性位點 (Active site) 或變構位點 (Allosteric site)。
    - 協同性證實: 透過能量評估量化「共存」是否導致受體結合能的顯著改變，從機理性層面證實合作危害。

---

### 各項毒理機制的指標
1. 代謝路徑壅塞指標 (Pathway Congestion Index, PCI)
    - 代表作用：酵素競爭、代謝排泄遲滯。
    - 計算指標：結構相似度 ($T$ 值)：利用 `Tanimoto Coefficient`，當混合物中存在多個 `$T > 0.7$`的分子時，PCI 指數飆升。
        - `氫鍵受體/供體總數`：代表與 CYP 酵素活性中心的結合潛力。
        - `分子體積 (Molecular Volume)`：相似體積的分子更容易競爭相同的蛋白口袋。
2. 屏障破壞風險指標 (Barrier Disruption Score, BDS)
    - 代表作用：界面活性劑增加腸道通透性。
    - 計算指標：兩親性指數 (Amphiphilicity Index)：計算分子的親水親油平衡值（HLB 值）
    - `TPSA 分佈`：如果混合物中包含 $TPSA > 100$（高極性）且同時具有長碳鏈（高脂溶性）的分子，BDS 分數增加。
    - `臨界膠束濃度 (CMC)` 推估值：評估物質在腸道環境形成膠束的傾向。
3. 氧化還原耗竭潛力 (Redox Depletion Potential, RDP)
    - 代表作用：GSH 消耗、細胞防禦崩潰。計算指標：親電性指數 (Electrophilicity Index, $\omega$)：$$\omega = \frac{\mu^2}{2\eta}$$（其中 $\mu$ 是化學勢，$\eta$ 是化學硬度，可由軌域能量 $E_{LUMO}$ 和 $E_{HOMO}$ 推算）。親電性越強，越容易消耗體內的親核排毒劑（如 GSH）。活性片段標記 (Structural Alerts)：如醛基、不飽和羰基等易引發氧化壓力的結構。
4. 載體誘導生物利用度 (Carrier-Induced Bioavailability, CIB)
    - 代表作用：脂溶性物質透過膠束增加吸收。
    - 計算指標：混合物總脂溶性 ($\sum XLogP$)：當 $XLogP > 5$ 的物質與乳化劑共存時，CIB 風險極高。分子柔韌性 (Rotatable Bond Count)：較柔韌的分子更容易被包裹在脂質載體中。

---

### 📏 風險量化指標定義 (Quantification Metrics)
為了使研究具備可預測性，本專案定義了四大風險指標：
1. **PCI (Pathway Congestion Index)**: 基於 Tanimoto 結構相似度，量化酵素競爭強度。
2. **BDS (Barrier Disruption Score)**: 基於兩親性與 TPSA，預測腸道通透性改變風險。
3. **RDP (Redox Depletion Potential)**: 基於親電性結構片段，評估 GSH 排毒系統之耗竭潛力。
4. **CIB (Carrier-Induced Bioavailability)**: 結合 XLogP 與膠束形成傾向，預測生物利用度之異常提升。

---

## 🧱 模組化研究框架 (Modular Research Framework)

### 📁 Module 1: Data Engine
- **Task**: 從 PubChem 提取 SMILES 與理化參數。
- **Output**: `data/processed/features.csv`

### 📁 Module 2: Space Analyzer
- **Task**: 執行 PCA 聚類與 Tanimoto 相似度矩陣運算。
- **Objective**: 識別性質重疊之「結構孿生」群落。

### 📁 Module 3: Synergy Scorer
- **Task**: 運算四大合作危害指標 (PCI, BDS, RDP, CIB)。
- **Logic**: 基於分子描述符之非線性加權風險評分。

### 📁 Module 4: Mech-Validator
- **Task**: 分子對接模擬 (Molecular Docking) 與 QSAR 驗證。
- **Objective**: 從蛋白質結構層面證實代謝競爭機制。

### 📁 Module 5: Market Guardian
- **Task**: 串接 Open Food Facts API，實地偵測法規盲區產品。

---

## 📊 數據結構 (Data Schema)
- `molecular_features.csv`: 儲存單分子的物理化學特徵。
- `synergy_model.py`: 實作混合物加權演算法與風險分級。
- `off_comparison.csv`: 連動 Open Food Facts 之市售產品實例分析。

## 🧪 驗證與正確性說明
- **無監督驗證**: 觀察聚類結果是否與已知毒理學功能分類產生偏離。
- **基準測試 (Benchmarking)**: 比對 OECD QSAR Toolbox 之單體預測數據。
- **虛擬標籤**: 結合已知之 ADI 值與代謝途徑資料，進行半監督式模型評估。

---

## 🚀 研究管線 (Research Pipeline)
1. **微觀特徵化**: 從 SMILES 提取 MW/XLogP/TPSA 指紋。
2. **空間聚類**: 透過 PCA 識別性質重疊之添加物群落。
3. **合作危害建模**: 定義 PCI (代謝競爭)、BDS (屏障破壞)、RDP (氧化耗竭)、CIB (載體效應) 四大指標。
4. **系統性驗證**: 結合分子對接模擬 (Docking) 與 Open Food Facts 大數據，量化現行法規之「劑量漏洞」。

---
## 🚀 目前進度
- [ ] 研究架構定義與 README 撰寫
- [ ] 添加物特徵提取 (SMILES, XLogP)
- [ ] 初步化學空間分佈視覺化
- [ ] 多重混合物風險加權公式開發
- [ ] 市售產品大數據比對

--- 

### 可能可以繼續增進的方向:
方向 A：擴充數據集（解決 PCI 權重過低問題）
目前只有 57 筆，AI 很容易產生偏差。如果能擴充到 1000 筆，AI 就能接觸到更多「長得像但類別不同」的分子，PCI 的權重會顯著提升。

方向 B：啟動「模組四」的分子對接 (Molecular Docking)
這是解決「AI 覺得安全 vs. 傳統覺得危險」的最佳裁判。

實驗設計：將 BHA 與 BHT 拿去跟肝代謝酵素（如 CYP3A4）做對接。

預期結果：如果 Docking 顯示兩者搶奪同一個活性口袋（Active Site），你就可以在論文中寫道：「雖然 ML 模型因 MW 權重過高而判定安全，但分子對接證實了其代謝競爭的機理性風險。」

方向 C：調整 ML 的特徵（Feature Engineering）
既然 AI 太依賴 mw，我們可以試著加入**「交互特徵」**。例如：建立一個 mw_similarity_index，強迫 AI 關注「分子量接近且相似度高」的組合。

方向D: 生物路徑去計算競爭或是危害性

方向E: 複雜混合物，沒有Smiles
對於這類「找不到結構」的添加物，我們在機器學習階段會將其視為「複雜混合物」，這也是法規中最大的盲區之一。

---

## 📈 階段性發現：機器學習模型分析 (2026-04-15)
- **模型表現**: 隨機森林模型達到 $R^2 = 0.837$ 的準確度。
- **權重發現**: 分子量 (MW, 60.3%) 與 載體誘導生物利用度 (CIB, 19.6%) 為風險主導因子。
- **模型背離現象**: 在 BHA/BHT 組合中，AI 預測風險 (0.79) 低於傳統公式 (1.49)。
- **推論**: 現有 ML 模型對結構相似度 (PCI) 的敏感度仍需透過擴大數據集 (N > 1000) 來優化。