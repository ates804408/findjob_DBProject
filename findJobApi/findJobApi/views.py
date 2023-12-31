from django.utils import timezone
from datetime import *
import uuid
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import User, UserPost
from .serializers import UserSerializer
from django.db import connection
from rest_framework import status
from .utils import sendMail
from django.db import connection, transaction


@api_view(["GET"])
def get_company_job_applications(request, companyId):
    raw_get_query = 'SELECT * FROM "findJobApi_jobapplication" where company_id = %s'

    count = 0
    job_applications = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query, params=[companyId])
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "job_application_id": p[0],
            "application_date": p[1],
            "company_id": p[2],
            "job_id": p[3],
            "user_id": p[4],
        }
        job_applications.append(company_post)
        count += 1

    return JsonResponse(
        {"result": job_applications, "count": count}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_user_job_applications(request, userId):
    raw_get_query = 'SELECT * FROM "findJobApi_jobapplication" where user_id = %s'

    count = 0
    job_applications = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query, params=[userId])
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "job_application_id": p[0],
            "application_date": p[1],
            "company_id": p[2],
            "job_id": p[3],
            "user_id": p[4],
        }
        job_applications.append(company_post)
        count += 1

    return JsonResponse(
        {"result": job_applications, "count": count}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_all_job_applications(request):
    raw_get_query = 'SELECT * FROM "findJobApi_jobapplication" '

    count = 0
    job_applications = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "job_application_id": p[0],
            "application_date": p[1],
            "company_id": p[2],
            "job_id": p[3],
            "user_id": p[4],
        }
        job_applications.append(company_post)
        count += 1

    return JsonResponse(
        {"result": job_applications, "count": count}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def create_job_application(request):
    raw_insert_query = 'insert into "findJobApi_jobapplication" (job_application_id,application_date,company_id,job_id,user_id) values (%s,%s,%s,%s,%s)'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    uniqueID = (str(uuid.uuid4()),)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                raw_insert_query,
                params=[
                    uniqueID,
                    f"{current_time}",
                    request.data.get("company_id"),
                    request.data.get("job_id"),
                    request.data.get("user_id"),
                ],
            )

            cursor.close()

    except Exception as e:
        return JsonResponse(
            {"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        {
            "result": {
                "job_application_id": f"{uniqueID}",
                **request.data,  # Merge request.data into the result dictionary
            }
        },
        safe=False,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_company_jobs(request, companyId):
    raw_get_query = 'SELECT * FROM "findJobApi_job" where company_id = %s '

    count = 0
    jobs = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query, params=[companyId])
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "title": p[0],
            "description": p[1],
            "application_count": p[2],
            "salary": p[3],
            "created_data": p[4],
            "job_id": p[5],
            "company_id": p[6],
        }
        jobs.append(company_post)
        count += 1

    return JsonResponse({"result": jobs, "count": count}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all_jobs(request):
    raw_get_query = 'SELECT * FROM "findJobApi_job"'

    count = 0
    jobs = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "title": p[0],
            "description": p[1],
            "application_count": p[2],
            "salary": p[3],
            "created_data": p[4],
            "job_id": p[5],
            "company_id": p[6],
        }
        jobs.append(company_post)
        count += 1

    return JsonResponse({"result": jobs, "count": count}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_job(request):
    raw_insert_query = 'insert into "findJobApi_job" (title,description,application_count,salary,created_date,job_id,company_id) values (%s,%s,%s,%s,%s,%s,%s)'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                raw_insert_query,
                params=[
                    request.data.get("title"),
                    request.data.get("description"),
                    request.data.get("application_count"),
                    request.data.get("salary"),
                    f"{current_time}",
                    str(uuid.uuid4()),
                    request.data.get("company_id"),
                ],
            )

    except Exception as e:
        return JsonResponse(
            {"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        {"result": request.data}, safe=False, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_all_companies_posts(request):
    raw_get_query = 'SELECT * FROM "findJobApi_companypost"'

    count = 0
    posts = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "title": p[0],
            "description": p[1],
            "company_post_id": p[2],
            "company_post_date": p[3],
            "company": p[4],
        }
        posts.append(company_post)
        count += 1

    return JsonResponse({"result": posts, "count": count}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_company_posts(request, companyId):
    raw_get_query = 'SELECT * FROM "findJobApi_companypost" where company_id = %s'

    count = 0
    posts = []

    if companyId is not None:
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_get_query, params=[companyId])
                result = cursor.fetchall()

        except Exception as e:
            return JsonResponse(
                {"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for p in result:
            company_post = {
                "title": p[0],
                "description": p[1],
                "company_post_id": p[2],
                "company_post_date": p[3],
                "company": p[4],
            }
            posts.append(company_post)
            count += 1

        return JsonResponse(
            {"result": posts, "count": count}, status=status.HTTP_200_OK
        )

    return JsonResponse(
        {"result": "You have to provide a mail address"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def create_company_post(request):
    raw_insert_query = 'insert into "findJobApi_companypost" (title,description,company_post_id,company_post_date,company_id) values (%s,%s,%s,%s,%s)'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                raw_insert_query,
                params=[
                    request.data.get("title"),
                    request.data.get("description"),
                    str(uuid.uuid4()),
                    f"{current_time}",
                    request.data.get("company_id"),
                ],
            )

    except Exception as e:
        print(e)
        return JsonResponse(
            {"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        {"result": request.data}, safe=False, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_all_users(request):
    raw_get_query = 'SELECT * FROM "findJobApi_user"'

    count = 0
    companies = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "name": p[0],
            "surname": p[1],
            "mail": p[2],
            "person_id": p[3],
            "created_date": p[4],
            "is_active": p[5],
            "gender": p[6],
        }
        companies.append(company_post)
        count += 1

    return JsonResponse(
        {"result": companies, "count": count}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_all_companies(request):
    raw_get_query = 'SELECT * FROM "findJobApi_company"'

    count = 0
    companies = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for p in result:
        company_post = {
            "name": p[0],
            "company_id": p[1],
            "created_date": p[2],
        }
        companies.append(company_post)
        count += 1

    return JsonResponse(
        {"result": companies, "count": count}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def create_company(request):
    raw_insert_query = 'insert into "findJobApi_company" (name,company_id,created_date) values (%s,%s,%s)'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                raw_insert_query,
                params=[
                    request.data.get("name"),
                    str(uuid.uuid4()),
                    f"{current_time}",
                ],
            )

    except Exception as e:
        return JsonResponse(
            {"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        {"result": request.data}, safe=False, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_all_user_posts(request):
    raw_get_query = 'SELECT * FROM "findJobApi_userpost"'

    count = 0
    posts = []

    try:
        with connection.cursor() as cursor:
            cursor.execute(raw_get_query)
            result = cursor.fetchall()

        for p in result:
            user_post = {
                "title": p[0],
                "description": p[1],
                "user_post_id": p[2],
                "user_post_date": p[3],
                "user": p[4],
            }
            posts.append(user_post)
            count += 1

    except Exception as e:
        return JsonResponse({"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({"result": posts, "count": count}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_posts(request, userId):
    raw_get_query = 'SELECT * FROM "findJobApi_userpost" where user_id = %s'

    count = 0
    posts = []

    if userId is not None:
        try:
            with connection.cursor() as cursor:
                cursor.execute(raw_get_query, params=[userId])
                result = cursor.fetchall()

        except Exception as e:
            return JsonResponse(
                {"result": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        for p in result:
            user_post = {
                "title": p[0],
                "description": p[1],
                "user_post_id": p[2],
                "user_post_date": p[3],
                "user": p[4],
            }
            posts.append(user_post)
            count += 1

        return JsonResponse(
            {"result": posts, "count": count}, status=status.HTTP_200_OK
        )

    return JsonResponse(
        {"result": "You have to provide a mail address"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def create_user_post(request):
    #'2023-09-24T23:24:00.000Z
    raw_insert_query = 'insert into "findJobApi_userpost" (title,description,user_post_id,user_id,user_post_date) values (%s,%s,%s,%s,%s)'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                raw_insert_query,
                params=[
                    request.data.get("title"),
                    request.data.get("description"),
                    str(uuid.uuid4()),
                    request.data.get("user_id"),
                    current_time,
                ],
            )

            return JsonResponse(
                {"result": request.data}, safe=False, status=status.HTTP_201_CREATED
            )

    except Exception as e:
        return JsonResponse(
            {"result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def create_user(request):
    mail = request.data.get("mail")
    raw_query = 'select * from "findJobApi_user" where mail= %s '

    user = User()

    if mail is not None:
        result = User.objects.raw(raw_query=raw_query, params=[mail])

        for p in result:
            user.name = p.name
            user.surname = p.surname
            user.is_active = p.is_active
            user.mail = p.mail
            user.gender = p.gender
            user.person_id = p.person_id
            user.created_date = p.created_date

        if len(result) == 0:
            print("verilen mail addresinde kullanici mevcut degil")
            raw_insert_query = 'INSERT INTO "findJobApi_user" (name, surname, mail, "person_id",created_date, is_active,gender) VALUES (%s, %s, %s, %s, %s, %s,%s)'
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            with connection.cursor() as cursor:
                cursor.execute(
                    raw_insert_query,
                    params=[
                        request.data.get("name"),
                        request.data.get("surname"),
                        request.data.get("mail"),
                        uuid.uuid4(),
                        f"'{current_time}'",
                        "False",  # assuming is_active is a boolean field
                        request.data.get("gender"),
                    ],
                )

            # Commit the changes to the database
            transaction.commit()
            sendMail([request.data["mail"]])
            ## kullanici yeni kaydoluyor suanda kendisini kaydedip aktivasyon maili yollamamiz gerekli
            return JsonResponse(
                {"result": request.data},
                safe=False,
                status=status.HTTP_201_CREATED,
            )

        elif user.is_active == False:
            print("kullanici vardi ve aktif degildi dolayisiyla mail yollandi")
            ## ilgili kullanici veri tabaninda varmis ama aktif degilmis kendisine dogrulama maili yollayalim
            sendMail([user.mail])
            return JsonResponse(
                {"result": UserSerializer(user).data},
                safe=False,
                status=status.HTTP_200_OK,
            )

        elif user.is_active == True and len(result) > 0:
            print(
                "bu kullanici zaten vardi ve veri tabaninda aktif olarak kayitli gozukuyor"
            )
            ## var ve aktif olan bir kullanici icin kayit olunmaya calisildi hata mesaji vererek islemi sonlandiralim
            return JsonResponse(
                {"result": "Bu kullanici zaten mevcut"}, status=status.HTTP_409_CONFLICT
            )

    else:
        print("kullanici mail girmemis")
        return JsonResponse(
            {"result": "Mail adresi gonderilmedi"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def login_user(request):
    mail = request.data.get("mail")
    raw_query = 'select * from "findJobApi_user" where mail= %s'

    user = User()

    if mail is not None:
        result = User.objects.raw(raw_query=raw_query, params=[mail])

        for p in result:
            user.name = p.name
            user.surname = p.surname
            user.is_active = p.is_active
            user.mail = p.mail
            user.gender = p.gender
            user.person_id = p.person_id

        if len(result) == 0:
            ## boyle bir kullanici yokmus dolayisiyla hata atalim
            return JsonResponse(
                {"result": "Mail adresi veri tabanina kayitli degil"},
                safe=False,
                status=status.HTTP_404_NOT_FOUND,
            )

        elif user.is_active == False:
            print("kullanici vardi ve aktif degildi dolayisiyla mail yollandi LOGIN")
            ## ilgili kullanici veri tabaninda varmis ama aktif degilmis kendisine dogrulama maili yollayalim
            sendMail([user.mail])
            return JsonResponse(
                {"result": UserSerializer(user).data},
                safe=False,
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(
            {"result": UserSerializer(user).data}, safe=False, status=status.HTTP_200_OK
        )

    else:
        print("kullanici mail girmemis")
        return JsonResponse(
            {"result": "Mail adresi gonderilmedi"},
            safe=False,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def activate_user_account(request, mail):
    raw_query = 'select * from "findJobApi_user" where mail= %s'

    if mail is not None:
        result = User.objects.raw(raw_query=raw_query, params=[mail])

        if len(result) == 0:
            return JsonResponse(
                {"response": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )

        with connection.cursor() as cursor:
            cursor.execute(
                'update "findJobApi_user" set is_active = True where mail = %s',
                params=[mail],
            )

        return JsonResponse({"response": "Account verified"}, status=status.HTTP_200_OK)

    return JsonResponse(
        {"BAD_REQUEST": "given mail does not exist in database"},
        status=status.HTTP_404_NOT_FOUND,
    )
