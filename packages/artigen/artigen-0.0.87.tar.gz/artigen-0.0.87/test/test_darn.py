from artigen.Registry.Darn import Darn
import asyncio

async def test_list_darn():
    api_key = "VyA7hXeMMgMvTxuAhhFB5w025eG2D+1p4Jc1+ES4ZtY7PM7VeCY+EyNDiyEQJhkH5kFiOdWnnijiNhqo2RLjoHp31KiATi1/fPnsWWWS8wkGsWpeARhWg/eIPI5Iji0HQga8n9MMkGroB51sj1SlqgFVF+5SkmtZN2t/dC22XMP7L7Db0fz0r7jT6Y4WJJ1pKchG7b0BQ0P0tw5XLVdbNg=="
    darn = Darn(api_key=api_key)
    # response = await darn.list_darn()
    # print(response)

    # darn_create = await darn.update_darn(
    #     name="SDK_101",
    #     file_paths=["/Users/surajsingh/Downloads/09738562-8C7D-42C5-B8B4-D0B341E2FA96.jpg"]
    # )
    # print(darn_create)

    # darn_create = await darn.create_new_darn(
    #     name="SDK_111")
    # print(darn_create)

    darn_delete=await darn.delete_darn(name="SDK_101")
    print(darn_delete)
asyncio.run(test_list_darn())