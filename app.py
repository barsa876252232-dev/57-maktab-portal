
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "boysun57_test_portal_2026"

SINF_NOMLARI = [
    "5-A", "5-B",
    "6-A", "6-B",
    "7-A",
    "8-A", "8-B",
    "9-A", "9-B",
    "10-A", "11-A"
]


def savol_yarat(matn, javob, tartib):
    variantlar = [
        javob - 2,
        javob - 1,
        javob + 1
    ]

    togri_joy = tartib % 4
    natija = []
    xato_index = 0

    for i in range(4):
        if i == togri_joy:
            natija.append(str(javob))
        else:
            natija.append(str(variantlar[xato_index]))
            xato_index += 1

    return {
        "savol": matn,
        "variantlar": natija,
        "javob": togri_joy
    }


def matematika_testi(sinf):
    savollar = []
    sinf = int(sinf)

    for i in range(20):
        n = i + 1

        if sinf == 5:
            tur = i % 5

            if tur == 0:
                a, b = 24 + n, 13 + n
                matn = f"Hisoblang: {a} + {b}"
                javob = a + b

            elif tur == 1:
                a, b = 70 + n, 15 + n
                matn = f"Hisoblang: {a} - {b}"
                javob = a - b

            elif tur == 2:
                a, b = 3 + n % 7, 4 + n % 5
                matn = f"Hisoblang: {a} × {b}"
                javob = a * b

            elif tur == 3:
                b = 3 + n % 7
                a = b * (2 + n % 5)
                matn = f"Hisoblang: {a} : {b}"
                javob = a // b

            else:
                a, b = 5 + n, 3 + n % 4
                matn = f"Tomonlari {a} sm va {b} sm bo‘lgan to‘g‘ri to‘rtburchak perimetrini toping."
                javob = 2 * (a + b)

        elif sinf == 6:
            tur = i % 5

            if tur == 0:
                a, b = 100 + 10*n, 10 + 10*(n % 5)
                matn = f"{a} sonining {b}% ini toping."
                javob = a * b // 100

            elif tur == 1:
                a, b = 35 + n, 17 + n
                matn = f"Hisoblang: {a} + {b}"
                javob = a + b

            elif tur == 2:
                a, b = 50 + n, 12 + n
                matn = f"Hisoblang: {a} - {b}"
                javob = a - b

            elif tur == 3:
                a, b = 4 + n % 6, 5 + n % 4
                matn = f"Hisoblang: {a} × {b}"
                javob = a * b

            else:
                a, b = 20 + n, 4
                matn = f"Hisoblang: {a} × {b}"
                javob = a * b

        elif sinf == 7:
            x = 2 + n
            a = 2 + n % 5
            b = 3 + n
            c = a * x + b
            matn = f"Tenglamani yeching: {a}x + {b} = {c}"
            javob = x

        elif sinf == 8:
            tur = i % 4

            if tur == 0:
                a = n + 3
                matn = f"Hisoblang: {a}²"
                javob = a ** 2

            elif tur == 1:
                a = n + 4
                matn = f"Hisoblang: √{a*a}"
                javob = a

            elif tur == 2:
                x = n + 2
                a = 3
                b = 5 + n
                c = a*x + b
                matn = f"Tenglamani yeching: {a}x + {b} = {c}"
                javob = x

            else:
                a = n + 2
                b = n + 3
                matn = f"Hisoblang: ({a} + {b})²"
                javob = (a + b) ** 2

        elif sinf == 9:
            x1 = 1 + n % 5
            x2 = 2 + n % 7
            b = -(x1 + x2)
            c = x1 * x2
            d = b*b - 4*c
            matn = f"x² + ({b})x + {c} = 0 tenglamaning diskriminantini toping."
            javob = d

        elif sinf == 10:
            a = 2 + n % 6
            b = 3 + n
            x = n + 2
            matn = f"f(x) = {a}x + {b}. f({x}) ni toping."
            javob = a*x + b

        else:
            a = 2 + n % 5
            b = 3 + n
            x = n + 1
            matn = f"f(x) = {a}x² + {b}x. f'({x}) ni toping."
            javob = 2*a*x + b

        savollar.append(savol_yarat(matn, javob, i))

    return savollar


TESTLAR = {
    sinf: {
        "Matematika": matematika_testi(sinf.split("-")[0])
    }
    for sinf in SINF_NOMLARI
}


# ONLINE TEST — sinf tanlash
@app.route("/")
def bosh_sahifa():
    return render_template("index.html")


@app.route("/haqida")
def maktab_haqida():
    return render_template("haqida.html")


@app.route("/yangiliklar")
def yangiliklar():
    return render_template("yangiliklar.html")


@app.route("/boglanish")
def boglanish():
    return render_template("boglanish.html")
@app.route("/testlar")
def testlar():
    return render_template(
        "testlar.html",
        mode="sinflar",
        sinflar=SINF_NOMLARI
    )


# ONLINE TEST — fan tanlash
@app.route("/testlar/<sinf>")
def fan_tanlash(sinf):
    if sinf not in SINF_NOMLARI:
        return redirect(url_for("testlar"))

    fanlar = list(TESTLAR[sinf].keys())

    return render_template(
        "testlar.html",
        mode="fanlar",
        sinf=sinf,
        fanlar=fanlar
    )


# ONLINE TEST — savollar
@app.route("/test/<sinf>/<fan>", methods=["GET", "POST"])
def test_ishlash(sinf, fan):
    if sinf not in TESTLAR or fan not in TESTLAR[sinf]:
        return redirect(url_for("testlar"))

    savollar = TESTLAR[sinf][fan]

    if request.method == "POST":
        togri = 0
        javoblar = []

        for i, savol in enumerate(savollar):
            tanlov = request.form.get(f"savol_{i}")
            to_gri_javob = str(savol["javob"])

            if tanlov == to_gri_javob:
                togri += 1

            javoblar.append({
                "savol": savol["savol"],
                "togri": tanlov == to_gri_javob
            })

        jami = len(savollar)
        foiz = round(togri / jami * 100) if jami else 0

        return render_template(
            "testlar.html",
            mode="natija",
            sinf=sinf,
            fan=fan,
            togri=togri,
            jami=jami,
            foiz=foiz,
            javoblar=javoblar
        )

    return render_template(
        "testlar.html",
        mode="test",
        sinf=sinf,
        fan=fan,
        savollar=savollar
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

