from .models import Result,Question


def get_inducation_avg(user_id,inducation_id):
    sum = 0
    count = 0
    question_list = Question.objects.filter(inducation_id = inducation_id)
    question_list = [o.get_json() for o in question_list]
    for j in question_list:
        question_id = j['id']
        try:
            result = Result.objects.get(question_id = question_id,user_id = user_id)
            value = result.score
            count = count + 1
            sum = sum + value
        except Result.DoesNotExist:
            pass
    avg = round(sum/count, 2)

    return avg

