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
# from app.models.base import CTable, Menu, Employee
from app.models.table import Tables
from app.models.menu import Menu
from app.models.employee import Employee

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
# from app.models.payment import Payment


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
    # db.session.add(CTable(ctable_name="t1", status='Occupied'))
    # db.session.add(CTable(ctable_name="t2", status='Occupied'))

    db.session.add(Tables(table_id=1, qrcode='/static/qrcode/1.png'))
    db.session.add(Tables(table_id=2, qrcode='/static/qrcode/2.png'))
    db.session.commit()

    #?-------------------------------------------------------------------------
    # สร้างข้อมูลเมนู
    db.session.add(Menu(name='ข้าวผัด',
                        description='ข้าวผัดหมู', 
                        price=50, 
                        category='อาหารคาว', 
                        image_url='มาฮั้ฮัโตะ'))
    
    db.session.add(Menu(name='Pizza', 
                        description='Pizza', 
                        price=10, 
                        category='อาหารอิตารี่', 
                        image_url='มาฮั้ฮัโตะ'))
    
    db.session.add(Menu(name='ไก่ย่าง', 
                        description='ไก่ย่างจากญี่ปุ่น', 
                        price=50, 
                        category='อาหารคาว', 
                        image_url='มาฮั้ฮัโตะ'))

    # #?-------------------------------------------------------------------------
    # สร้างข้อมูลพนักงาน
    db.session.add(Employee(firstname='ธนารักษ์', 
                             lastname='กันยาประสิทธิ์', 
                             phone='081-111-1111', 
                             role='Admin'))
    db.session.add(Employee(firstname='ทิวัตถ์', 
                             lastname='ทาจุมปู', 
                             phone='082-222-2222', 
                             role="i tell you it's a threat not a promise"))
    db.session.add(Employee(firstname='กฤตภาส',
                            lastname='เกตุกำเนิด', 
                            phone='083-333-3333', 
                            role='chicken hunter'))
    db.session.add(Employee(firstname='พ่อใหญ่นน',
                            lastname='เทพสุข', 
                            phone='084-444-4444', 
                            role='darkknights'))
    # #?-------------------------------------------------------------------------
    # # สร้างคำสั่งซื้อ (orders) และรายละเอียดการสั่งซื้อ (order_details)
    # # สมมติว่าโต๊ะที่ 1 สั่งข้าวผัด 2 จานและไก่ย่าง 1 จาน
    # order = Order(table_name=1, status="Preparing", total_price=150)
    # db.session.add(order)
    # db.session.flush()  # ใช้เพื่อให้ `order_id` ถูกสร้างขึ้น

    # # รายการคำสั่งซื้อ
    # db.session.add(OrderDetail(order_id=order.order_id, menu_id=1, quantity=2, price_per_unit=50))
    # db.session.add(OrderDetail(order_id=order.order_id, menu_id=3, quantity=1, price_per_unit=50))

    #?-------------------------------------------------------------------------
    # db.session.add(Contact(firstname='John', lastname='Doe', phone='123456789'))
    # db.session.commit()



if __name__ == "__main__":
    cli()
