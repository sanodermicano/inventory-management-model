import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

product_df = pd.DataFrame(columns=['ProductCode', 'ProductName', 'ProductCategory', 'ProductDescription', 'UnitPrice', 'Supplier'])
sales_df = pd.DataFrame(columns=['SalesDate', 'CustomerName', 'ProductCode', 'SalesQuantity'])
inventory_df = pd.DataFrame(columns=['ProductCode', 'InventoryDate', 'InventoryStart', 'InventoryEnd'])

product_mapping = {
    'Surgical Mask': 'Medical Supplies',
    'Ventilator': 'Medical Devices',
    'PPE Kit': 'Medical Supplies',
    'Antibiotics': 'Medications',
    'Vaccine': 'Medications',
    'Medical Gloves': 'Medical Supplies',
    'Thermometer': 'Medical Devices',
    'Face Shield': 'Medical Supplies',
    'Sanitizer': 'Medical Supplies',
    'Syringe': 'Medical Supplies',
    'Oxygen Concentrator': 'Medical Devices',
    'Wheelchair': 'Medical Devices',
    'Blood Pressure Monitor': 'Medical Devices',
    'Crutches': 'Medical Supplies',
    'IV Bag': 'Medical Supplies',
    'Defibrillator': 'Medical Devices',
    'Stethoscope': 'Medical Devices',
    'Orthopedic Implants': 'Medical Devices',
    'Nebulizer': 'Medical Devices',
    'X-ray Machine': 'Medical Devices',
    'Ultrasound Machine': 'Medical Devices',
    'MRI Scanner': 'Medical Devices',
    'Wheelchair Ramp': 'Medical Devices',
    'Catheters': 'Medical Supplies',
    'Dental Chair': 'Medical Devices',
    'Hearing Aids': 'Medical Devices',
    'Sterile Gauze': 'Medical Supplies',
    'Nurse Uniforms': 'Medical Apparel',
    'Blood Glucose Monitor': 'Medical Devices',
    'Intraocular Lens': 'Medical Devices',
    'Dialysis Machine': 'Medical Devices',
    'ECG Machine': 'Medical Devices',
    'Infusion Pump': 'Medical Devices',
    'Orthopedic Shoes': 'Medical Supplies',
    'Wound Dressing': 'Medical Supplies',
    'Diagnostic Reagents': 'Medical Supplies',
    'Hospital Bed': 'Medical Devices',
    'Dental Implants': 'Medical Devices',
    'Prosthetic Limbs': 'Medical Devices',
    'Dermatology Creams': 'Medications',
    'Orthopedic Braces': 'Medical Supplies',
    'Ambulance Stretcher': 'Medical Devices',
    'Hearing Aid Batteries': 'Medical Supplies',
    'Laboratory Microscopes': 'Medical Devices',
    'Pulse Oximeter': 'Medical Devices',
    'Respiratory Masks': 'Medical Supplies',
    'First Aid Kits': 'Medical Supplies',
    'Neurological Medications': 'Medications',
    'Sterilization Equipment': 'Medical Devices',
    'Diagnostic Ultrasound Gel': 'Medical Supplies',
    'Artificial Hearts': 'Medical Devices',
    'Wound Closure Strips': 'Medical Supplies',
    'Radiology Contrast Media': 'Medical Supplies',
    'Surgical Scissors': 'Medical Supplies',
    'Prosthetic Joints': 'Medical Devices',
    'Orthopedic Casts': 'Medical Supplies',
    'Dental Floss': 'Medical Supplies',
    'Nasal Cannulas': 'Medical Supplies',
    'Orthopedic Tapes': 'Medical Supplies',
    'Medical Carts': 'Medical Devices',
    'Orthopedic Bandages': 'Medical Supplies',
    'Hydrocolloid Dressings': 'Medical Supplies',
    'Medical Scales': 'Medical Devices',
    'Mobility Scooters': 'Medical Devices',
    'Phlebotomy Needles': 'Medical Supplies',
    'Orthopedic Pillows': 'Medical Supplies',
    'Respiratory Therapy Equipment': 'Medical Devices',
    'Diagnostic Imaging Film': 'Medical Supplies',
    'Pulmonary Function Testers': 'Medical Devices',
    'Intravenous Poles': 'Medical Supplies',
    'Oxygen Masks': 'Medical Supplies',
    'Medical Charts and Records': 'Medical Supplies'
}

productId = 0

for product_name, product_category in product_mapping.items():
    #product_code = fake.uuid4()
    product_code = productId
    productId+=1
    product_description = f"{product_name} for medical use."
    unit_price = round(random.uniform(1, 100), 2)
    supplier = fake.company()
    product_df = pd.concat([product_df, pd.DataFrame({'ProductCode': [product_code],
                                    'ProductName': [product_name],
                                    'ProductCategory': [product_category],
                                    'ProductDescription': [product_description],
                                    'UnitPrice': [unit_price],
                                    'Supplier': [supplier]})], ignore_index=True)

print("done products")

start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 1, 1)
current_inventory = {}

while start_date < end_date:
    for product_code in product_df['ProductCode']:
        if product_code not in current_inventory:
            current_inventory[product_code] = 0
        if current_inventory[product_code] <= 0:
            current_inventory[product_code] = random.randint(1000, 10000)

    sales_date = start_date
    customer_name = fake.name()
    for _ in range(random.randint(50, 200)):
        product_code = random.choice(product_df['ProductCode'])
        sales_quantity = random.randint(1, 50)

        if current_inventory[product_code] >= sales_quantity:
            current_inventory[product_code] -= sales_quantity
        else:
            sales_quantity = current_inventory[product_code]
            current_inventory[product_code] = 0

        inventory_df = pd.concat([inventory_df, pd.DataFrame({'ProductCode': [product_code],
                                            'InventoryDate': [sales_date],
                                            'InventoryStart': [current_inventory[product_code] + sales_quantity],
                                            'InventoryEnd': [current_inventory[product_code]]})], ignore_index=True)
        sales_df = pd.concat([sales_df, pd.DataFrame({'SalesDate': [sales_date],
                                'CustomerName': [customer_name],
                                'ProductCode': [product_code],
                                'SalesQuantity': [sales_quantity]})], ignore_index=True)

    start_date += timedelta(days=1)

print("done for sales and inventory")

product_df.to_csv('product_data.csv', index=False)
sales_df.to_csv('sales_data.csv', index=False)
inventory_df.to_csv('inventory_data.csv', index=False)