import datetime
import json

from django.db import models

from utils.liu_student import exam_result


class Course(models.Model):
    course_code = models.CharField(max_length=10, verbose_name="Kurskod", unique=True)
    name = models.CharField(max_length=255, verbose_name="Kursnamn")

    def collect_results(self):
        res = exam_result(self.course_code)
        return res

    def store_results(self, res):
        for r in res:
            if r['course_code'] == self.course_code:
                exam, created = Exam.objects.get_or_create(
                    course=self,
                    exam_code=r['exam_code'],
                    name=r['exam_name'],
                    date=datetime.datetime.strptime(r['date'], "%Y-%m-%d")
                )
                if created:
                    for k, v in r["results"].items():
                        ExamResult.objects.get_or_create(exam=exam, name=k.upper(), amount=v)

    def collect_and_store_results(self):
        self.store_results(self.collect_results())

    def google_chart(self, exam, date_from, date_to):
        grade_set = []
        kw = {}
        if exam:
            kw["exam_code__contains"] = exam
        if date_from and date_to:
            kw["date__gte"] = date_from
            kw["date__lte"] = date_to
        exam_set = list(self.exam_set.filter(**kw))
        if not exam_set:
            return "[]"
        for e in exam_set:
            grade_set += e.grades()
        grade_set = sorted(list(set(grade_set)), key=lambda x: (x[0].isdigit(), x))
        label = ["Betyg", ] + grade_set
        res = []
        for e in exam_set:
            tmp = [e.exam_code + " " + datetime.datetime.strftime(e.date, "%Y-%m-%d")]
            for l in label[1:]:
                try:
                    tmp.append(e.examresult_set.get(name=l).amount)
                except ExamResult.DoesNotExist:
                    tmp.append(0)
            res.append(tmp)
        result = [label, ] + res
        return json.dumps(result)

    def __str__(self):
        return self.course_code


class Exam(models.Model):
    course = models.ForeignKey(Course)
    exam_code = models.CharField(max_length=10, verbose_name="Tentamenskod")
    name = models.CharField(max_length=255, verbose_name="Tentanamn")
    date = models.DateField()

    def grades(self):
        return self.examresult_set.all().values_list("name", flat=True)


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam)
    name = models.CharField(max_length=10)
    amount = models.IntegerField()
