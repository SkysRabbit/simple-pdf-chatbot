# 回答用戶特定問題的聊天機器人

## 達成目標
讓機器人能回答用戶關於污水處理廠的相關問題及給予最相近與精確的回答

## 目標資料
- 竹東SMP pdf檔
- 竹東SOP pdf檔

## 使用工具與技術
- 模型使用Llama3(open source LLM)
- 使用RAG
- Embedding model使用HuggingFace上對中文語意理解最好的model
- 向量資料庫先選擇熱門的FAISS或ChromaDB
- 使用LlamaParse將PDF拆分成小部分，**並將圖片、表格塞選出來作後續處理或優化**
- UI先使用Python前端框架Streamlit實現，之後再轉成使用React與Python backend

## 目前進度
- [x] 將pdf檔切割成子pdf
- [x] 將pdf檔裡的圖片擷取出來，並儲存metadata資訊以供後續使用
- [x] 將OCR的pdf存成圖片並解析圖片內的文字，作為後續RAG的應用
- [x] 使用Llamaparse將pdf變成document格式
- [x] 準備向量資料庫
- [x] pdf進行embedding與存入向量資料庫
- [x] 選擇LLM model
- [x] 本地測試問答
- [x] 將所有元素放在一起
- [x] 設計UI，並將整合前者的步驟 - 使用`Streamlit`設計介面
- [ ] 優化RAG的表現 - RagFusion、SelfQuery或其他手法
- [ ] Apply multi agent
- [ ] LangGraph
- [ ] 爬蟲處理
- [ ] 加上log追蹤

## 目標問題集
- 如果有機會，是否能夠使用prompt的方式產生QA?
- 或是先以用戶自行發問為主

## 挑戰與改善空間
- 增加擷取來源資料的正確性
- 使用不同的embedding model增加語意分析
- Reranking RAG?
- RAG fusion機制

## 其他或已知問題
- 在分割pdf時需要手動切割
- 在Llamaparse部分若是使用免費版本擷取，在效果上會受限，會影響到最終LLM的回答
- 如果為OCR PDF，需要使用其他方法處理，如easyocr、pytesseract等函式庫

## 部署方式
- 目前先以本地端為主
- 參考 `.env.example` 內容並創建 `.env` 儲存環境變數
