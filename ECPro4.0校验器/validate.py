# pylint: disable=bad-continuation
"""
上货关联数据校验
"""
import re
import typing
import json

from marshmallow import fields, Schema
from product_schema import (
    BasePropDataSchema,
    CategoryPropSchema,
    validate_schema,
)
from product_schema.ptyping import SimpleProp
from product_schema.exceptions import ValidationError

from config.size_map.models import SizeMap
from engine.configs import (
    TAOBAO_TP_ID,
    VIP_TP_ID,
    TMALL_TP_ID,
    TIKTOK_TP_ID,
    AIKUCUN_TP_ID,
    YK_TP_ID
)
from product.models import (
    Product,
    ProductInfo,
    ProductSizeInfo,
    ProductSpec,
    ProductSpecValue,
    ProductSku
)
from shop.models import Shop, ShopBrand, TaobaoBrand
from publish.models import TpCategorySpecialProp as TpCategoryProp, TpCategorySpec, TpCategorySpecValue
from publish.models import Publish
from publish.define import (
    TAOBO_BRAND_PROP_ID,
    TAOBAO_EMPTY_QUANTITY,
    VIP_EMPTY_NUMBER,
)
from outside import catalog as CatalogService
from platform_resources.api import validate as platform_validate


class ProductPropDataSchema(BasePropDataSchema):
    """商品数据校验"""
    category_id = SimpleProp(label="类目", required=True, must=True, value_type="int")
    category_path = SimpleProp(label="类目路径", value_type="string")
    account_id = SimpleProp(label="账户ID", value_type="int")
    sizes = SimpleProp(label="商品尺码", value_type="string")

    def __init__(self, **context):
        """初始化"""
        category_prop_schema = self.get_category_schema(context["category_id"], context["tp_ids"])
        created_type = context.get("created_type")
        context["excludeValidator"] = "requiredValidator" if created_type != ProductInfo.ENTERED_STATUS else None
        super().__init__(category_prop_schema, **context)

    def validate(self):
        super().validate()
        return self.errs

    @validate_schema
    def validate_sku_related(self, obj):
        """校验SKU相关数据"""
        if self.context.get("excludeValidator") == "requiredValidator":
            return
        tp_ids = self.context.get("tp_ids")
        if tp_ids is None:
            return
        sku_table = obj.get_prop_by_name("sku_table")
        # 淘宝SKU相关
        if TAOBAO_TP_ID in tp_ids:
            # 库存校验
            quantities = sku_table.get_cloumns_by_name("quantities")
            sku_quantities = [quantity.value_instance.text for quantity in quantities]
            if not any(sku_quantities):
                self.errs.append("淘宝平台SKU库存必须至少有一个大于0")
            # 一口价校验
            price = obj.get_prop_by_name("price")
            sku_prices = [sku_price.value_instance.text for sku_price in sku_table.get_cloumns_by_name("sku-price")]
            price_value = price.value_instance.text
            if price_value is not None and price_value not in sku_prices:
                str_sku_prices = ",".join([str(sku_price) for sku_price in sku_prices])
                self.errs.append(f"一口价【{price_value}】必须与SKU表有库存的价格【{str_sku_prices}】一致")

        # 唯品会SKU相关
        if VIP_TP_ID in tp_ids:
            vip_barcode_props = sku_table.get_cloumns_by_name("vip_barcode")
            vip_barcodes = [vip_barcode.value_instance.text for vip_barcode in vip_barcode_props]
            code = obj.get_prop_by_name("code")
            code = code.value_instance.text
            for vip_barcode in vip_barcodes:
                err_msg = platform_validate.check_barcode_conflict_on_tp(
                    self.context.get("access_token"),
                    self.context.get("vendor_id"),
                    vip_barcode,
                    code,
                )
                if err_msg is not None:
                    self.errs.append(err_msg)

    @validate_schema
    def validate_number(self, obj):
        """校验色号"""
        if self.context.get("excludeValidator") == "requiredValidator":
            return
        if VIP_TP_ID in self.context.get("tp_ids", []):
            colors = obj.get_prop_by_name("color")
            numbers = colors.get_cloumns_by_name("number")
            empty_numbers = [number for number in numbers if number.is_empty()]
            if len(empty_numbers) > VIP_EMPTY_NUMBER:
                self.errs.append("唯品会色号最多允许一个不填写")
            group_numbers = {number.value_instance.text for number in numbers}
            if len(group_numbers) != len(numbers):
                self.errs.append("颜色色号冲突，请检查存在的重复色号")

    @validate_schema
    def validate_code(self, obj):
        """校验货号"""
        code = obj.get_prop_by_name("code")
        code = code.value_instance.text
        tp_ids = self.context.get("tp_ids", [])
        if VIP_TP_ID in tp_ids and not self.context.get("is_sync"):
            error_msg = platform_validate.validate_vip_code(
                self.context["access_token"], self.context["vendor_id"], code
            )
            if error_msg is not None:
                self.errs.append(error_msg)
        if AIKUCUN_TP_ID in tp_ids:
            res = re.search(r"^[a-zA-Z0-9\+\*\-\.]+$", code)
            if res is None:
                self.errs.append("爱库存款号仅能包含数字、+号、字母、-短横线、*号、小数点，请修改后再提交")

    @validate_schema
    def validate_title(self, obj):
        """校验标题"""
        if self.context.get("excludeValidator") == "requiredValidator":
            return
        title = obj.get_prop_by_name("title")
        title = title.value_instance.text
        if title is None:
            return
        tp_ids = self.context.get("tp_ids", [])
        if VIP_TP_ID in tp_ids:
            try:
                vip_title = obj.get_prop_by_name("vip_title").value_instance.text
                if vip_title:
                    title = vip_title
            except:
                pass
            if len(title) > 30:
                self.errs.append("唯品会标题不能大于30")
        if TIKTOK_TP_ID in tp_ids:
            try:
                tiktok_title = obj.get_prop_by_name("tiktok_title").value_instance.text
                if tiktok_title:
                    title = tiktok_title
            except:
                pass
            count = 0
            for _char in title:
                if _char is None:
                    continue
                # 中文在unicode编码中的开头和结尾
                if "\u4e00" <= _char <= "\u9fa5":
                    count += 2
                else:
                    count += 1
            if count <= 15:
                self.errs.append("抖音标题信息过少，请完善至8个汉字（15字符）及以上")

    @validate_schema
    def validate_official_price(self, obj):
        """校验专柜价"""
        if self.context.get("excludeValidator") == "requiredValidator":
            return
        if TMALL_TP_ID not in self.context.get("tp_ids", []):
            return
        if self.context.get("shop_type") != Shop.OUTLETS_SHOP:
            return
        # 专柜价校验
        price = obj.get_prop_by_name("price")
        price = float(price.value_instance.text) if price.value_instance.text is not None else 0
        official_price = obj.get_prop_by_name("official_price")
        sku_table = obj.get_prop_by_name("sku_table")
        official_prices =  sku_table.get_cloumns_by_name("official_price")
        sku_official_prices = {float(i.value_instance.text) for i in official_prices if i.value_instance.text}
        if not sku_official_prices:
            self.errs.append("SKU的专柜价为必填项")
            return
        official_price = float(official_price.value_instance.text) if official_price.value_instance.text else None
        if not official_price:
            self.errs.append("专柜价为必填项")
            return
        max_sku_official_price, min_sku_official_price = max(sku_official_prices), min(
            sku_official_prices
        )
        if not min_sku_official_price <= official_price <= max_sku_official_price:
            self.errs.append(
                f"专柜价必须在SKU的专柜价区间内\
                    [{min_sku_official_price} ~ {max_sku_official_price}]，请修改"
            )
            return
        if official_price * 0.45 <= price:
            self.errs.append(f"价格不能高于专柜价45折，请修改;SKU中价格不能高于45折，请修改以下项：价格{price}")

    @validate_schema
    def validate_yk_sku(self, obj):
        if self.context.get("excludeValidator") == "requiredValidator":
            return
        tp_ids = self.context.get("tp_ids", [])
        if YK_TP_ID not in tp_ids:
            return
        sku_table = obj.get_prop_by_name("sku_table")
        # 商家编码
        outer_id_columns = sku_table.get_cloumns_by_name("outer_id")
        for index, column in enumerate(outer_id_columns):
            if not column.value_instance.text:
                self.errs.append(f"SKU表第【{index + 1}】行, 驿氪平台的商家编码为必填项")
        # 一口价校验
        bar_code_columns = sku_table.get_cloumns_by_name("barcode")
        for index, column in enumerate(bar_code_columns):
            if not column.value_instance.text:
                self.errs.append(f"SKU表第【{index + 1}】行, 驿氪平台的商品条形码为必填项")

    @validate_schema
    def validate_sizes(self, obj):
        if TMALL_TP_ID not in self.context.get("tp_ids", []):
            return

        validate, err = self._validate_tmall_sizes()
        if not validate:
            self.errs.append(err)

    def _validate_tmall_sizes(self):
        validate = True
        err = ""
        sizes = self._map_sizes(json.loads(self.sizes or "[]"), TMALL_TP_ID)
        ori_category_id = CatalogService.get_original_category_leaf(TMALL_TP_ID, self.category_id)
        size_prop = TpCategorySpec.query.filter(
            TpCategorySpec.tp_id == TMALL_TP_ID,
            TpCategorySpec.tp_category_id == ori_category_id,
            TpCategorySpec.spec_type.in_(["height", "size"]),
            TpCategorySpec.scene == "pub"
        ).first()

        if size_prop is None:
            return validate, err

        size_value_map = {s.prop_value_name: s for s in TpCategorySpecValue.query.filter_by(
            tp_category_spec_id=size_prop.id)}
        if not size_value_map:
            return validate, err

        if not size_prop.is_allow_alias:
            for size in sizes:
                if size not in size_value_map:
                    validate = False
                    err = f"当前类目支持的尺码只包括【{','.join(size_value_map.keys())}】"
                    return validate, err

        return validate, err

    def _map_sizes(self, sizes, tp_id):
        # 用户设置的尺码映射
        size_map = {}
        category_info = CatalogService.categories_get([self.category_id])["categories"][0]
        size_map_data = SizeMap.query.filter(
            SizeMap.account_id == self.account_id,
            SizeMap.type_name == category_info["category_group"]
        ).all()
        for map_data in size_map_data:
            for map in json.loads(map_data.data):
                mapped = map.get(str(tp_id))
                if mapped:
                    size_map[map["text"]] = mapped
        return [size_map.get(size, size) for size in sizes]

    @staticmethod
    def get_category_schema(category_id, tp_ids):
        """获取类目Schema"""
        json_schema = CatalogService.get_category_schema(category_id, tp_ids)
        for sub_schema in json_schema:
            if sub_schema["name"] == "size_table" and TMALL_TP_ID in tp_ids and sub_schema["sub_props"]:
                sub_schema["required"] = True
        return CategoryPropSchema(json_schema)


class PublishRelatedDataValidateForm(Schema):
    """获取类目信息必需数据校验"""
    product_id = fields.Integer(required=True)
    shop_id = fields.Integer(required=True)
    brand_id = fields.Integer(allow_none=True)
    is_main_product = fields.Boolean(allow_none=True)
    batch_id = fields.String(allow_none=True)
    is_sync = fields.Boolean(required=True)


def validate_brand(
    tp_id: int,
    category_id: int,
    brand_id: typing.Optional[int],
    error_messages: typing.List[str]
):
    """校验品牌"""
    brand_name = ""
    if brand_id is not None:
        shop_brand = ShopBrand.query.filter_by(id=brand_id).first()
        if shop_brand is None:
            error_messages.append("品牌已失效，请重新选择")
        else:
            brand_name = shop_brand.name
    if tp_id == TAOBAO_TP_ID:
        tp_category_id = CatalogService.get_original_category_leaf(tp_id, category_id=category_id)
        validate_taobao_brand(brand_name, tp_category_id, error_messages)


def validate_taobao_brand(
    name: str,
    tp_category_id: str,
    error_messages: typing.List[str]
):
    """校验淘宝品牌"""
    brand_prop = TpCategoryProp.query.filter_by(
        tp_id=TAOBAO_TP_ID,
        tp_category_id=tp_category_id,
        prop_id=TAOBO_BRAND_PROP_ID,
    ).first()
    # TODO: 改为抛异常
    if brand_prop is None:
        error_messages.append("品牌规则缺失, 请联系客服")
        return
    if name:
        taobao_brand = TaobaoBrand.query.filter_by(name=name, cid=tp_category_id).first()
        if taobao_brand is None and not brand_prop.is_allow_alias:
            error_messages.append(f"品牌【{name}】无效")
    else:
        if brand_prop.is_must:
            error_messages.append("品牌为必填项")


def validate_publish_related_data(
    shop_id: int,
    product_id: int,
    is_main_product: bool = True,
    brand_id: typing.Optional[int] = None,
    is_sync: bool = False
) -> typing.Optional[typing.List]:
    """校验上货关联数据"""
    if not is_main_product:
        shop_product = Product.query.filter_by(parent_id=product_id, shop_id=shop_id).first()
        if shop_product is None:
            raise ValidationError(messages="店铺级商品数据不存在，不支持按店铺同步")
        product_id = shop_product.id
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        raise ValidationError(messages=f"商品不存在, ID: {product_id}")
    shop = Shop.query.filter_by(id=shop_id).first()
    if shop is None:
        raise ValidationError(messages=f"店铺不存在, ID: {shop_id}")
    related_data = product.__dict__
    if product.price is not None:
        related_data["price"] = float(product.price)
    # 规格
    product_specs = ProductSpec.query.filter_by(product_id=product_id)
    specs = []
    for product_spec in product_specs:
        spec = product_spec.__dict__
        spec_values = []
        # 使用懒加载不清楚哪里被改变了, 第二次使用的时候product_spec_value成了一个dict，改为重新查询，每次生成新对象
        # for product_spec_value in product_spec.spec_values:
        product_spec_values = ProductSpecValue.query.filter_by(product_spec_id=product_spec.id)
        for product_spec_value in product_spec_values:
            spec_values.append({
                "prop_value_id": product_spec_value.id,
                "prop_value_name": product_spec_value.prop_value_name,
                "remark": product_spec_value.remark,
                "number": product_spec_value.number,
            })
        spec["spec_values"] = spec_values
        specs.append(spec)
    related_data["specs"] = specs
    # SKU表
    product_skus = ProductSku.query.filter_by(product_id=product_id)
    skus = []
    for product_sku in product_skus:
        skus.append({
            "spec_value_first_id": product_sku.product_spec_value_first_id,
            "spec_value_second_id": product_sku.product_spec_value_second_id,
            "info": product_sku.info,
        })
    related_data["sku_table"] = skus
    # 尺码表
    size_info = ProductSizeInfo.query.filter_by(product_id=product_id).first()
    if size_info is not None and size_info.data:
        related_data["size_table"] = size_info.data
    # 商品平台属性
    product_info = ProductInfo.query.filter_by(product_id=product_id).first()
    if product_info is not None:
        related_data["info"] = product_info.data
    context = {
        "category_id": product.category_id,
        "tp_ids": [shop.tp_id],
        "created_type": product_info.status if product_info is not None else ProductInfo.NOT_ENTERED_STATUS,
        "shop_type": shop.shop_type,  # 店铺类型
        "access_token": shop.access_token,
        "vendor_id": shop.vendor_id,
        "is_sync": is_sync,
    }
    if not is_main_product or not shop.fill_data:
        # 设置进行全属性字段的校验
        context["created_type"] = ProductInfo.ENTERED_STATUS

    obj = ProductPropDataSchema(**context).load(related_data)
    error_messages = obj.errs
    if not is_sync:
        validate_brand(shop.tp_id, product.category_id, brand_id, error_messages)
    return error_messages
