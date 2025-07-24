CREATE TABLE "brand" (
  "id" int PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "category" (
  "id" int PRIMARY KEY,
  "display_text" varchar,
  "description" varchar
);

CREATE TABLE "product" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "description" varchar,
  "sku" varchar,
  "small_image" varchar,
  "out_of_stock" boolean,
  "category_id" int,
  "brand_id" int
);

ALTER TABLE "product" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("id");

ALTER TABLE "product" ADD FOREIGN KEY ("brand_id") REFERENCES "brand" ("id");