from django.shortcuts import render
from django.http import HttpResponse

from .models import User,Address,Answer
from .tasks import fetchLocation

def add_user_address(request):

    # TODO: Check if request has all the fields.

    # Create user, address, and answers and save them to the database:
    created_user = User(
        name_text=request["user_info"]["name"],
        email_text=request["user_info"]["email"],
        phone_text=request["user_info"]["phone"]
    )
    created_user.save()

    created_address = created_user.address_set.create(
        city_text=request["address_attributes"]["city"],
        neighborhood_text=request["address_attributes"]["neighborhood"],
        street_text=request["address_attributes"]["street"],
        uf_code=request["address_attributes"]["uf"],
        zip_code=request["address_attributes"]["zip_code"]
    )
    created_address.save()

    for question in request["request_info"]:
        created_answer = created_user.answer_set.create(
            question_text=question,
            answer_text=request["request_info"][question]
        )
        created_answer.save()


    # Send task to fetch location:
    fetchLocation.delay(address_id=created_address.id, street=request["address_attributes"]["street"],
                        city=request["address_attributes"]["city"], state=request["address_attributes"]["uf"])

    # Respond the request:
    return HttpResponse("User information added.")
