# Project: Molecular Additive Synergy Analysis (MASA)

## 📌 研究背景
現行食品安全標準多基於單一化學物質的毒理實驗。然而，現代食品加工普遍併用多種添加物，本研究旨在透過計算毒理學 (Computational Toxicology) 探索混合物對人體造成的累積負擔。

## 🎯 研究核心
1. **結構毒理預測**: 從 SMILES 結構預測添加物的潛在代謝競爭。
2. **混合物暴露建模**: 建立 Hazard Index (HI) 以外的動態代謝模型。
3. **法規缺口分析**: 識別出哪些市售產品雖然符合現行法規，但在計算模型下具有潛在風險。

## 🛠 目前進度
- [x] 研究框架定義
- [ ] 核心添加物 SMILES 特徵庫建立 (正在進行)
- [ ] 代謝路徑競爭邏輯開發

## 🧪 研究方法論：三維驗證 (Triple Validation)
1. **空間聚類 (Spatial Clustering)**: 證明不同法規類別的化學物質在生物物理特性上的重疊性。
2. **酵素競爭模型 (Enzyme Competition)**: 基於氫鍵受體與脂溶性預測代謝瓶頸。
3. **HI 漏洞分析 (Hazard Index Simulation)**: 量化「單一合格、群體超標」之法規漏洞，並以市售產品組合為驗證對象。

## 🔬 驗證與科學性
本研究將引用 OECD QSAR 工具箱進行基準測試，並比對 PubMed 歷史毒理文獻作為外部驗證標竿。
