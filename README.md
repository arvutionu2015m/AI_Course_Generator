**AI Course Generator** on täisfunktsionaalne Django-põhine veebirakendus, mis võimaldab kasutajatel kirjeldada kursuse teemat ja seejärel laseb OpenAI’l automaatselt genereerida:

* moodulid
* peatükid
* sisu
* viktoriiniküsimused
* praktilised ülesanded

Lisaks võimaldab admin-paneelis:

* kogu struktuuri uuesti genereerimist ühe nupuvajutusega
* quiz’ide ja ülesannete eraldi AI-genereerimist
* kursuse struktuuri AI-põhist hindamist ja valideerimist
* kursuste detailvaadet kasutajale

---

## ⚙️ Tehnilised omadused

### 💡 Arhitektuur:

* **Backend**: Django 5, Python 3.10+
* **Frontend**: Bootstrap 5 + custom templates
* **AI-integreerimine**: OpenAI GPT-4 kaudu
* **Andmebaas**: SQLite (dev), laiendatav Postgres/MariaDB-le
* **Autentimine**: Django `auth` (login, signup, logout)
* **Failistruktuur**:

  ```
  /config/         # Django seadistused
  /core/           # Kursuste äriloogika (models, views, admin)
  /templates/      # Bootstrap5 mallid (home, login, detail jne)
  /static/         # CSS ja JS
  /services.py     # OpenAI päringuloogika
  ```

---

## 🔍 Peamised funktsioonid

### 👨‍🏫 Kasutajavaade:

* Loo uus kursus teemal “X”
* Vaata AI poolt loodud kursuse struktuuri
* Vasta viktoriiniküsimustele (AI hindab ja annab tagasisidet)
* Näe AI soovitatud järgmise kursuse ideed
* Detailvaade: moodulid, peatükid, quiz’id, ülesanded, hinnang

### 🛠️ Admin-paneel:

* Moodulite ja peatükkide inline-haldusega admin
* Nupud:

  * 🔁 Regenereri kogu kursus AI-ga
  * 🤖 Genereeri quiz AI abil
  * 🧠 Genereeri ülesanne AI abil
  * 🔍 Valideeri kursuse kvaliteeti AI kaudu
* AI hinnangu salvestamine (`ai_score`, `ai_feedback`)
* QuizAnswer logid kasutajate vastustega

---

## 🧪 AI-toega kontrollid

* **Quiz vastused** – kasutaja sisestab, AI hindab punktidega (0–10) ja annab tagasisidet
* **Valideerimine** – AI analüüsib kursuse ülesehitust ja annab soovitusi
* **Soovitused** – süsteem pakub järgmise kursuse teemat olemasolevate põhjal

---

## 🔐 Turvalisus ja ligipääs

* Kasutaja näeb ainult enda kursuseid
* Administraator saab hallata kogu sisu
* CSRF kaitse ja sisendivalideerimine Django vormide kaudu

---

## 🧰 Laiendusvõimalused (järgmised etapid)

* 📦 PDF / Markdown eksport kursustest
* 📊 Kursuse progressi jälgimine (Chart.js)
* 🧑‍🤝‍🧑 Kursuse jagamine tiimide vahel
* 🌐 Avalik kataloog jagamiseks
* 📁 Failiüleslaadimised / lisamaterjalid

---

## ✅ Projekti valmidus

| Funktsioon                                  | Valmis |
| ------------------------------------------- | ------ |
| Kursuse loomine AI abil                     | ✅      |
| Moodulite & peatükkide struktuur            | ✅      |
| Viktoriinide vastamine ja hindamine         | ✅      |
| Admin AI-nupud (quiz, assignment, generate) | ✅      |
| Kursuse struktuuri valideerimine AI-ga      | ✅      |
| AI soovitus järgmise kursuse jaoks          | ✅      |
| Bootstrap5 responsive UI                    | ✅      |

---

## 📁 Failid & põhimallid

* `base.html` – navbar ja üldkujundus
* `home.html` – kursuse loomine + soovitus
* `course_detail.html` – moodulid, quiz’id, ülesanded
* `login.html`, `signup.html`, `logout.html` – autentimine
* `course_change_form.html`, `chapter_change_form.html` – AI-nuppudega admin vaated

---

Kui soovid, võin koostada ka:

* **README.md** GitHubi jaoks
* **PDF-esitlusfaili**/pitch decki
* **Swagger/OpenAPI skeemi** backend API laienduseks
* või genereerida automaatse testpaketi (`tests.py`)

Kas liigume järgmise sammuna millegi nendest suunas?
