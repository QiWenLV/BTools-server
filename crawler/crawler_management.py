from crawler.crawler_video_list import *
from crawler.crawler_up_stat import *
from crawler.crawlet_up_follows import *
from crawler.crawler_video_detail import *
from persist.persist import IPersist
from persist.mongo_persist import MongoPersist
import json


def crawler(upid, iPersist: IPersist):
    # up账号信息
    iPersist.write('up_info', get_up_info(upid), index="mid")
    # 视频列表信息
    pd_v_list_data, pd_classify_data = get_v_list_data(upid, mongo_persist, increment=True)
    iPersist.write('classify_data', pd_classify_data, index=["mid", "tid"])
    v_list = []
    for i in range(0, len(pd_v_list_data)):
        list_item = json.loads(pd_v_list_data.iloc[i].to_json())
        whole_item = get_v_detail(list_item["bvid"], list_item)
        v_list.append(whole_item)
        print("up:{}, bvid:{}, 完成".format(list_item["mid"], list_item["bvid"]))
    iPersist.write('up_video_list', v_list, index="bvid")
    # up关注列表
    up_follows_data = get_up_follows(upid)
    iPersist.write("up_follows", up_follows_data, index=["upid", "mid"])


if __name__ == '__main__':
    upid = 19642758
    mongo_persist = MongoPersist()


    crawler(upid, mongo_persist)
    print("获取完成")
