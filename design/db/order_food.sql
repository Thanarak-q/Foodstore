CREATE TABLE "Table"(
    "table_id" INTEGER NOT NULL,
    "qrcode" CHAR(255) NOT NULL,
    "status" CHAR(255) NOT NULL
);
ALTER TABLE
    "Table" ADD PRIMARY KEY("table_id");
CREATE TABLE "menu"(
    "menu_id" INTEGER NOT NULL,
    "name" CHAR(255) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "category" CHAR(255) NOT NULL,
    "image_url" CHAR(255) NOT NULL,
    "availability" CHAR(255) NOT NULL
);
ALTER TABLE
    "menu" ADD PRIMARY KEY("menu_id");
CREATE TABLE "orders"(
    "order_id" INTEGER NOT NULL,
    "table_name" INTEGER NOT NULL,
    "order_time" TIME(0) WITHOUT TIME ZONE NOT NULL,
    "status" CHAR(255) NOT NULL,
    "menu_id" INTEGER NOT NULL
);
ALTER TABLE
    "orders" ADD PRIMARY KEY("order_id");
CREATE TABLE "payment"(
    "payment_id" INTEGER NOT NULL,
    "order_id" INTEGER NOT NULL,
    "payment_method" CHAR(255) NOT NULL,
    "payment_time" TIME(0) WITHOUT TIME ZONE NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL
);
ALTER TABLE
    "payment" ADD PRIMARY KEY("payment_id");
CREATE TABLE "employee"(
    "em_id" BIGINT NOT NULL,
    "firstname" CHAR(255) NOT NULL,
    "lastname" CHAR(255) NOT NULL,
    "phone" CHAR(255) NOT NULL,
    "role" CHAR(255) NOT NULL
);
ALTER TABLE
    "employee" ADD PRIMARY KEY("em_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_table_name_foreign" FOREIGN KEY("table_name") REFERENCES "payment"("order_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_table_name_foreign" FOREIGN KEY("table_name") REFERENCES "Table"("table_id");
ALTER TABLE
    "orders" ADD CONSTRAINT "orders_menu_id_foreign" FOREIGN KEY("menu_id") REFERENCES "menu"("menu_id");