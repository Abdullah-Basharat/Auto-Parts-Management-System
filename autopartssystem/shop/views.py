from django.shortcuts import render
from . import models
from django.utils.html import escape
from datetime import datetime
from django.contrib.auth import authenticate, login
# Create your views here.

def escaped_name(x):
    new = []
    for i in x:
        i.name = escape(i.name)
        new.append(i)
    return new
def dropdown():
    brand_obj = models.Brand.objects.all()
    car_obj = models.Car.objects.all()
    type_obj = models.Type.objects.all()
    parts_obj = models.Part.objects.all()
    new_brand = escaped_name(brand_obj)
    new_car = escaped_name(car_obj)
    new_type = escaped_name(type_obj)
    new_items = escaped_name(parts_obj)
    my_dict1= {"Brands":new_brand,"Cars":new_car,"Type":new_type,"Items":new_items}
    return my_dict1

def get_total_objects(x):
    total_objects = []
    a = 0
    for i in x:
        a += 1
        my_dict = {
            "no": a,
            "brand": i['car_type__car__brand__name'],
            "car": i['car_type__car__name'],
            "type": i['car_type__type__name'],
            "item": i['part__name'],
            "quantity": i["quantity"],
            "price": i["price"]
        }
        total_objects.append(my_dict)
    return total_objects

def login_page(request):
    if request.method == 'POST':
        content = dropdown()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html',content)  # replace 'home' with your desired homepage URL
        else:
            error_message = ['Invalid username or password']
    else:
        error_message = ''
    return render(request, 'login.html', {'message': error_message})

def insertdata(request):
    content = dropdown()
    if request.method == "POST":
        msg = []
        my_brand = request.POST.get("brand")
        my_car = request.POST.get("car")
        my_car_type = request.POST.get("type")
        my_part = request.POST.get("item")
        my_quantity = request.POST.get("quantity")
        my_price = request.POST.get("price")
        my_brand = my_brand.strip().capitalize()
        my_car = my_car.strip().capitalize()
        my_car_type = my_car_type.strip().upper()
        my_part = my_part.strip().capitalize()
        my_brand_obj = models.Brand.objects.filter(name=my_brand)
        if len(my_brand_obj) == 0:
            x = models.Brand(name=my_brand)
            x.save()
            my_brand_obj = models.Brand.objects.filter(name=my_brand)
        my_car_obj = models.Car.objects.filter(name=my_car, brand=my_brand_obj[0])
        if len(my_car_obj) == 0:
            x = models.Car(name=my_car, brand=my_brand_obj[0])
            x.save()
            my_car_obj = models.Car.objects.filter(name=my_car, brand=my_brand_obj[0])
        my_type_obj = models.Type.objects.filter(name=my_car_type)
        if len(my_type_obj) == 0:
            x = models.Type(name=my_car_type)
            x.save()
            my_type_obj = models.Type.objects.filter(name=my_car_type)
        my_car_type_obj = models.Car_Type.objects.filter(car=my_car_obj[0],type=my_type_obj[0])
        if len(my_car_type_obj) == 0:
            x = models.Car_Type(car=my_car_obj[0],type=my_type_obj[0])
            x.save()
            my_car_type_obj = models.Car_Type.objects.filter(car=my_car_obj[0], type=my_type_obj[0])
        my_part_obj = models.Part.objects.filter(name=my_part)
        if len(my_part_obj) == 0:
            x = models.Part(name = my_part)
            x.save()
            my_part_obj = models.Part.objects.filter(name=my_part)
        my_car_part_obj = models.Car_Parts.objects.filter(car_type=my_car_type_obj[0],part=my_part_obj[0])
        if len(my_car_part_obj) == 0:
            x = models.Car_Parts(car_type=my_car_type_obj[0],part=my_part_obj[0],quantity=my_quantity,price=my_price)
            x.save()
            msg.append("Record has been added successfully")
        else:
            pre_price = my_car_part_obj[0].price
            if pre_price > int(my_price):
                my_price = pre_price
            my_quantity = int(my_quantity) + my_car_part_obj[0].quantity
            models.Car_Parts.objects.filter(car_type=my_car_type_obj[0], part=my_part_obj[0]).update(quantity=my_quantity,price=my_price)
            msg.append("Record has been updated successfully")
        content = dropdown()
        content["brand"] = my_brand
        content["car"] = my_car
        content["type"] = my_car_type
        content["message"] = msg
    return render(request,"insertdata.html",content)

def retrievedata(request):
    content = dropdown()
    if request.method == "POST":
        my_brand = request.POST.get("brand")
        my_car = request.POST.get("car")
        my_car_type = request.POST.get("type")
        if my_brand != "":
            my_brand = my_brand.strip().capitalize()
            content["brand"] = my_brand
            if my_car != "":
                my_car = my_car.strip().capitalize()
                content["car"] = my_car
                if my_car_type != "":
                    my_car_type = my_car_type.strip().upper()
                    content["brand"] = ''
                    content["car"] = ''
                    content["type"] = ''
                    x = models.Car_Parts.objects.filter(car_type__car__brand__name=my_brand,car_type__car__name=my_car,car_type__type__name=my_car_type).values('car_type__car__brand__name',
                                                                                         'car_type__car__name',
                                                                                         'car_type__type__name',
                                                                                         'part__name', 'quantity',
                                                                                         'price').order_by(
                        'car_type__car__brand__name', 'car_type__car__name')

                else:
                    x = models.Car_Parts.objects.filter(car_type__car__brand__name=my_brand, car_type__car__name=my_car,
                                                        ).values(
                        'car_type__car__brand__name',
                        'car_type__car__name',
                        'car_type__type__name',
                        'part__name', 'quantity',
                        'price').order_by(
                        'car_type__car__brand__name', 'car_type__car__name')
            else:
                x = models.Car_Parts.objects.filter(car_type__car__brand__name=my_brand).values(
                    'car_type__car__brand__name',
                    'car_type__car__name',
                    'car_type__type__name',
                    'part__name', 'quantity',
                    'price').order_by(
                    'car_type__car__brand__name', 'car_type__car__name')
        else:
            x = models.Car_Parts.objects.select_related('part', 'car_type__car__brand', 'car_type__type').values(
                'car_type__car__brand__name',
                'car_type__car__name',
                'car_type__type__name',
                'part__name', 'quantity',
                'price').order_by(
                'car_type__car__brand__name', 'car_type__car__name')
    else:
        x = models.Car_Parts.objects.select_related('part', 'car_type__car__brand','car_type__type').values('car_type__car__brand__name',
                                                                                           'car_type__car__name',
                                                                                           'car_type__type__name',
                                                                                           'part__name', 'quantity',
                                                                                           'price').order_by(
            'car_type__car__brand__name', 'car_type__car__name')
    total_objects = get_total_objects(x)

    content["table_data"] = total_objects

    return render(request,"availabedata.html",content)
def calculate_bill(brand,car,car_type,parts,quantity,prices):
    msg = []
    total_amount = 0
    total_bill = []
    for i in range(len(parts)):
        if quantity[i] == "" or prices[i] == "" or parts[i] =="":
            continue
        y = parts[i]
        y = y.strip().capitalize()
        x = models.Car_Parts.objects.filter(car_type__car__brand__name=brand,car_type__car__name=car,car_type__type__name=car_type,part__name=y)
        if len(x) == 0:
            z = f"You have no "+str(y)
            msg.append(z)
        else:

            if x[0].quantity <= int(quantity[i]) :
                x = models.Car_Parts.objects.filter(car_type__car__brand__name=brand, car_type__car__name=car,
                                                    car_type__type__name=car_type, part__name=y)
                z = f"You have only" + str(x[0].quantity) + " " + y
                msg.append(z)
                x.delete()

            else:
                my_quantity = x[0].quantity-int(quantity[i])
                models.Car_Parts.objects.filter(car_type__car__brand__name=brand, car_type__car__name=car,
                                                car_type__type__name=car_type, part__name=y).update(
                    quantity=my_quantity)

        my_dict = {
                "no":i+1,
                "item":y,
                "quantity":quantity[i],
                "price":prices[i],
                "Total":int(quantity[i]) * int(prices[i])
                }
        total_bill.append(my_dict)
        total_amount += int(quantity[i]) * int(prices[i])
    return  total_bill,total_amount,msg
def index(request):
    content = dropdown()
    return render(request,"index.html",content)

def bill(request):
    content = dropdown()
    if request.method == "POST":
        d = datetime.now()
        my_brand = request.POST.get("brand")
        my_car = request.POST.get("car")
        my_car_type = request.POST.get("type")
        my_part = request.POST.getlist("item")
        my_part.pop()
        my_quantity = request.POST.getlist("quantity")
        my_quantity.pop()
        my_price = request.POST.getlist("price")
        my_price.pop()
        my_brand = my_brand.strip().capitalize()
        my_car = my_car.strip().capitalize()
        my_car_type = my_car_type.strip().upper()
        total_bill, total_amount, msg = calculate_bill(my_brand, my_car, my_car_type, my_part, my_quantity,
                                                                   my_price)
        x = models.History.objects.filter(date=d.date())
        if len(x) == 0:
            x = models.History(date=d.date(),earn=total_amount)
            x.save()
        else:
            total = total_amount+ x[0].earn
            models.History.objects.filter(date=d.date()).update(earn=total)
        content["message"] = msg
        content["brand"] = my_brand
        content["car"] = my_car
        content["type"] = my_car_type
        content["table_data"] = total_bill
        content["total"] = total_amount
        content["date"] = d.date()
        content["time"] = d.time()


        return render(request, "bill.html", content)

    return render(request,"index.html",content)

