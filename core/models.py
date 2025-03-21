from django.db import models
from pandas import DataFrame

class analysed_news(models.Model):
    """分析完畢的新聞表格\n
    """
    news_id_one:int = models.IntegerField()
    news_id_two:int = models.IntegerField()
    class Meta:
            unique_together = ('news_id_one', 'news_id_two')  # 保證組合唯一
            
    date:str = models.CharField(max_length=255, blank=True, null=True)
    category:str = models.CharField(max_length=255, blank=True, null=True)
    title:str = models.CharField(max_length=255, blank=True, null=True)
    content:str  = models.TextField(blank=True, null=True)
    
    sentiment:list = models.JSONField(default=list)
    summary:list = models.JSONField(default=list)
    
    top_key_freq:list = models.JSONField(default=list)
    tokens:list = models.JSONField(default=list)
    tokens_v2:list = models.JSONField(default=list)
    
    entities:str  = models.TextField(blank=True, null=True)
    token_pos:str  = models.TextField(blank=True, null=True)

    photo_link:str  = models.TextField(blank=True, null=True)
    def __str__(self):
        
        return (
            f"News {self.news_id_one}-{self.news_id_two}\nDate: {self.date}\nCategory: {self.category}\nTitle: {self.title}\nContent: {self.content}\nSentiment: {self.sentiment}\nSummary: {self.summary}\nTop Key Freq: {self.top_key_freq}\nTokens: {self.tokens}\nTokens V2: {self.tokens_v2}\nEntities: {self.entities}\nToken POS: {self.token_pos}\nPhoto Link: {self.photo_link}"
        )
    def to_dict(self):
            return {
                "news_id_one": self.news_id_one,
                "news_id_two": self.news_id_two,
                "date": self.date,
                "category": self.category,
                "title": self.title,
                "content": self.content,
                "sentiment": self.sentiment,
                "summary": self.summary,
                "top_key_freq": self.top_key_freq,
                "tokens": self.tokens,
                "tokens_v2": self.tokens_v2,
                "entities": self.entities,
                "token_pos": self.token_pos,
                "photo_link": self.photo_link,
            }
    def news_id_get(self)->tuple:
        """回傳本物件的news_id

        Returns:
            tuple: news_id
        """
        return self.news_id_one,self.news_id_two
    
    def news_id_get(self)->tuple:
        """回傳本物件的news_id

        Returns:
            tuple: news_id
        """
        return self.news_id_one,self.news_id_two
    
    def news_url_get(self)->str:
        """回傳本物件的news_url\n
        目前source_query = "?from=udn-catebreaknews_ch2"

        Returns:
            str: news_url
        """
        source_query = "?from=udn-catebreaknews_ch2"
        return f'/news/story/{self.news_id_one}/{self.news_id_two}{source_query}'
    
    @classmethod
    def db_get(cls,news_id: tuple) -> "dict | None":
        """
        根據 news_id 獲取對應的新聞。
        Args:
            tuple: news_id
        Returns:
            dict: 若找到則回傳對應新聞，否則回傳 None。
        """
        try:
            return cls.objects.get(news_id_one=news_id[0], news_id_two=news_id[1]).to_dict()
        except Exception as e:
            print(f"❗core/models/db_get 發生錯誤: {e}")
            return False
        
    @classmethod
    def db_get_all_DataFrame(cls) -> "DataFrame | None":
        """將所有新聞打包進 DataFrame

        Returns:
            DataFrame | 包含所有新聞，若失敗則回傳 None
        """        
        try:
            queryset = cls.objects.all().values()  # 取得所有新聞的 QuerySet，轉為字典列表
            df = DataFrame(list(queryset))  # 轉換為 DataFrame
            return df if not df.empty else None  # 確保回傳非空的 DataFrame
        except Exception as e:
            print(f"❗core/models/db_get_all_df 發生錯誤: {e}")
            return False
        
    @classmethod
    def db_bulk_update_DataFrame(cls, data: DataFrame) -> bool:
        """批量更新新聞資料 (所有資料必定已存在)

        Args:
            data (DataFrame)

        Returns:
            bool: 成功則回傳 True，失敗則回傳 False。
        """
        try:
            records = data.to_dict(orient="records")  # 轉換 DataFrame 為字典列表
            for i in records:
                cls.db_update((i["news_id_one"], i["news_id_two"]), i)  # 逐筆更新
            return True
        except Exception as e:
            print(f"❗core/models/db_bulk_update_DataFrame 發生錯誤: {e}")
            return False
        
    @classmethod
    def db_update(cls,news_id:tuple,data: dict)->bool:
        """
        寫入新聞資料 (如果存在則更新，不存在則創建)
        Args:
            tuple: news_id
            dict: data
        Returns:
            bool: 成功則回傳True，失敗則回傳False。
            
        """
        try:
            cls.objects.update_or_create(
            news_id_one=news_id[0],  # 從 tuple 拆出兩個 ID
            news_id_two=news_id[1],
            defaults=data
            )
            return True
        except Exception as e:
            print(f"❗core/models/db_update 發生錯誤: {e}")
            return False
    
    @classmethod    
    def db_delete(cls,news_id:tuple)->bool:
        """
        刪除新聞資料
        Args:
            tuple: news_id
        Returns:
            bool: 成功則回傳True，失敗則回傳False。
            
        """
        try:
            player = cls.objects.get(news_id_one=news_id[0],news_id_two=news_id[1])
            player.delete()
            return True
        except cls.DoesNotExist as e:
            print(f"❗core/models/delete_player_profile 發生錯誤: {e}")
            return False
    @classmethod   
    def db_is_news_exists(cls,news_id:tuple) -> bool:
        """檢查特定新聞是否存在於資料庫
        
        Args:
            tuple: news_id
        
        Returns:
            bool: 若存在則回傳 True，否則回傳 False
        """
        return cls.objects.filter(news_id_one=news_id[0],news_id_two=news_id[1]).exists()
    
    
class system_config(models.Model):
    """系統資料\n
    """
    sysdb_id = models.IntegerField(primary_key=True)
    sysdb_name:str = models.CharField(max_length=50, blank=True, null=True)
    sysdb_data = models.JSONField(default=dict)

    def __str__(self)->str:
    
        return (
            f"{self.sysdb_id}.{self.sysdb_name}：{self.sysdb_data}"
        )
        
    def get_data(self)->dict:
        
        return self.sysdb_data
        
    @classmethod
    def sysdb_get(cls,sysdb_name:str) -> dict:
        """回傳指定的sysdb_data

        Returns:
            dict: 指定的sysdb_data
        """        
        try:
            return cls.objects.get(sysdb_name=sysdb_name).get_data()
        except cls.DoesNotExist:
            print(f"❗core/models/sysdb_get 找不到資料，回傳空字典")
            return {}
        except Exception as e:
            print(f"❗core/models/sysdb_get 發生錯誤，回傳空字典: {e}")
        return {}
    
    @classmethod
    def sysdb_update(cls,sysdb_name:str,sysdb_data:dict) -> bool:
        """
        設定指定sysdb_name的sysdb_data

        Returns:
            bool: 是否成功
        """        
        try:
            cls.objects.update_or_create(
            sysdb_name = sysdb_name,
            defaults={"sysdb_data":sysdb_data}
            )
            return True
        except Exception as e:
            print(f"❗core/models/sysdb_update 發生錯誤: {e}")
            return False