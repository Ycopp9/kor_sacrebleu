class BaseTokenizer:
    sample = "결국 황대헌만 부지런히 쫓아갔더니 은메달이라는 값진 성과를 냈다는 것이다."
    
    def tokenize(self, text):
        return text.split()
    
    def token_to_sent(self, token:list) -> str:
        return ' '.join(token)
    
 
    
class Character(BaseTokenizer):
    def tokenize(self, text):
        return [char for char in text if char != ' ']