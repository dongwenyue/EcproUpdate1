from src.dangdang.client import DangDangAPi


class SimpleDangDangAPi(DangDangAPi):

    def getShopBrand(self):
        # 品牌
        url = "dangdang.shop.ddbrand.get"
        return self.send(DangDangAPi.Get, url, "2.0")

    def getTemplateBaseInfo(self):
        # 运费模板
        url = "dangdang.shop.getTemplateBaseInfo.get"
        return self.send(DangDangAPi.Get, url, "1.0")

    def getShopCategory(self):
        # 店铺分类
        url = "dangdang.shop.category.get"
        return self.send(DangDangAPi.Get, url, "2.0")

    def getShopProps(self):
        url = "dangdang.shop.ddsaleprops.get"
        return self.send(DangDangAPi.Get, url, "1.0")


if __name__ == "__main__":
    DangDang_APP_KEY = "2100009643"
    DangDang_APP_SECRET = "54F12C7FA3115A6BE66A1BB2DBAA78DE"
    token = "E5DC29D15647874342FDEC22D1B6AD4C6251F9744F65EFCFB84EA943BAC96908"
    t = SimpleDangDangAPi("2100009643", "54F12C7FA3115A6BE66A1BB2DBAA78DE", "E5DC29D15647874342FDEC22D1B6AD4C6251F9744F65EFCFB84EA943BAC96908")
    z = t.getShopBrand()
    w = t.getTemplateBaseInfo()
    v = t.getShopCategory()
    print(z)
    print(w)
    print(v)