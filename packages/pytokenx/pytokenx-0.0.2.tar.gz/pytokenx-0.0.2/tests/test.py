
from pytokenx import TokenManager, FileTokenStorage, SQLAlchemyTokenStorage

# 使用文件存储
token_manager = TokenManager(FileTokenStorage("tokens.json"))
# sqlite存储
# token_manager = TokenManager(SQLAlchemyTokenStorage(connection_string="sqlite:///test.db"))
token = token_manager.generate_token() # 生成token
print(token)
token_data = token_manager.validate_token(token) # 验证token
if token_data:
    print(token_data)
else:
    print("token 无效")

token_manager.delete_token(token) # 删除token

# # 使用装饰器
# @token_validator(token_manager)
# def my_function(token):
#     print(token)