from flask.cli import FlaskGroup
from app import app, db
from app.models.contact import Contact
import qrcode

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
@cli.command("create_db")
def create_db():
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

    def gennerate_qrcode(id):
        img = qrcode.make('google.com') # Must to change to menu select url
        type(img)  # qrcode.image.pil.PilImage
        img.save(f"app/static/qrcode/{id}.png")
        return f"app/static/qrcode/{id}.png"

    for i in range(1, 21):
        db.session.add(Tables(table_id=i, qrcode=gennerate_qrcode(i)))
    # db.session.add(Tables(table_id=1, qrcode='/static/qrcode/1.png'))
    # db.session.add(Tables(table_id=2, qrcode='/static/qrcode/2.png'))
    db.session.commit()

    #?-------------------------------------------------------------------------
    # สร้างข้อมูลเมนู
    sample_menus = [
    # อาหารคาว
    ('ข้าวผัด', 'ข้าวผัดหมู', 50, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ไก่ย่าง', 'ไก่ย่างสูตรพิเศษ', 100, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ต้มยำกุ้ง', 'ต้มยำกุ้งรสแซ่บ', 150, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('แกงเขียวหวานไก่', 'แกงเขียวหวานไก่รสเข้มข้น', 120, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ผัดกะเพรา', 'ผัดกะเพราหมูสับไข่ดาว', 70, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('หมูทอดกระเทียม', 'หมูทอดกระเทียมพริกไทย', 90, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ปลาทอดน้ำปลา', 'ปลากะพงทอดน้ำปลา', 180, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ไข่พะโล้', 'ไข่พะโล้ใส่หมูสามชั้น', 80, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ข้าวมันไก่', 'ข้าวมันไก่สูตรต้นตำรับ', 75, 'อาหารคาว', '/static/food_image/test0.jpg'),
    ('ข้าวหมูแดง', 'ข้าวหมูแดงราดน้ำซอสหวาน', 70, 'อาหารคาว', '/static/food_image/test0.jpg'),

    # อาหารไทย
    ('ส้มตำ', 'ส้มตำไทย', 60, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ลาบหมู', 'ลาบหมูรสเด็ด', 80, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('น้ำตกเนื้อ', 'น้ำตกเนื้อย่างจิ้มแจ่ว', 120, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ต้มแซ่บกระดูกหมู', 'ต้มแซ่บกระดูกอ่อน', 130, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ข้าวเหนียวไก่ทอด', 'ข้าวเหนียวไก่ทอดสูตรเด็ด', 75, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ข้าวซอยไก่', 'ข้าวซอยไก่สูตรเชียงใหม่', 100, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('แกงส้มชะอมไข่', 'แกงส้มชะอมไข่กุ้งสด', 120, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ห่อหมกทะเล', 'ห่อหมกทะเลเครื่องแน่น', 150, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('ขนมจีนน้ำยา', 'ขนมจีนน้ำยาใต้รสเข้มข้น', 90, 'อาหารไทย', '/static/food_image/test0.jpg'),
    ('หมูปิ้ง', 'หมูปิ้งไม้ละ 10 บาท', 10, 'อาหารไทย', '/static/food_image/test0.jpg'),

    # อาหารฝรั่ง
    ('Pizza', 'Pizza อิตาลี', 200, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('สเต็กหมู', 'สเต็กหมูซอสพริกไทยดำ', 180, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('สเต็กเนื้อ', 'สเต็กเนื้อริบอายซอสเกรวี่', 350, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('พาสต้า', 'พาสต้าคาโบนาร่า', 160, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('เบอร์เกอร์เนื้อ', 'เบอร์เกอร์เนื้อชีส', 140, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('ซุปเห็ด', 'ซุปครีมเห็ดทรัฟเฟิล', 120, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('สปาเก็ตตี้โบโลเนส', 'สปาเก็ตตี้ซอสโบโลเนส', 150, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('แซนด์วิชแฮมชีส', 'แซนด์วิชแฮมชีสกรอบ', 100, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('ซีซาร์สลัด', 'ซีซาร์สลัดไก่กรอบ', 130, 'อาหารฝรั่ง', '/static/food_image/test0.jpg'),
    ('Fish and Chips', 'ปลาทอดกรอบเสิร์ฟพร้อมมันฝรั่งทอด', 190, 'อาหารฝรั่ง', '/static/food_image/test0.jpg')
    ]

    for name, desc, price, cat, image_url in sample_menus:
        db.session.add(Menu(name=name, description=desc, price=price, category=cat, image_url=image_url))

    #?-------------------------------------------------------------------------
    # สร้างข้อมูลพนักงาน
    sample_employees = [
    ('ธนารักษ์', 'กันยาประสิทธิ์', '081-111-1111', 'Admin'),
    ('ทิวัตถ์', 'ทาจุมปู', '082-222-2222', 'Best manager ever'),
    ('กฤตภาส', 'เกตุกำเนิด', '083-333-3333', 'Chef'),
    ('พ่อใหญ่นน', 'เทพสุข', '084-444-4444', 'Waiter'),
    ('สุริยา', 'จันทร์สว่าง', '085-555-5555', 'Cashier'),

    ('นที', 'วงศ์เจริญ', '086-111-1111', 'Let me close my eyes with dignity'),
    ('จิรายุ', 'ทองดี', '087-222-2222', 'Let\'s end it all, the world\'s not far behind'),
    ('พีรพัฒน์', 'เกษมสุข', '088-333-3333', 'So what\'s the point of staying?'),
    ('กันตภณ', 'ศิริวัฒน์', '089-444-4444', 'It\'s going up in flames, I know'),
    ('สุวัฒน์', 'ปรีชาธรรม', '090-555-5555', 'Yes, I know, ooh'),
    
    ('ภาณุวัฒน์', 'อินทรีทอง', '091-666-6666', 'Oh-oh-oh'),
    ('อริยะ', 'โชติพงษ์', '092-777-7777', 'Hey-hey Oh-oh (Hey)'),
    ('รัชพล', 'ศรีสุข', '093-888-8888', 'Just hold my heartbeat close to you'),
    ('ศิวกร', 'ไพศาล', '094-999-9999', 'Remember how it always beats for you'),
    ('สิรวิชญ์', 'พรหมวิเศษ', '095-000-0000', 'I\'m falling at the speed of light'),

    ('ธวัชชัย', 'สุนทรกุล', '096-111-1111', 'I\'m staring at your shrinking face, don\'t cry'),
    ('ปริญญา', 'อุดมทรัพย์', '097-222-2222', 'You know my heart belongs to you'),
    ('วิชัย', 'เดชาศิลป์', '098-333-3333', 'One last time, say that you want me too'),
    ('เอกชัย', 'สมบูรณ์', '099-444-4444', 'The only words that gave me life'),
    ('จักรพงษ์', 'โชติภักดี', '080-555-5555', 'Now I\'ll see you on the other side'),

    ('ปิยะ', 'เศรษฐวิทยา', '081-666-6666', 'Oh-oh, oh-oh, oh-oh'),
    ('ณัฐพล', 'ทองกาญจน์', '082-777-7777', 'Oh-oh, oh-oh, oh-oh'),
    ('ชัยวัฒน์', 'พงศ์เจริญ', '083-888-8888', 'Oh-oh, oh-oh, oh-oh'),
    ('อธิป', 'จันทร์สม', '084-999-9999', 'Oh-oh, oh-oh, oh-oh'),

    ('สรวิชญ์', 'ภูมิวัฒน์', '085-000-0000', 'Oh, mama, I\'ll pray'),
    ('กฤษณะ', 'นวลศรี', '086-111-1111', 'I\'m running away'),
    ('อานนท์', 'เทวะ', '087-222-2222', 'Oh-oh Hey-hey (Oh, no)'),
    ('วิทยา', 'ศักดิ์ศรี', '088-333-3333', 'Is a threat not a promise? (Mmm)'),
    ('ธนกฤต', 'รุ่งเรือง', '089-444-4444', 'If you\'re looking for rage (Mmm, oh)'),

    ('ภาสกร', 'จิรเดช', '090-555-5555', 'If you\'re looking for ragin\''),
    ('พงศกร', 'ธรรมเจริญ', '091-666-6666', 'Quiet for days'),
    ('อนันต์', 'โชคชัย', '092-777-7777', 'Baby, running away'),
    ('วีระ', 'ศรีวัฒน์', '093-888-8888', 'Ayy-yeah'),
    ('นภดล', 'แสงจันทร์', '094-999-9999', 'It\'s a threat, not a promise'),
    ]

    for fname, lname, phone, role in sample_employees:
        db.session.add(Employee(firstname=fname, lastname=lname, phone=phone, role=role))
    
    #?-------------------------------------------------------------------------
    # สร้างข้อมูลคำสั่งซื้อ
    import random
    from datetime import datetime, timedelta

    payment_methods = ["cash", "credit_card", "paypal", "bank_transfer"]
    start_time = datetime(2024, 2, 12, 10, 0, 0)

    sample_payments = [
    [
        str(i + 1),  # order_id
        random.choice(payment_methods),  # payment_method
        (start_time + timedelta(minutes=i * 5)).strftime("%Y-%m-%d %H:%M:%S"),  # payment_time
        str(random.randint(100, 5000))  # amount
    ]
    for i in range(100)
    ]

    for order_id, payment_method, payment_time, amount in sample_payments:
        db.session.add(Payment(order_id=order_id, payment_method=payment_method, payment_time=payment_time, amount=amount))   

    #?-------------------------------------------------------------------------
    # เพิ่มเติม Contact 
    for i in range(1, 21):
        db.session.add(Contact(firstname=f'John{i}', lastname=f'Doe{i}', phone=f'12345678{i}'))
    
    db.session.commit()

if __name__ == "__main__":
    cli()
