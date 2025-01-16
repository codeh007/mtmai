# @mtform()
# class SiteCreateForm(BaseModel):
#     name: str = PydanticField(default=None, description="站点名称")
#     title: str = PydanticField(default=None, description="站点标题")
#     description: str = PydanticField(default=None, description="站点描述")
#     layout: str = PydanticField(default=None, description="站点布局")
#     submit_text: str = PydanticField(default=None, description="站点提交文本")
#     action: str = PydanticField(
#         default=None,
#         description="站点操作",
#         json_schema_extra={
#             "title": "Password",
#             "description": "Password of the user",
#             "examples": ["123456"],
#         },
#     )

#     class Config:
#         json_schema_extra = {
#             "title": "站点创建",
#         }
