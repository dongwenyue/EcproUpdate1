#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022-07-07
# @Author  : AYER
# @Function : 药物临床试验机构备案管理信息平台采集
import os
import sys
from email import header

from faker import proxy

sys.path.append(os.getcwd())

# from src.wangran import config
from lxml import etree
import json
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s: %(message)s')

DETAIL_URL = "https://beian.cfdi.org.cn/CTMDS/pub/PUB010100.do?method=handle07&compId={ID}&_=1657160967711"

PAGE_NUMBER = 1     # 122
CONCURRENCY = 2

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

async def scrape_api(Data_ID):
    if isinstance(Data_ID,dict):
        INDEX_URL = "https://beian.cfdi.org.cn/CTMDS/pub/PUB010100.do?method=handle06&_dt=20220707102928"
        async with semaphore:   # 作为上下文信号变量
            try:
                logging.info("Data_ID: %s", Data_ID['curPage'])
                # header = config.get_headers()
                # proxy = config.process_requestb()
                # proxy = proxy['http']
                async with session.post(INDEX_URL,data=Data_ID,headers=header,proxy=proxy,verify_ssl=False) as response:
                    return await response.json()
            except aiohttp.ClientError:
                logging.error("error occurred while scraping %s", Data_ID, exc_info=True)
    elif isinstance(Data_ID,str):
        async with semaphore:   # 作为上下文信号变量
            try:
                PAGE_URL = Data_ID
                logging.info("Data_ID: %s", PAGE_URL)
                # header = config.get_headers()
                # proxy = config.process_requestb()
                # proxy = proxy['http']
                async with session.get(PAGE_URL,headers=header,proxy=proxy,verify_ssl=False) as response:
                    return await response.text()
            except aiohttp.ClientError:
                logging.error("error occurred while scraping %s", Data_ID, exc_info=True)


async def scraoe_index(PAGE):
    data = {
        "pageSize": '10',
        "curPage": str(PAGE),
        "sortName": "",
        "sortOrder": "",
    }
    return await scrape_api(data)

async def main():
    '''
    串联调用上面两个方法
    :return:
    '''
    global session  # 全局一个session变量方便引用
    session = aiohttp.ClientSession()
    scrape_index_tasks = [asyncio.ensure_future(scraoe_index(page)) for page in range(1,PAGE_NUMBER + 1)]
    results = await asyncio.gather(*scrape_index_tasks)
    # logging.info("results %s",json.dumps(results,ensure_ascii=False,indent=2))
    ids = []
    for index_data in results:
        if index_data['data']!=[]:
            for IDS in index_data['data']:
                ID = IDS['companyId']
                ids.append(ID)

    Data_List = []
    for da in results:
        if da['data'] != []:
            for message in da['data']:
                del message['showInfo']
                del message['ROW2']
                del message['recordStatus']
                Data_List.append(message)
    await seve_data_hospital(Data_List)

    scrape_index_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
    await asyncio.wait(scrape_index_tasks)
    await session.close()

async def seve_data_persion(data):
    logging.info('saving data %s',data)
    html = etree.HTML(data)
    a = html.xpath("//li[@class='active']//text()")
    logging.info(a)

async def seve_data_hospital(data):
    for da in data:
        cols = ", ".join('"{}"'.format(k) for k in da.keys())
        val_cols = ", ".join("'{}'".format(k) for k in da.values())
        sql = "INSERT INTO medo_master.xxxxx (%s) VALUES(%s)" % (
            cols,
            val_cols,
        )
        logging.info(sql)

async def scrape_detail(id):
    url = DETAIL_URL.format(ID=id)
    data = await scrape_api(url)
    await seve_data_persion(data)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
