import datetime
import json

from django.db import models

from utils.liu_student import exam_result


class Groupings(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kursnamn")
    courses = models.ManyToManyField("Course")

    def __str__(self):
        return self.name


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

                    exam_code=r['exam_code'].upper(),

                    name=r['exam_name'],
                    date=datetime.datetime.strptime(r['date'], "%Y-%m-%d")
                )
                if created:
                    for k, v in r["results"].items():
                        ExamResult.objects.get_or_create(exam=exam, name=k.upper(), amount=v)

    def collect_and_store_results(self):
        self.store_results(self.collect_results())


    def google_chart(self, exam, date_from, date_to, min_participants=0):
        grade_set = []
        kw = {}
        if exam:
            kw["exam_code__contains"] = exam.upper()

        if date_from and date_to:
            kw["date__gte"] = date_from
            kw["date__lte"] = date_to
        exam_set = list(self.exam_set.filter(**kw))
        if not exam_set:
            return "[]"
        for e in exam_set:
            grade_set += e.grades()
        grade_set = sorted(list(set(grade_set)), key=lambda x: (x[0].isdigit(), x))

        fgh = []
        total = {'summed': 0}
        for cp in grade_set:
            total[cp] = 0
        res = []

        for e in exam_set:
            tmp = [e.exam_code + " " + datetime.datetime.strftime(e.date, "%Y-%m-%d")]
            summed = 0
            exam_results = {}
            for l in grade_set:
                try:
                    exam_results[l] = e.examresult_set.get(name=l).amount
                except ExamResult.DoesNotExist:
                    exam_results[l] = 0

                summed += int(exam_results[l])
            if summed >= min_participants:
                for j in grade_set:
                    total[j] += exam_results[j]
                    tmp.append(exam_results[j])
                    tmp.append("<div style='margin: 5px; color: black;'><p>Betyg:&nbsp;{0}</p><p>Antal:&nbsp;{1}</p><p>Procent:&nbsp;{2:.1f}%</p></div>".format(str(j), str(exam_results[j]), (exam_results[j]*100/summed)))
                total['summed'] += summed
                res.append(tmp)
        for cp in grade_set:
            fgh.append("{0}, {1:.1f}%".format(str(cp), (total[cp]*100/total["summed"])))
            fgh.append({'type': 'string', 'role': 'tooltip', 'p': {'html': True}})
        label = ["Betyg", ] + fgh
        result = [label, ] + res
        return {"json": json.dumps(result), "total": total}


    def __str__(self):
        return self.course_code


    def statistics(self, date_from, date_to, min_participants=0):
        grade_set = []
        exam_code_set = []
        kw = {}
        if date_from and date_to:
            kw["date__gte"] = date_from
            kw["date__lte"] = date_to
        exam_set = list(self.exam_set.filter(**kw))
        if not exam_set:
            return {}
        for e in exam_set:
            exam_code_set.append(e.exam_code)
            grade_set += e.grades()
        grade_set = sorted(list(set(grade_set)), key=lambda x: (x[0].isdigit(), x))
        exam_code_set = sorted(list(set(exam_code_set)))

        total = {}
        for e in exam_code_set:
            total[e] = {'summed': 0}
            for cp in grade_set:
                total[e][cp] = 0

        for e in exam_set:
            summed = 0
            exam_results = {}
            for l in grade_set:
                try:
                    exam_results[l] = e.examresult_set.get(name=l).amount
                except ExamResult.DoesNotExist:
                    exam_results[l] = 0

                summed += int(exam_results[l])
            if summed >= min_participants:
                for j in grade_set:
                    total[e.exam_code][j] += exam_results[j]

                total[e.exam_code]['summed'] += summed
        return total


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
