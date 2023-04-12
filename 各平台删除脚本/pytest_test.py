import pytest
import requests

from 各平台删除脚本.pytest import get_test_data

cases, list_params = get_test_data("/Users/orange_mac/learn/api_pytest/data/test_in_theaters.yaml")


class TestInTheaters(object):
    @pytest.mark.parametrize("case,http,expected", list(list_params), ids=cases)
    def test_in_theaters(self, case, http, expected):
        host = "http://api.douban.com"
        r = requests.request(http["method"],
                             url=host + http["path"],
                             headers=http["headers"],
                             params=http["params"])
        response = r.json()
        assert response["count"] == expected['response']["count"]
        assert response["start"] == expected['response']["start"]
        assert response["title"] == expected['response']["title"], "实际的标题是：{}".format(response["title"])