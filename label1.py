# coding:utf-8
# 导入Flask类
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
import json
import time
import sqlite3
from flask import g
from config import LEXMARK_PN, ZEBRA_IP , PN_DATE_IP, SQLLITE_PATH
import socket
import pymssql
import datetime
import random

# Flask类接收一个参数__name__
app = Flask(__name__)
app.debug = False
manager = Manager(app)

# sqlite3的配置部分
DATABASE = SQLLITE_PATH

# SQL EXPRESS 配置部分
# host = '10.10.161.249\SQLEXPRESS'
# database = 'OrionLocal'
# user = 'sa'
# password = 'Lexmark2018'


S = 0


# 获取sqllite3数据库连接
def connect_db():
    return sqlite3.connect(DATABASE)


# 获取SQL EXPRESS数据库连接
mstest = []
def connect_msdb():
    # return conn
    if mstest:
        # print('old conn')
        return mstest[random.randint(0,2)]
    else:
        try:
            print("start 3 new connect_msdb")
            for i in range(0,3):
                ms = pymssql.connect(host='10.10.161.249\SQLEXPRESS', database='OrionLocal', user='sa',
                                     password='Lexmark2018')
                mstest.append(ms)
            print("new 3 connect_msdb ok")
            return mstest[random.randint(0,2)]
        except Exception as e:
            print(e)

@app.before_request
def before_request():
    # print("before")
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    # print("teardown")
    if hasattr(g, 'db'):
        g.db.close()
    # if hasattr(g, 'msdb'):
    #     g.msdb.close()


# 简化sqllite3数据库查询函数
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# 简化SQLEXPRESS数据库查询函数
def query_msdb(query, args=(), one=False):
    mscur = g.msdb.execute(query, args)
    rv = [dict((mscur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in mscur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index1():
    return render_template("test.html")


# 获取sqllite3数据库操作的连接
cur = connect_db()


def zpl_print(part_no_code, print_part_name, qty1, print_po, print_sn, print_time):
    """
    生成打印的斑马指令,并打印
    :return: None
    """
    supplier = b"^XA^FX Top section with company logo, name and address.^CF0,60,50^FO80,50^FDSUPPLIER : Ninestar ^FS"
    # 中文的纳思达显示
    # ns = b"^FO310,15^GFA,05760,05760,00060,:Z64:eJztlj+OFDkUxl9tIUyAMCEBwhxhww1Qm6NwBMINmnK1OpiQI/RR1iOQOuQIU6MOOtvxiGAsrbH3e8/urgK0m5K0R+qpKtdXP7+/NtFlXMZlXMZlXMZl/ILxgij+33w//vfcK6J0un5ENJwnntZ/avHl7getHZlrC8b4VLS6TLZMpMfXNDatK7tSAvWeJur51dy0XeJJ1jpcEJkSHF40wRoPbZi1KvShakvV0swtjRssXtRetHpacGMfl1on9p65w8z1znglL4YzVyVSs3ZYcGH7yV5ox0FPFRKbFvdpaW+i2V6scWGvL+B8pzWhy8s1J54eV7DbjGYS7jas4BM7ZnXiDmY34hHmM528hJCJ1jsAzaiD2PspDF0gh6nGDWtjiD/nqQJ5edDGqxPXjrpxp6GfyPYJfm3clRllKVRqmq1Ee/9QPcxrVntcJ7MFN5KDNjXC2orWjeT8zO1D9bD89ryGCHtzX8YMKrRiILjsK0Ct1/x9sVfd18jK72+qcVMHrWKvdqJdD6ztYKwJht8RrjqUKerGlbiDOyXmavZqX7mi5WsdmJvFXv3p4TqZxqXKLV/B3RTDixRH03rNWiQVmTRzdTlO0XzPLV8jlU228HXTDqwIGgmo02yvKUdwfeNKbptyD5f2GS514hlwRWviY1JZL7h7trfGF1WbJJ/fIQAZEbGTkeQdIsfITv3Ylzm+puzFXo7vBq4ULpesKtAaL8bQB9G6ANfX5Gjcq1tM1HwuUydc1upsJVmrvZXrYfG56vnzqnIdcycJ4fYr1qkzyzx/x9GHaq83oTU04T5eqdt8im9B3YzI54No+dmGtasWX82F9Ib4k6v6BXVdWnw3rPWVWwz+yreryl07iS98Ry+6WneSMsisU3y5T6BBtjWjhtK2FvpgJZ+5CEm4ttX+vpziqyZVIuqXtSYjLVJrTqhf0Tr/lhbcCO7HM1eX1Ox9hqhS6v+p8TXSc5CjnmZ7uwjuTctnzUUCe8NzymaQzvHQuLud/x1IdOuZ25fj3d0N4v2MYzrZA75Qwh+UGvdQ7dW7jyO0GV0Jqad9i+/xy55zxfDN5K6LR16tu/RIuP2++tncaI+2npRoTeVCe8faARkIeznGyGf0DFCZ29f4gnsr2li5q1YL+BvfOueVV7foIIH7M95xzO3UiXv1gC0hKWnnZ+6+bMv452Am9NhDIRuhtVcBPSOj4zHXsp+3d5l05NaxsHdfuuKRdEhXdczSkIL7wombu7b70IdyI5HnljVz+6j+pi9jHtSkvT7g5clsJ3vHnTpT3X3g8bLbIuOQkmUR357U585sklOfTdD3eNkjvgZpzdbO3N2GH2FfGBd5BRAqNw399uOkJ4R+hFbD81hx13Zb5m5A5N4+LvLZHlE5mzR06hhMeMetpMc2hCJZcNfFcGWz3M9c7pOkN3FApw5WziW2n9idA2Jc/Yz4ZjSVkfs8rD7ba8oDV2x0pB6Cy1ULLoxTkbk1vgHFUDfF8AMX2oH0IeJh1Rp8Pms5XdT4gvFX3RSjHKlc68+e7D6gXd1+k2LNTsm+P5j7cubiPSloaLkdduXEteVqQhFeT9Le8qocJKb2tgiXr3Eg0enM7et5wySFwtkE1nbJSc/H700ZB9RUJO7I8DO0KrGlhVfc1fPGM06kMr62vKVE3gXiCkW8LZTR+5bcbRRtFm07djBXDjojvZd98KV7yDBocBs5UrF2TS51WEE9FFFX0imvdGaf4ec1xy4+tZ8icnlYcTCZm5g70Xs+XhLvGXTWepO5nnD7Vh68tDjlvCH3ivcecF1gPxM9l/42CTeeuT8doEd6QvnJfD/Qk+/mJQ8u4zIu45eOfwEzUDEx:816E"

    # part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO: 690300236200^FS"
    part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO:" + part_no_code + b"^FS"
    part_name = b"^FO80,190^FDPART NAME: " + print_part_name + b"^FS"
    ship_to = b"^FO80,260^FDShip to : Primax SSG^FS"
    # qty = b"^FO750,260^FDQty : 6000 pcs^FS"
    qty = b"^FO750,260^FDQty : " + qty1 + b" pcs^FS"
    barcode = b"^FX Third section with barcode.^BY4,3,95^FT84,413^BCN,,N,N^FD>;" + print_po + print_sn + b">6->5" + qty1 + b">6->5" + print_time + b"^FS"
    print(barcode)
    gr2 = b"^FO880,30^GB200,90,12^FS^FT905,95^A0N,60,60^FH\^FDG+R2^FS"
    barcode_text = b"^CF0,40,40^FO350,420^FD" + print_po + print_sn + b"-" + qty1 + b"-" + print_time + b"^FS^XZ"

    z = supplier + part_no + part_name + ship_to + qty + barcode + gr2 + barcode_text
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ZEBRA_IP
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        mysocket.send(z)  # send zpl code
        mysocket.close()  # closing connection
    except Exception as e:
        print(e)


@app.route("/label", methods=["POST"])
def printlabel():
    """
    print label
    :return:
    """
    # 1.获取json参数
    req_dict = request.get_json()

    # 2.获取参数
    lex_pn = req_dict.get("lex_pn")                     # 获取利盟的型号
    part_no = LEXMARK_PN[lex_pn][0]  # 打印的part_no
    qty = req_dict.get("qty")                            # 打印的数量
    po = req_dict.get("po")                              # 打印的po项次信息
    row = req_dict.get("row")                           # 打印的行项目

    # 参数校验
    print(all([lex_pn, po, qty]))
    if not all([lex_pn, po, qty, row]):
        return jsonify(errno="1", errmsg="err", data={"msg": "参数不完整"})

    # 对获取的PO 进行处理
    po = po[:10] + row

    # 3.进行打印信息编码（byte）
    part_no_code = part_no.encode("utf-8").encode()         # 打印的PN
    qty1 = qty.encode("utf-8").encode()                     # 字符串转byte，打印的数量
    print_time = time.strftime("%y%m%d", time.localtime()).encode("utf-8").encode()  # 打印的时间
    print_part_name = LEXMARK_PN[lex_pn][1].encode("utf-8").encode()  # 打印的型号名称
    print_po = po.encode("utf-8").encode()   # 打印的po项次信息

    # 获取创建数据的创建时间
    recode_time = time.strftime("%y%m%d", time.localtime())

    # 处理流水信息
    values = query_db('select max(id), sn from print where po = ?',
                      [po], one=True)
    print(values)
    new_sn = 1
    if values["max(id)"] is None:
        print('No such SN')
        # print(po, recode_time, new_sn, qty, lex_pn, part_no, LEXMARK_PN[lex_pn][1],"Primax", "NS", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        try:
            cur.execute(
                'insert into print (po,print_time,sn,qty,lex_pn,part_no,part_name,ship_to,supplier,create_time) '
                'values (?,?,?,?,?,?,?,?,?,?)',
                (po, recode_time, new_sn, qty, lex_pn, part_no, LEXMARK_PN[lex_pn][1],"Primax", "NS",
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        except Exception as e:
            print(e)
        print('No such SN2')
        cur.commit()
        print("*" * 10)
        # print(cur)
    else:
        new_sn = values['sn'] + 1
        try:
            cur.execute(
                'INSERT INTO print (po,print_time,sn,qty,lex_pn,part_no,part_name,ship_to,supplier,create_time)'
                ' VALUES (?,?,?,?,?,?,?,?,?,?)',
                (po, recode_time, new_sn, qty, lex_pn, part_no, LEXMARK_PN[lex_pn][1], "Primax", "NS",
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            cur.commit()
        except Exception as e:
            print(e)
        print(values)

    # 进行流水号的格式化
    print_sn = "%03d" % new_sn
    print_sn = print_sn.encode("utf-8").encode()

    # pb = str.encode(print_part_no)
    # ns = b"^FO310,23^GFA,04992,04992,00052,:Z64:eJztlT2OGzcYhskwAF0E5nZpDNFALuB0BmJwcpQAuYC7qBCGY2yhLnuD5CimsIWSyjfIUp5iyqWwxXBhmsz7cUaadWEgdSACEsiZefnw+yVjl3EZl3EZl3EZ/3X88pXnvGObefoz0+w8pWG/tplnb86zsyZ+h71YPn/08ktOAIcXDMygsVkXz5L64BhLeF3GgvWGvWUa30y7CHogaCkiM6RR+Caqm65qROlJY/BSLZqFk06cwJPeOtq3HIkTmKWXTzlvqiZj22bm8Ki3vmr68kAcerlopCMEvWbt2R4eGjlpDtUeUL7QdGSKV52BBvaszXPhRTB4VDmH3gtwZx+a+q/+ri6TTrONxdE3RnNorAgT5zg67BHnWLWT5ndweOW8xjdhbTS+8RlbKw9ze+JA03QLR+uzPVeV02qe5SHBBIUQ8WEPe2RgjcPbNHFMEzcrMZmHp35tjICGDFBkaX+LhyBq12Bpzho9cdhkj+VZj2RAPcEITtCO6bBwmhTXJ86UB5lnNZABTeVcgwNjVFg49nOYOTKTW2zesKTvEfrOkneqPbZzMj3hROKQ30SeOK/hmMGDU5NwuCYvMi/y4jf7SByKDziWNFfYaKjOxIqXrRMH5CKt2FxqTYhpxWeO7aChh0jmQjsbcU+cJCh5zpwfjyGf7bGObVpbkiWNxM7tZM9GRraWmLRzXsc8+80wZPDa2BLtR/ypyR6KzytUzEvSTBy5eyxzfFqOSkF8wEEwYs03PlL9XCERrqAJ7ZzXj+WPqX4MLziCKSX+BPuifl/jU+uUUm/hqO5Y7maOKGmy5zev3yVNQeTH2g+082yxR6VPwz8wi5wijxkcdJ0fiPO85oHvB2R0cw0NimLO6884MZUrnKSOpbN5xeP34MQXVOng7HcI8DbgE+lPeVD6zOQH9w0zGolls+FBeN3FZ4bi4z/1B2hQQU855bZwuQ+KtY1rPPqBDGgGqLmG4nMY9+PUdxaOjuUdRSFoZmynoFFbRL5h0JA9h4e+UDHlJ5wXvPA7Oe6i7trSaQfOnZOhcmrSjTvqd0jFJT7wEluJYfcRGWeY6KKRpQOHz5z7hwPWdNAlPtSwtdy7/Y1rV3D5poVGeovHNT7g4FhUTkt8eAYHGjG4/IyolN8CL0+cHtWjqJwWDuqUabV3MKn8hS0iMojBQZPfLPrBrtTW7UizOfUDtlIorJ78UzlkT5puCSMGMbynVoCG5U49kTgWt4DcU22Wx9Cix6O/IcVrfLwsfybioJRhyImjEMZSbm+p0GIwTYmij9AYFC16aLkJatbMPd4iMkWRRuzovkEa3xU5hsqxGZ2ibGvrpoOXWuDsFe60TBddJ6jRHPtcrpO49xaXGw5B18M1fk6QxsY5pkEl0jBOjTOMCU1GDh6tAZwEDm6Ab2sYoUmnPIDmdFLGfo1rthZ9hxYETqA7Yrq1XW1SpzxQ82xevkXpH5almGcdcRy7jMu4jMv4/45/AZfTu+Y=:A33A"
    supplier = b"^XA^FX Top section with company logo, name and address.^CF0,60,50^FO80,50^FDSUPPLIER : Ninestar ^FS"
    # 中文的纳思达显示
    # ns = b"^FO310,15^GFA,05760,05760,00060,:Z64:eJztlj+OFDkUxl9tIUyAMCEBwhxhww1Qm6NwBMINmnK1OpiQI/RR1iOQOuQIU6MOOtvxiGAsrbH3e8/urgK0m5K0R+qpKtdXP7+/NtFlXMZlXMZlXMZl/ILxgij+33w//vfcK6J0un5ENJwnntZ/avHl7getHZlrC8b4VLS6TLZMpMfXNDatK7tSAvWeJur51dy0XeJJ1jpcEJkSHF40wRoPbZi1KvShakvV0swtjRssXtRetHpacGMfl1on9p65w8z1znglL4YzVyVSs3ZYcGH7yV5ox0FPFRKbFvdpaW+i2V6scWGvL+B8pzWhy8s1J54eV7DbjGYS7jas4BM7ZnXiDmY34hHmM528hJCJ1jsAzaiD2PspDF0gh6nGDWtjiD/nqQJ5edDGqxPXjrpxp6GfyPYJfm3clRllKVRqmq1Ee/9QPcxrVntcJ7MFN5KDNjXC2orWjeT8zO1D9bD89ryGCHtzX8YMKrRiILjsK0Ct1/x9sVfd18jK72+qcVMHrWKvdqJdD6ztYKwJht8RrjqUKerGlbiDOyXmavZqX7mi5WsdmJvFXv3p4TqZxqXKLV/B3RTDixRH03rNWiQVmTRzdTlO0XzPLV8jlU228HXTDqwIGgmo02yvKUdwfeNKbptyD5f2GS514hlwRWviY1JZL7h7trfGF1WbJJ/fIQAZEbGTkeQdIsfITv3Ylzm+puzFXo7vBq4ULpesKtAaL8bQB9G6ANfX5Gjcq1tM1HwuUydc1upsJVmrvZXrYfG56vnzqnIdcycJ4fYr1qkzyzx/x9GHaq83oTU04T5eqdt8im9B3YzI54No+dmGtasWX82F9Ib4k6v6BXVdWnw3rPWVWwz+yreryl07iS98Ry+6WneSMsisU3y5T6BBtjWjhtK2FvpgJZ+5CEm4ttX+vpziqyZVIuqXtSYjLVJrTqhf0Tr/lhbcCO7HM1eX1Ox9hqhS6v+p8TXSc5CjnmZ7uwjuTctnzUUCe8NzymaQzvHQuLud/x1IdOuZ25fj3d0N4v2MYzrZA75Qwh+UGvdQ7dW7jyO0GV0Jqad9i+/xy55zxfDN5K6LR16tu/RIuP2++tncaI+2npRoTeVCe8faARkIeznGyGf0DFCZ29f4gnsr2li5q1YL+BvfOueVV7foIIH7M95xzO3UiXv1gC0hKWnnZ+6+bMv452Am9NhDIRuhtVcBPSOj4zHXsp+3d5l05NaxsHdfuuKRdEhXdczSkIL7wombu7b70IdyI5HnljVz+6j+pi9jHtSkvT7g5clsJ3vHnTpT3X3g8bLbIuOQkmUR357U585sklOfTdD3eNkjvgZpzdbO3N2GH2FfGBd5BRAqNw399uOkJ4R+hFbD81hx13Zb5m5A5N4+LvLZHlE5mzR06hhMeMetpMc2hCJZcNfFcGWz3M9c7pOkN3FApw5WziW2n9idA2Jc/Yz4ZjSVkfs8rD7ba8oDV2x0pB6Cy1ULLoxTkbk1vgHFUDfF8AMX2oH0IeJh1Rp8Pms5XdT4gvFX3RSjHKlc68+e7D6gXd1+k2LNTsm+P5j7cubiPSloaLkdduXEteVqQhFeT9Le8qocJKb2tgiXr3Eg0enM7et5wySFwtkE1nbJSc/H700ZB9RUJO7I8DO0KrGlhVfc1fPGM06kMr62vKVE3gXiCkW8LZTR+5bcbRRtFm07djBXDjojvZd98KV7yDBocBs5UrF2TS51WEE9FFFX0imvdGaf4ec1xy4+tZ8icnlYcTCZm5g70Xs+XhLvGXTWepO5nnD7Vh68tDjlvCH3ivcecF1gPxM9l/42CTeeuT8doEd6QvnJfD/Qk+/mJQ8u4zIu45eOfwEzUDEx:816E"

    # part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO: 690300236200^FS"
    part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO:" + part_no_code + b"^FS"
    part_name = b"^FO80,190^FDPART NAME: " + print_part_name + b"^FS"
    ship_to = b"^FO80,260^FDShip to : Primax SSG^FS"
    # qty = b"^FO750,260^FDQty : 6000 pcs^FS"
    qty = b"^FO750,260^FDQty : " + qty1 + b" pcs^FS"
    barcode = b"^FX Third section with barcode.^BY4,3,95^FT84,413^BCN,,N,N^FD>;" + print_po + print_sn + b">6->5" + qty1 + b">6->5" + print_time + b"^FS"
    print(barcode)
    gr2 = b"^FO880,30^GB200,90,12^FS^FT905,95^A0N,60,60^FH\^FDG+R2^FS"
    barcode_text = b"^CF0,40,40^FO350,420^FD" + print_po + print_sn + b"-" + qty1 + b"-" + print_time + b"^FS^XZ"

    z = supplier + part_no + part_name + ship_to + qty + barcode + gr2 + barcode_text

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ZEBRA_IP
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        mysocket.send(z)    # send zpl code
        mysocket.close()  # closing connection
    except Exception as e:
        print(e)

    return jsonify(errno="0", errmsg="ok", data={"real_name": ""})


@app.route("/reprint", methods=["POST", "GET"])
def reprint():
    """
    标签重打
    :return:
    """
    # 重打标签需获取的参数为：PO+项次+流水号
    # 获取参数
    rebarcode = request.get_json().get("posn")
    # rebarcode = request.args.get("posn")
    print(rebarcode)

    # 对参数进行处理，只取：PO+项次+流水号
    reposn = rebarcode[:16]
    poitem = rebarcode[:13]
    sn = str(int(str(reposn[13:])))
    print(poitem)
    print(sn)

    # 取数据库中
    values = query_db('select part_no,part_name,qty,print_time  from print where po = ? and sn = ?',
                      [poitem, sn], one=True)

    if values is None:
        return jsonify(errno="1", errmsg="ok", data={"real_name": ""})
    print(1)
    print(values)
    part_no = values["part_no"]
    part_name = values["part_name"]
    qty = values["qty"]
    ptime = values["print_time"]

    # 进行打印参数的编码和拼接
    part_no_code = part_no.encode()
    print_part_name = part_name.encode()
    qty1 = qty.encode()
    print_po = poitem.encode()

    # 进行流水号的格式化
    sn = "%03d" % int(sn)
    print_sn = sn.encode()

    print_time = ptime.encode()
    zpl_print(part_no_code, print_part_name, qty1, print_po, print_sn, print_time)
    print(values)
    return jsonify(errno="0", errmsg="ok", data={"real_name": ""})


@app.route("/pnlabel", methods=["POST", "GET"])
def pnlabel():
    """
    小标签打印
    :return:
    """
    # url:127.0.0.1/pnlabel?pn=50G4135&print_date=190329&qty=1
    # 获取参数
    pn = request.get_json().get("pn")   # 打印的型号名称
    print_date = request.get_json().get("print_date")      # 指定的打印日期
    print_date = print_date[2:].replace('-', '')
    # print(print_date)
    qty = request.get_json().get("qty_row")         # 指定打印的行数
    top = request.get_json().get("top")             # 打印标签的上下偏移量
    try:
        if len(top) == 0:
            top = "0"
        top = int(top)
    except Exception as e:
        print(e)
    # rebarcode = request.args.get("posn")
    # pn = request.args.get("pn")   # 打印的型号名称
    # print_date = request.args.get("print_date")       # 指定的打印日期
    # qty = request.args.get("qty")         # 指定打印的行数

    # print(pn+print_date)

    # 对获取的参数进行编码
    pn_print_date = pn + ' '+print_date
    pn_print_date = pn_print_date.encode("utf-8").encode()
    pn = pn.encode("utf-8").encode()
    print_date = print_date.encode("utf-8").encode()
    qty = qty.encode("utf-8").encode()
    top = str(top+15).encode()

    # print("ok1")
    # 拼接斑马指令
    # z = b"^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR6,6~SD15^JUS^LRN^CI0^XZ^XA^MMT^LL0059^PW1228^LS0^FT1132,33^A0N,33,33^FH\^FD190329^FS^FT1012,33^A0N,33,33^FH\^FD50G4135^FS^FT731,33^A0N,33,33^FH\^FD50G4135 190329^FS^FT399,33^A0N,33,33^FH\^FD50G4135 190329^FS^FT94,33^A0N,33,33^FH\^FD50G4135 190329^FS^PQ1,0,1,Y^XZ"
    z1 = b"^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR6,6~SD15^JUS^LRN^CI0^XZ^XA^MMT^LL0059^PW1228^LS0"      # 打印是纸张的初始化参数
    # z2 = b"^FT1129,"+top+b"^A0N,33,33^FH\^FD"+print_date+b"^FS^FT1004,"+top+b"^A0N,33,33^FH\^FD"+pn+b"^FS"      # 打印的型号和日期
    z2 = b"^FS^FT980," + top + b"^A0N,33,33^FH\^FD" + pn_print_date + b"^FS"
    z3 = b"^FT678,"+top+b"^A0N,33,33^FH\^FD"+pn_print_date+b"^FS"
    z4 = b"^FT368,"+top+b"^A0N,33,33^FH\^FD"+pn_print_date+b"^FS"
    z5 = b"^FT47,"+top+b"^A0N,33,33^FH\^FD"+pn_print_date+b"^FS"
    z6 = b"^PQ"+qty+b",0,1,Y^XZ"
    z = z1+z2+z3+z4+z5+z6
    # print(z)
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host =PN_DATE_IP
    port = 9100
    # print("ok2")
    try:
        mysocket.connect((host, port))  # connecting to host
        mysocket.send(z)  # send zpl code
        mysocket.close()  # closing connection
    except Exception as e:
        print(e)

    return jsonify(errno="0", errmsg="ok", data={"real_name": ""})



@app.route("/kanban", methods=["POST", "GET"])
def kanban():
    """
    奔图物料看板逻辑
    :return:
    """
    """
    1、前端扫码推送表信息到物料看板信息更新系统，触发场景为：
        ①当某一岗位有物料短缺时：操作员扫码指定的URL缺料二维码，传递拉线（line）,岗位（operation），物料编码（material_code）,物料状态（mark）四个参数到后台，
        缺料URL示例：http://127.0.0.1:80/material?line=1&operation=FA03&material_code=49N0024&state =starving    1
        ②后台进行参数合法性的校验，
            1.判断参数是否都传递了，
            2.判断传递的参数是否正确
            3.数据库中所有物料的初始状态为：0，当收到第一次请求后，校验mark参数为starving,表示发送的是缺料信息，修改该物料的状态为1，并向扫描条码的客户端发送提示信息：XXX物料的缺料信息已发送
            4.物料员收到物料看板展示的欠料信息，并完成该岗位的上料后，扫描该岗位的上料二维码，后台继续进行数据校验，校验mark参数为full,查询该物料的状态为：1，后台修改该物料的状态为：0，并向扫描条码的客户端发送提示信息：XXX物料已完成上料。
            上料URL示例：http://127.0.0.1:5000/kanban?line=1&operation=FA03&material_code=49N0024&state =full    0
        ③前台每10秒向后台请求所有的物料数据，后端查询数据库中的缺料的物料信息并展示，并只显示缺料的物料信息
    """
    # 获取参数
    line = request.args.get("line")
    operation = request.args.get("operation")
    material_code = request.args.get("material_code")
    state = request.args.get("state")
    state = int(state)

    try:
        values = query_db('select state  from kanban WHERE line = ? AND operation = ? AND material_code = ?',
                          [line, operation, material_code], one=True)
        statedb = values['state']
        if statedb == state and state == 1:
            return "<h1>%s线%s岗位，%s，缺料信息已发送,请勿重复扫描</h1>" %(line.encode("utf-8"), operation.encode("utf-8"), material_code.encode("utf-8"))
        if statedb == state and state == 0:
            return "<h1>%s线%s岗位，%s，上料信息已发送,请勿重复扫描</h1>"  %(line.encode("utf-8"), operation.encode("utf-8"), material_code.encode("utf-8"))
    except Exception as e:
        print(e)
        return "error"

    if state == 0:
        try:
            cur.execute('UPDATE kanban SET state = 0 WHERE line = ? AND operation = ? AND material_code = ?',
                        [line, operation, material_code])
            cur.commit()
        except Exception as e:
            print(e)
        # return render_template("kanban.html")
        return "<h1>%s线%s岗位，%s，已完成上料</h1>" %(line.encode("utf-8"), operation.encode("utf-8"), material_code.encode("utf-8"))
    if state == 1:
        try:
            s = cur.execute('UPDATE kanban SET state = 1 WHERE line = ? AND operation = ? AND material_code = ?',
                            [line, operation, material_code])
            # print(s)
            cur.commit()
        except Exception as e:
            print(e)
        return "<h1>%s线%s岗位，%s，缺料信息已发送</h1>" %(line.encode("utf-8"), operation.encode("utf-8"), material_code.encode("utf-8"))


@app.route("/getkanban", methods=["POST", "GET"])
def getkanban():
    """
    获取看板的数据
    :return:
    """
    try:
        # 取数据库中
        values = query_db('select *  from kanban WHERE state = ?', [1])
        for value in values:
            value['state'] = "缺料"
        # print(values)
    except Exception as e:
        print(e)
    return jsonify(errno="0", code=0, data=values)


@app.route("/showkanban", methods=["POST", "GET"])
def showkanban():
    """
    显示看板页面
    :return:
    """
    return render_template("kanban.html")


@app.route("/apex", methods=["POST", "GET"])
def apex():
    """
    APEX 页面
    :return:
    """
    return render_template("apex.html")


@app.route("/apexpn", methods=["POST", "GET"])
def apexpn():
    """
    APEX型号小标签打印
    :return:
    """
    return jsonify(errno="0", errmsg="ok", data={"PNs": ""})


@app.route("/importpn", methods=["POST", "GET"])
def importpn():
    """
    返回所有的APEX型号
    :return:
    """
    import xlrd
    try:
        workbook = xlrd.open_workbook(r"C:\Users\zhaohui.li\Desktop\zpl\apex.xlsx")  # 文件名以及路径，如果路径或者文件名有中文给前面加一个r拜师原生字符。
        sheet1 = workbook.sheet_by_index(0)
        cols = sheet1.col_values(0)
        print(cols)
        for pn in cols:
            print(pn)
            pn = pn.encode("utf-8")
           # cur.execute('insert into apexpn (pn) values (?) ', [pn])
            x = cur.execute('insert into apexpn (pn) values (?) ', [pn])
            print(x)
            cur.commit()
    except Exception as e:
        print(e)

    return "OK"

@app.route("/exportpn", methods=["POST", "GET"])
def exportpn():
    """
    导出所有的APEX型号
    :return:
    """
    pns = []
    try:
        # 取数据库中
        values = query_db('select pn from apexpn ', one=False)

        for pn in values:
            pns.append(pn["pn"])
        return jsonify(errno="0", errmsg="ok", data=pns)
    except Exception as e:
        print(e)
    return jsonify(errno="1", errmsg="ng", data={})

@app.route("/getinput", methods=["POST", "GET"])
def query_input():
    """
    查询当天产线的投入
    :return:
    """
    # 获取参数
    SN = request.args.get("key[SN]")
    part_sn = request.args.get("key[part_sn]")
    if SN is None and part_sn is None:
        return jsonify(errno="0", code=0, data={})
    # print(SN,part_sn)
    sql = ""
    params = None
    if len(SN) > 0:
        sql = "select * from PartScan where SN = (%s)"
        params = (SN,)
        print(params)

    if len(part_sn) > 0:
        # sql = "SELECT * FROM PartScan WHERE PartSN LIKE %s"
        sql = "SELECT * FROM PartScan WHERE PartSN LIKE '%%%%%s%%%%'" % part_sn
        # print(sql)
        # params = (part_sn,)
        print(params)

    try:
        msconn = connect_msdb()
        mscur = msconn.cursor()
        mscur.execute(sql, params)
        rv = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        datalist = (rv[0] if rv else None) if False else rv
        # datalist = mscur.fetchall()
        mscur.close()
        # msconn.close()
        return jsonify(errno="0", code=0, data=datalist)
    except Exception as e:
        mscur.close()
        # msconn.close()
        print(e)
        return "query failed"

@app.route("/showpartscan", methods=["POST", "GET"])
def showpartscan():
    """
    showpsartscan 页面
    :return:
    """
    return render_template("partscan2.html")

@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    """
    显示投入和产出
    dashboard 页面
    :return:
    """
    return render_template("dashboard.html")

@app.route("/getdashboard", methods=["POST", "GET"])
def getdashboard():
    """
    查询投入和产出
    dashboard 页面
    :return:
    """
    # 定义查询参数
    dt = datetime.datetime.now()
    query_date = dt.strftime("%Y-%m-%d")
    params = (query_date)

    sql = "SELECT COUNT(*) AS input FROM Products WHERE EntryDateTime > (%s) and Family is not null"
    sql_out = "select COUNT(DISTINCT Product) as output_qty from Outcomes where OperationTypeName = 'Manufacturing Kit Check' and EntryDateTime > (%s)"
    print(sql_out)
    try:
        msconn = connect_msdb()
        mscur = msconn.cursor()
        mscur.execute(sql, params)
        rv = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        datalist1 = (rv[0] if rv else None) if False else rv

        mscur.execute(sql_out, params)
        rv1 = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        datalist2 = (rv1[0] if rv1 else None) if False else rv1
        print(datalist2)

        datalist1[0].update(datalist2[0])
        datalist = [datalist1[0]]
        mscur.close()
        # msconn.close()
        return jsonify(errno="0", code=0, data=datalist)
    except Exception as e:
        mscur.close()
        # msconn.close()
        print(e)
        return "query failed"

@app.route("/index", methods=["POST", "GET"])
def showtest():
    """
    显示投入和产出
    dashboard 页面
    :return:
    """
    return render_template("index.html")

@app.route("/dypns", methods=["POST", "GET"])
def dypns():
    """
    查询当天每个机型的投入和产出
    dashboard 页面
    :return:
    """
    try:
        sql_out = "SELECT * FROM PN_DY_OUT"
        sql_in = "SELECT * FROM PN_DY_IN"

        msconn = connect_msdb()
        mscur = msconn.cursor()
        mscur.execute(sql_out)
        rv = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        dy_out = (rv[0] if rv else None) if False else rv
        print(dy_out)

        mscur.execute(sql_in)
        rv = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        dy_in = (rv[0] if rv else None) if False else rv
        print(dy_in)
        mscur.close()
        return jsonify(errno="0", code=0, data_out=dy_out, data_in=dy_in)
    except Exception as e:
        mscur.close()
        # msconn.close()
        print(e)
        return "query failed"


@app.route("/table", methods=["POST", "GET"])
def table():

    try:
        sql = "select * from day_every_hour_out order by Hour"
        msconn = connect_msdb()
        mscur = msconn.cursor()
        mscur.execute(sql)
        rv = [dict((mscur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in mscur.fetchall()]
        dy_hour_out = (rv[0] if rv else None) if False else rv
        # print(dy_hour_out)
        # data: [98, 77, 101, 99, 40]
        data = []
        datax = []
        for item in dy_hour_out:
            data.append(item["out_qty"])
            # print(type(item["Hour"]))
            hour = item["Hour"]
            hour_str = "%s-%s" %(str(hour),str(hour+1))
            datax.append(hour_str)
        mscur.close()
        return jsonify(data=data,datax=datax)
    except Exception as e:
        mscur.close()
        # msconn.close()
        print(e)
        return "query failed"




# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    # connect_msdb()
    manager.run()

