# import sys
# import pathlib

# cur_folder = pathlib.Path(__file__).parent.parent
# sys.path.append(str(cur_folder))
# import tests
# import pytest

# from agenteasy.utils import term_parser, review_parser


# def test_term_parser():
#     text = r"这是很多的内容````fdhsjkafdsa{abc:aa} fdhsjk```"
#     result = term_parser(text)
#     assert isinstance(result, dict)


# def test_review_parser():
#     text = "这是很多的内容``最终修改后的译文: test text```解释：ok完成"
#     result = review_parser(text)
#     assert result == "test text"
#     text = "最终修改后的译文: ```test text```\n解释: ok完成"
#     result = review_parser(text)
#     assert result == "test text"
#     text = "fdsafdsa"
#     result = review_parser(text)
#     text = """回答的格式：
# 术语是否正确使用：xxx
# 译文可进行的优化：xxx
# 修改后的译文：xxx
# ---
# 术语是否正确使用：否

# 译文可进行的优化：满
# 解释：根据术语表，"御真" 应翻译为 "ยุโรปจริง"，"修为" 应翻译为 "EXP บำเพ็ญ"，"福袋" 应翻译为 "กระเป๋าโชคลาภ"。合并后的译文应为 "กระเป๋าโชคลาภประจำยุโรปจริง EXP บำเพ็ญ"

# 修改后的译文：กระเป๋าโชคลาภประจำยุโรปจริง EXP บำเพ็ญ"""
#     result = review_parser(text)
#     assert result == "กระเป๋าโชคลาภประจำยุโรปจริง EXP บำเพ็ญ"


# test_review_parser()
