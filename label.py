# coding:utf-8
# 导入Flask类
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
import json

#Flask类接收一个参数__name__
app = Flask(__name__)
manager = Manager(app)

# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
	return render_template("label.html")


@app.route('/test')
def index1():
	return render_template("test.html")



@app.route("/label", methods=["POST"])
def printlabel():
    """
    print label
    :return:
    """

    # 1.获取参数
    req_dict = request.get_json()

    # 2.获取参数
    print_part_no = req_dict.get("part_no")
    qty = req_dict.get("qty")
    # pb = bytes(print_part_no, encoding = "utf8")
    print(print_part_no)
    print(qty)
    pn = print_part_no.encode("utf-8")
    qty1 = qty.encode("utf-8").encode()
    pn = pn.encode()
    # pb = str.encode(print_part_no)
    # ns = b"^FO310,23^GFA,04992,04992,00052,:Z64:eJztlT2OGzcYhskwAF0E5nZpDNFALuB0BmJwcpQAuYC7qBCGY2yhLnuD5CimsIWSyjfIUp5iyqWwxXBhmsz7cUaadWEgdSACEsiZefnw+yVjl3EZl3EZl3EZ/3X88pXnvGObefoz0+w8pWG/tplnb86zsyZ+h71YPn/08ktOAIcXDMygsVkXz5L64BhLeF3GgvWGvWUa30y7CHogaCkiM6RR+Caqm65qROlJY/BSLZqFk06cwJPeOtq3HIkTmKWXTzlvqiZj22bm8Ki3vmr68kAcerlopCMEvWbt2R4eGjlpDtUeUL7QdGSKV52BBvaszXPhRTB4VDmH3gtwZx+a+q/+ri6TTrONxdE3RnNorAgT5zg67BHnWLWT5ndweOW8xjdhbTS+8RlbKw9ze+JA03QLR+uzPVeV02qe5SHBBIUQ8WEPe2RgjcPbNHFMEzcrMZmHp35tjICGDFBkaX+LhyBq12Bpzho9cdhkj+VZj2RAPcEITtCO6bBwmhTXJ86UB5lnNZABTeVcgwNjVFg49nOYOTKTW2zesKTvEfrOkneqPbZzMj3hROKQ30SeOK/hmMGDU5NwuCYvMi/y4jf7SByKDziWNFfYaKjOxIqXrRMH5CKt2FxqTYhpxWeO7aChh0jmQjsbcU+cJCh5zpwfjyGf7bGObVpbkiWNxM7tZM9GRraWmLRzXsc8+80wZPDa2BLtR/ypyR6KzytUzEvSTBy5eyxzfFqOSkF8wEEwYs03PlL9XCERrqAJ7ZzXj+WPqX4MLziCKSX+BPuifl/jU+uUUm/hqO5Y7maOKGmy5zev3yVNQeTH2g+082yxR6VPwz8wi5wijxkcdJ0fiPO85oHvB2R0cw0NimLO6884MZUrnKSOpbN5xeP34MQXVOng7HcI8DbgE+lPeVD6zOQH9w0zGolls+FBeN3FZ4bi4z/1B2hQQU855bZwuQ+KtY1rPPqBDGgGqLmG4nMY9+PUdxaOjuUdRSFoZmynoFFbRL5h0JA9h4e+UDHlJ5wXvPA7Oe6i7trSaQfOnZOhcmrSjTvqd0jFJT7wEluJYfcRGWeY6KKRpQOHz5z7hwPWdNAlPtSwtdy7/Y1rV3D5poVGeovHNT7g4FhUTkt8eAYHGjG4/IyolN8CL0+cHtWjqJwWDuqUabV3MKn8hS0iMojBQZPfLPrBrtTW7UizOfUDtlIorJ78UzlkT5puCSMGMbynVoCG5U49kTgWt4DcU22Wx9Cix6O/IcVrfLwsfybioJRhyImjEMZSbm+p0GIwTYmij9AYFC16aLkJatbMPd4iMkWRRuzovkEa3xU5hsqxGZ2ibGvrpoOXWuDsFe60TBddJ6jRHPtcrpO49xaXGw5B18M1fk6QxsY5pkEl0jBOjTOMCU1GDh6tAZwEDm6Ab2sYoUmnPIDmdFLGfo1rthZ9hxYETqA7Yrq1XW1SpzxQ82xevkXpH5almGcdcRy7jMu4jMv4/45/AZfTu+Y=:A33A"
    supplier = b"^XA^FX Top section with company logo, name and address.^CF0,60,50^FO80,50^FDSUPPILER : ^FS"
    ns = b"^FO310,15^GFA,05760,05760,00060,:Z64:eJztlj+OFDkUxl9tIUyAMCEBwhxhww1Qm6NwBMINmnK1OpiQI/RR1iOQOuQIU6MOOtvxiGAsrbH3e8/urgK0m5K0R+qpKtdXP7+/NtFlXMZlXMZlXMZl/ILxgij+33w//vfcK6J0un5ENJwnntZ/avHl7getHZlrC8b4VLS6TLZMpMfXNDatK7tSAvWeJur51dy0XeJJ1jpcEJkSHF40wRoPbZi1KvShakvV0swtjRssXtRetHpacGMfl1on9p65w8z1znglL4YzVyVSs3ZYcGH7yV5ox0FPFRKbFvdpaW+i2V6scWGvL+B8pzWhy8s1J54eV7DbjGYS7jas4BM7ZnXiDmY34hHmM528hJCJ1jsAzaiD2PspDF0gh6nGDWtjiD/nqQJ5edDGqxPXjrpxp6GfyPYJfm3clRllKVRqmq1Ee/9QPcxrVntcJ7MFN5KDNjXC2orWjeT8zO1D9bD89ryGCHtzX8YMKrRiILjsK0Ct1/x9sVfd18jK72+qcVMHrWKvdqJdD6ztYKwJht8RrjqUKerGlbiDOyXmavZqX7mi5WsdmJvFXv3p4TqZxqXKLV/B3RTDixRH03rNWiQVmTRzdTlO0XzPLV8jlU228HXTDqwIGgmo02yvKUdwfeNKbptyD5f2GS514hlwRWviY1JZL7h7trfGF1WbJJ/fIQAZEbGTkeQdIsfITv3Ylzm+puzFXo7vBq4ULpesKtAaL8bQB9G6ANfX5Gjcq1tM1HwuUydc1upsJVmrvZXrYfG56vnzqnIdcycJ4fYr1qkzyzx/x9GHaq83oTU04T5eqdt8im9B3YzI54No+dmGtasWX82F9Ib4k6v6BXVdWnw3rPWVWwz+yreryl07iS98Ry+6WneSMsisU3y5T6BBtjWjhtK2FvpgJZ+5CEm4ttX+vpziqyZVIuqXtSYjLVJrTqhf0Tr/lhbcCO7HM1eX1Ox9hqhS6v+p8TXSc5CjnmZ7uwjuTctnzUUCe8NzymaQzvHQuLud/x1IdOuZ25fj3d0N4v2MYzrZA75Qwh+UGvdQ7dW7jyO0GV0Jqad9i+/xy55zxfDN5K6LR16tu/RIuP2++tncaI+2npRoTeVCe8faARkIeznGyGf0DFCZ29f4gnsr2li5q1YL+BvfOueVV7foIIH7M95xzO3UiXv1gC0hKWnnZ+6+bMv452Am9NhDIRuhtVcBPSOj4zHXsp+3d5l05NaxsHdfuuKRdEhXdczSkIL7wombu7b70IdyI5HnljVz+6j+pi9jHtSkvT7g5clsJ3vHnTpT3X3g8bLbIuOQkmUR357U585sklOfTdD3eNkjvgZpzdbO3N2GH2FfGBd5BRAqNw399uOkJ4R+hFbD81hx13Zb5m5A5N4+LvLZHlE5mzR06hhMeMetpMc2hCJZcNfFcGWz3M9c7pOkN3FApw5WziW2n9idA2Jc/Yz4ZjSVkfs8rD7ba8oDV2x0pB6Cy1ULLoxTkbk1vgHFUDfF8AMX2oH0IeJh1Rp8Pms5XdT4gvFX3RSjHKlc68+e7D6gXd1+k2LNTsm+P5j7cubiPSloaLkdduXEteVqQhFeT9Le8qocJKb2tgiXr3Eg0enM7et5wySFwtkE1nbJSc/H700ZB9RUJO7I8DO0KrGlhVfc1fPGM06kMr62vKVE3gXiCkW8LZTR+5bcbRRtFm07djBXDjojvZd98KV7yDBocBs5UrF2TS51WEE9FFFX0imvdGaf4ec1xy4+tZ8icnlYcTCZm5g70Xs+XhLvGXTWepO5nnD7Vh68tDjlvCH3ivcecF1gPxM9l/42CTeeuT8doEd6QvnJfD/Qk+/mJQ8u4zIu45eOfwEzUDEx:816E"
    # part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO: 690300236200^FS"
    part_no = b"^CF0,60,50^FO80,120^FDPRIMAX PART NO:"+ pn + b"^FS"
    part_name = b"^FO80,190^FDPART NAME: 1.0 ZIF FPC SMT R/A B/C^FS"
    ship_to = b"^FO80,260^FDShip to : Primax SSG^FS"
    # qty = b"^FO750,260^FDQty : 6000 pcs^FS"
    qty = b"^FO750,260^FDQty : " + qty1 + b" pcs^FS"
    barcode = b"^FX Third section with barcode.^BY4,3,95^FT84,413^BCN,,N,N^FD>;2600430381001001>6->56000>6->5180709^FS"
    gr2 = b"^FO880,30^GB200,90,12^FS^FT905,95^A0N,60,60^FH\^FDG+R2^FS"
    barcode_text = b"^CF0,40,40^FO350,420^FD2600430381001001-6000-180709^FS^XZ"

    # 拼接完整的斑马打印指令
    z = supplier + ns + part_no + part_name + ship_to + qty + barcode + gr2 + barcode_text

    import socket
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        
        mysocket.send(z)
       
        mysocket.close()  # closing connection
    except Exception as e:
		print(e)

    return jsonify(errno="0", errmsg="ok", data={"real_name": print_part_no})

# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    manager.run()