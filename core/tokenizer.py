
def test():
    ...  
def tokenizer():
    #段詞分析 需要網路！
    from pandas import DataFrame
    from collections import Counter
    from .models import analysed_news as news

	
    #print(news.db_get(news_id=(7315,8614171)))

    print("🔥載入斷詞模型...真浪費時間")
    from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
    print("🔥載入斷詞模型完成！")

    # model="albert-tiny" 最小模型，斷詞速度比較快，犧牲一些精確度
    # model="bert-base" 最大模型，斷詞準確，不要用CPU來算
    ws = CkipWordSegmenter(model="bert-base") 
    pos = CkipPosTagger(model="bert-base")
    ner = CkipNerChunker(model="bert-base")
    

    got_news_dict:DataFrame = news.db_get_rowNews_DataFrame()

    # Word Segmentation 進行分詞
    tokens = ws(got_news_dict.content)
    # Word Segmentation 進行分詞
    tokens = ws(got_news_dict.content)
    # POS 分析詞性
    tokens_pos = pos(tokens)

    # word pos pair 將1和2黏在一起
    word_pos_pair = [list(zip(w, p)) for w, p in zip(tokens, tokens_pos)]

    # NER命 名實體辨識
    entity_list = ner(got_news_dict.content)

    # 過濾條件:兩個字以上 特定的詞性
    # allowPOS 過濾條件: 特定的詞性
    allowPOS = ['Na', 'Nb', 'Nc', 'VC']

    tokens_v2 = []
    for wp in word_pos_pair:
        tokens_v2.append([w for w, p in wp if (len(w) >= 2) and p in allowPOS])

    # Insert tokens into dataframe (新增斷詞資料欄位)
    got_news_dict['tokens'] = tokens
    got_news_dict['tokens_v2'] = tokens_v2
    got_news_dict['entities'] = entity_list
    got_news_dict['token_pos'] = word_pos_pair

    # Calculate word count (frequency) 計算字頻(次數)
    def word_frequency(wp_pair):
        filtered_words = []
        for word, pos in wp_pair:
            if (pos in allowPOS) & (len(word) >= 2):
                filtered_words.append(word)
            #print('%s %s' % (word, pos))
        counter = Counter(filtered_words)
        return counter.most_common(200)

    keyfreqs = []
    for wp in word_pos_pair:
        topwords = word_frequency(wp)
        keyfreqs.append(topwords)
    got_news_dict['top_key_freq'] = keyfreqs

    # Abstract (summary) and sentimental score(摘要與情緒分數)
    summary = []
    sentiment = []
    for text in got_news_dict.content:
        summary.append("暫無")
        sentiment.append("暫無")
    got_news_dict['summary'] = summary
    got_news_dict['sentiment'] = sentiment
    
    
    # 將 DataFrame 寫入資料庫
    if news.db_bulk_update_DataFrame(got_news_dict):
        print("已儲存斷詞分析")
    else:
        print("❗斷詞分析儲存失敗")
            
# 此部分負責將熱門詞結果儲存為csv檔案
# df_top_group_words = pd.DataFrame(top_group_words, columns = ['category','top_keys'])
# Part3_file_name = "熱門詞結果_"+datetime.now().strftime("%m%d_%H%M") +".csv"
# df_top_group_words.to_csv(Part3_file_name, index=False, encoding="utf-8-sig")
# print("已將 CSV 檔案儲存在：%s\n檔案名稱：%s" % (where, Part3_file_name))