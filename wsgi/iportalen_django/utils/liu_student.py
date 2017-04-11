import requests


class MultipleMatches(Exception):
    pass


def exam_result(course_code):
    url = "http://student.liu.se/tentaresult/?kurskod={}&provkod=&datum=&kursnamn=&sort=0&search=S%F6k".format(course_code)

    payload = ""
    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    response.encoding = "iso-8859-1"
    data = response.text.lower()
    lines = data.split("\n")

    l_nr = 0
    for l in lines:
        l_nr += 1
        if "beskrivning av tentamenstillfället" in l:
            break

    lines = lines[l_nr:]
    l_nr = 0
    for l in lines:
        if "<form" in l:
            break
        l_nr += 1
    lines = lines[:l_nr]
    lines.insert(0, "</tr>")
    lines.append("</table></td>")
    text = "".join(lines).replace("<br>", "<br />").replace('bgcolor="#ffffff"', 'bgcolor=""').replace('bgcolor="#ffffcc"', 'bgcolor=""')
    tables = text.split('</tr><tr valign="top" bgcolor="">')[1:]
    results = []
    for exam in tables:
        parts = exam.split("</td><td>", 1)
        info = parts[0][4:].split("<br />")
        if info[0].split(":")[0].upper() != course_code.upper():
            raise MultipleMatches
        result = {
            "course_code": info[0].split(":")[0].upper(),
            "course_name": info[0].split(":")[1].replace("  ", " ").replace("  ", " "),
            "exam_code":  info[1].split(":")[0].upper(),
            "exam_name": info[1].split(":")[1].replace("  ", " ").replace("  ", " "),
            "date": info[2].strip()
        }
        res = parts[1].replace('<table border="1" cellspacing="0" cellpadding="2"><tr><td><i>betyg</i></td><td><i>antal</i></td></tr><tr>', "").replace("</tr>", "").replace("</table>", "").split("<tr>")
        exam_results = {}
        for r in res:

            s = r.replace(" ", "").split("</td><td>")
            exam_results[s[0].replace("<td>", "").strip()] = s[1].replace("</td>", "")
        result["results"] = exam_results
        results.append(result)
    return results


if __name__ == "__main__":
    res = exam_result("TATM79")
    print(res)
