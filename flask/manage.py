from flask.cli import FlaskGroup
from app import app, db
from werkzeug.security import generate_password_hash

import jwt
import datetime 
import qrcode
import secrets
import random


#!-------------------------------------------------------------------------
''' 
base เก็บข้อมูลพทัวไป
: Table สำหรับเก็บข้อมูลโต๊ะ
: Menu สำหรับเก็บข้อมูลเมนูอาหาร
: Employee สำหรับเก็บข้อมูลพนักงาน
'''
# from app.models.base import CTable
from app.models.menu import Menu
from app.models.employee import Employee
from app.models.table import Tables
from app.models.order import Order
from app.models.review import Review
from app.models.store import Store
# from app.models.employee import AuthUser

'''
buy 
: Order สำหรับเก็บข้อมูลคำสั่งซื้อ
: OrderDetail สำหรับเก็บข้อมูลรายละเอียดคำสั่งซื้อ
'''
# from app.models.buy import Order, OrderDetail

'''
payment เก็บข้อมูลการชำระเงิน
: Payment สำหรับเก็บข้อมูลการชำระเงิน
'''
from app.models.payment import Payment

'''
docker compose exec db psql --username=Pladug --dbname=Pladug_dev
to see database
'''

#!-------------------------------------------------------------------------

cli = FlaskGroup(app)
SECRET_KEY = 'wail to generate'

@cli.command("create_db")
def create_db():
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()



@cli.command("seed_db")
def seed_db():
    '''
    add base
    '''
    #?-------------------------------------------------------------------------
    # สร้างข้อมูลโต๊ะ
    # for i in range(1, 21):
    #     db.session.add(CTable(status='Available'))
    # db.session.add(CTable(ctable_name="t1", status='Occupied'))
    # db.session.add(CTable(ctable_name="t2", status='Occupied'))

    def gennerate_qrcode(id, count):
        token = generate_jwt(id, count)
        img = qrcode.make(f'http://localhost:56733/menu/table/{token}') # Must to change to menu select url
        type(img)  # qrcode.image.pil.PilImage
        img.save(f"app/static/qrcode/{id}.png")
        return f"app/static/qrcode/{id}.png"

    def generate_jwt(table_number, count):
        expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=48)
        payload = {
            'table_number': table_number,
            'exp': expiration_time,
            'count' : count
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token


    for i in range(1, 21):
        qrCode = gennerate_qrcode(i, count=0)
        db.session.add(Tables(qrcode=qrCode))
    # db.session.add(Tables(table_id=1, qrcode='/static/qrcode/1.png'))
    # db.session.add(Tables(table_id=2, qrcode='/static/qrcode/2.png'))
    db.session.commit()

    #?-------------------------------------------------------------------------
    # สร้างข้อมูลเมนู
    sample_menus = [
    # อาหารคาว
    ('ข้าวผัด', 'ข้าวผัดหมู', 50, 'อาหารคาว', '/static/food_image/ข้าวผัด.jpg'),
    ('ไก่ย่าง', 'ไก่ย่างสูตรพิเศษ', 100, 'อาหารคาว', '/static/food_image/ไก่ย่าง.jpg'),
    ('ต้มยำกุ้ง', 'ต้มยำกุ้งรสแซ่บ', 150, 'อาหารคาว', '/static/food_image/ต้มยำกุ้ง.jpg'),
    ('แกงเขียวหวานไก่', 'แกงเขียวหวานไก่รสเข้มข้น', 120, 'อาหารคาว', '/static/food_image/แกงเขียวหวานไก่.jpg'),
    ('ผัดกะเพรา', 'ผัดกะเพราหมูสับไข่ดาว', 70, 'อาหารคาว', '/static/food_image/ผัดกะเพรา.jpg'),
    ('หมูทอดกระเทียม', 'หมูทอดกระเทียมพริกไทย', 90, 'อาหารคาว', '/static/food_image/หมูทอดกระเทียม.jpg'),
    ('ปลาทอดน้ำปลา', 'ปลากะพงทอดน้ำปลา', 180, 'อาหารคาว', '/static/food_image/ปลาทอดน้ำปลา.jpg'),
    ('ไข่พะโล้', 'ไข่พะโล้ใส่หมูสามชั้น', 80, 'อาหารคาว', '/static/food_image/ไข่พะโล้.jpg'),
    ('ข้าวมันไก่', 'ข้าวมันไก่สูตรต้นตำรับ', 75, 'อาหารคาว', '/static/food_image/ข้าวมันไก่.jpg'),
    ('ข้าวหมูแดง', 'ข้าวหมูแดงราดน้ำซอสหวาน', 70, 'อาหารคาว', '/static/food_image/ข้าวหมูแดง.jpg'),

    # อาหารไทย
    ('ส้มตำ', 'ส้มตำไทย', 60, 'อาหารไทย', '/static/food_image/ส้มตำ.jpg'),
    ('ลาบหมู', 'ลาบหมูรสเด็ด', 80, 'อาหารไทย', '/static/food_image/ลาบหมู.jpg'),
    ('น้ำตกเนื้อ', 'น้ำตกเนื้อย่างจิ้มแจ่ว', 120, 'อาหารไทย', '/static/food_image/น้ำตกเนื้อ.jpg'),
    ('ต้มแซ่บกระดูกหมู', 'ต้มแซ่บกระดูกอ่อน', 130, 'อาหารไทย', '/static/food_image/ต้มแซ่บกระดูกหมู.jpg'),
    ('ข้าวเหนียวไก่ทอด', 'ข้าวเหนียวไก่ทอดสูตรเด็ด', 75, 'อาหารไทย', '/static/food_image/ข้าวเหนียวไก่ทอด.jpg'),
    ('ข้าวซอยไก่', 'ข้าวซอยไก่สูตรเชียงใหม่', 100, 'อาหารไทย', '/static/food_image/ข้าวซอยไก่.jpg'),
    ('แกงส้มชะอมไข่', 'แกงส้มชะอมไข่กุ้งสด', 120, 'อาหารไทย', '/static/food_image/แกงส้มชะอมไข่.jpg'),
    ('ห่อหมกทะเล', 'ห่อหมกทะเลเครื่องแน่น', 150, 'อาหารไทย', '/static/food_image/ห่อหมกทะเล.jpg'),
    ('ขนมจีนน้ำยา', 'ขนมจีนน้ำยาใต้รสเข้มข้น', 90, 'อาหารไทย', '/static/food_image/ขนมจีนน้ำยา.jpg'),
    ('หมูปิ้ง', 'หมูปิ้งไม้ละ 10 บาท', 10, 'อาหารไทย', '/static/food_image/หมูปิ้ง.jpg'),

    # อาหารฝรั่ง
    ('Pizza', 'Pizza อิตาลี', 200, 'อาหารฝรั่ง', '/static/food_image/Pizza.jpg'),
    ('สเต็กหมู', 'สเต็กหมูซอสพริกไทยดำ', 180, 'อาหารฝรั่ง', '/static/food_image/สเต็กหมู.jpg'),
    ('สเต็กเนื้อ', 'สเต็กเนื้อริบอายซอสเกรวี่', 350, 'อาหารฝรั่ง', '/static/food_image/สเต็กเนื้อ.jpg'),
    ('พาสต้า', 'พาสต้าคาโบนาร่า', 160, 'อาหารฝรั่ง', '/static/food_image/พาสต้า.jpg'),
    ('เบอร์เกอร์เนื้อ', 'เบอร์เกอร์เนื้อชีส', 140, 'อาหารฝรั่ง', '/static/food_image/เบอร์เกอร์เนื้อ.jpg'),
    ('ซุปเห็ด', 'ซุปครีมเห็ดทรัฟเฟิล', 120, 'อาหารฝรั่ง', '/static/food_image/ซุปเห็ด.jpg'),
    ('สปาเก็ตตี้โบโลเนส', 'สปาเก็ตตี้ซอสโบโลเนส', 150, 'อาหารฝรั่ง', '/static/food_image/สปาเก็ตตี้โบโลเนส.jpg'),
    ('แซนด์วิชแฮมชีส', 'แซนด์วิชแฮมชีสกรอบ', 100, 'อาหารฝรั่ง', '/static/food_image/แซนด์วิชแฮมชีส.jpg'),
    ('ซีซาร์สลัด', 'ซีซาร์สลัดไก่กรอบ', 130, 'อาหารฝรั่ง', '/static/food_image/ซีซาร์สลัด.jpg'),
    ('Fish and Chips', 'ปลาทอดกรอบเสิร์ฟพร้อมมันฝรั่งทอด', 190, 'อาหารฝรั่ง', '/static/food_image/Fish_and_Chips.jpg'),

    #mk
    ('Michael_jackson', 'ตายแล้ว', 17, 'hehe annie are u ok ', '/static/food_image/Michael_jackson.jpg')
    ]


    for name, desc, price, cat, image_url in sample_menus:
        db.session.add(Menu(name=name, description=desc, price=price, category=cat, image_url=image_url))

    #?-------------------------------------------------------------------------
    # สร้างข้อมูล Order

    def cal_price(menu_list):
        db_allmenus = Menu.query.all()
        menus = list(map(lambda x: x.to_dict(), db_allmenus))
        menus.sort(key=(lambda x: int(x['id'])))
        app.logger.debug(f"DB Get menus data to cal_price() in Order")

        total = 0
        # note menu_list key start at 0 but menus start at 1
        for key in menu_list:
            # app.logger.debug(f"{key} : {int(menus[key - 1]['price']) * menu_list[key]}")
            total += int(menus[key - 1]['price']) * menu_list[key]
            plus_menu_ordered(key, menu_list[key])
            
        return total

    def plus_menu_ordered(menu_id, amount):
        menu = Menu.query.get(menu_id)
        menu.update_ordered(amount)
        db.session.commit()
    
    def random_date(start_year=2023):
            start_date = datetime.date(start_year, 1, 1)
            end_date = datetime.date(start_year+6, 5, 5)
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            random_date = start_date + datetime.timedelta(days=random_days)
            return random_date

    # ใช้สุ่มค่าเวลาในโค้ดหลัก
    large_list = [{
        random.randint(1, 20): random.randint(1, 10) for _ in range(random.randint(1, 5))
    } for _ in range(700)]

    for menu_list in large_list:
        temp = Order(
            table_id=random.randint(1, 20),
            time=random_date(),
            menu_list=menu_list
        )
        temp.change_price(cal_price(menu_list))
        db.session.add(temp)
        
    db.session.commit()

    #?-------------------------------------------------------------------------
    # สร้างข้อมูลพนักงาน
    sample_employees = [
    ('User1', '1234' ,'ธนารักษ์', 'กันยาประสิทธิ์', '081-111-1111', 'Admin'),
    ('User2', '1234' ,'ทิวัตถ์', 'ทาจุมปู', '082-222-2222', 'Chef'),
    ('User3', '1234' ,'หวัง', 'รอยเลื่อน', '082-222-2222', 'Waiter'),
    ('User4', '1234' ,'เถื่อน', 'เลอะเลือน', '082-222-2222', 'Cashier'),
    ]

    for user, password, fname, lname, phone, role in sample_employees:
        db.session.add(Employee(username=user, 
                                password=generate_password_hash(password,method='sha256')
                                , firstname=fname
                                , lastname=lname
                                , phone=phone
                                , role=role))

    #?-------------------------------------------------------------------------
    payment_methods = ["cash", "credit_card", "paypal", "bank_transfer"]
    start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)  # เริ่มตั้งแต่ปี 2015

    num_payments = 19

    years = 3  # กำหนดจำนวนปีที่ต้องการ

    sample_payments = [
        [
            str(i + 1),  # table_id
            random.choice(payment_methods),  # payment_method
            (start_time + datetime.timedelta(days=random.randint(0, 365 * years),  # สุ่มวันที่ในช่วง 5 ปี
                                            hours=random.randint(0, 23),
                                            minutes=random.randint(0, 59))
            ).strftime("%Y-%m-%d %H:%M:%S"),  # payment_time
            str(random.randint(100, 5000))  # amount
        ]
        for i in range(num_payments)
    ]

    for table_id, payment_method, payment_time, amount in sample_payments:
        db.session.add(Payment(table_id=table_id, payment_method=payment_method, payment_time=payment_time, amount=amount))

    #?-------------------------------------------------------------------------
    db.session.add(Review(name='people1', star=5, review='แซ่บหลาย'))
    db.session.add(Review(name='people2', star=5, review='เฮาคนสุพัน'))
    db.session.add(Review(name='people-', star=5, review='that crazy i can  eat MJ WTH'))
    db.session.commit()
    #?-------------------------------------------------------------------------

    db.session.add(Store(name = "ปลาดุกทอด", vat = 7.0, service_charge = 0 , Max_Orders_per_Round = 5, Max_Food_Quantity_per_Order = 100))
    db.session.commit()

@cli.command("secret_key")
def generate_secret_key():
    SECRET_KEY = secrets.token_hex(32)

if __name__ == "__main__":
    cli()