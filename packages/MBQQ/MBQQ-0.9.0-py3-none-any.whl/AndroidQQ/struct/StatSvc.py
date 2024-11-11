import json
import zlib

from Jce import JceInputStream, JceStruct

from AndroidQQ.struct.head import *


def DelDevLoginInfo(info, key):
    """删除登录信息"""
    key = bytes.fromhex(key)
    _data = JceWriter().write_bytes(key, 0)

    jce = JceWriter()
    jce.write_bytes(info.Guid, 0)
    jce.write_string('com.tencent.mobileqq', 1)
    jce.write_jce_struct_list([_data], 2)
    jce.write_int32(1, 3)
    jce.write_int32(0, 4)
    jce.write_int32(0, 5)
    _data = jce.bytes()
    _data = JceWriter().write_jce_struct(_data, 0)
    _data = JceWriter().write_map({'SvcReqDelLoginInfo': _data}, 0)
    _data = PackHeadNoToken(info, _data, 'StatSvc.DelDevLoginInfo', 'StatSvc', 'SvcReqDelLoginInfo')
    _data = Pack_(info, _data, Types=11, encryption=1, sso_seq=info.seq)
    return _data


def DelDevLoginInfo_res(data):
    """似乎没有明确的返回信息"""
    # 1d8e13a0cfede20498125f0d34c4731932889c4c0d816af6e2bea8f81b3a62ff5a93d793ac36006e5c1f35ac6f1b35fca720957b9fe5fa568f777902a4d3843c8acbf2798d059a7df5c68ca6f1d781d88bf3c788155aa96802063369d004e41d431c50ca463a1b7b4f7865b5e81f34a9
    data = Un_jce_Head(data)
    data = Un_jce_Head_2(data)
    stream = JceInputStream(data)
    jce = JceStruct()
    jce.read_from(stream)
    return jce.to_json()
