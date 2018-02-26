from .models import Result


def saveresult(data,user_id)
    data = eval(data)
    for key, value in data.items():
        user_id = user_id
        question_id = key
        option = value
        result = Result(user_id = user_id,question_id = question_id,option = option)
        result.save()

    inducation_list = Inducation.objects.filter(test_id = 1)
    inducation_list = [o.get_json() for o in inducation_list]
    for i in inducation_list:
        inducation_id = i['id']
        sum = 0
        count = 0
        question_list = Question.objects.filter(inducation_id = inducation_id)
        question_list = [o.get_json() for o in question_list]
        for j in question_list:
            question_id = i['id']
            try:
                result = Result.objects.get(question_id = question_id,user_id = user_id)
                value = result.option
                count = count + 1
                sum = sum + value
                avg = round(sum/count, 2)
