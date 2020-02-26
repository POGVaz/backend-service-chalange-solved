from django.shortcuts import render
from django.http import HttpResponse

import json

from .models import User,Address,Answer
from .tasks import fetch_location

def add_user_address(request):

    # TODO: Check if request has all the fields.
    # IDEA: Separate each duty of this method in different functions.

    # Assuming the POST request carries a JSON object.
    request_body = json.loads(request.body)

    # Create user, address, and answers and save them to the database:
    created_user = User(
        name_text=request_body["user_info"]["name"],
        email_text=request_body["user_info"]["email"],
        phone_text=request_body["user_info"]["phone"],
    )
    created_user.save()

    created_address = created_user.address_set.create(
        city_text=request_body["address_attributes"]["city"],
        neighborhood_text=request_body["address_attributes"]["neighborhood"],
        street_text=request_body["address_attributes"]["street"],
        uf_code=request_body["address_attributes"]["uf"],
        zip_code=request_body["address_attributes"]["zip_code"],
    )
    created_address.save()

    # request_info can have an arbitrary number of questions:
    for question in request_body["request_info"]:
        created_answer = created_user.answer_set.create(
            question_text=question,
            answer_text=request_body["request_info"][question]
        )
        created_answer.save()

    # Send task to fetch location:
    fetch_location.delay(address_id=created_address.id, street=request_body["address_attributes"]["street"],
                        city=request_body["address_attributes"]["city"], state=request_body["address_attributes"]["uf"])

    # Respond the request:
    return HttpResponse("User information added.")
