# build_quiz_html.py
from docx import Document
import html

docx_path = "250C_SV_ONTHIMONGDCT.CD.25.26.docx"
doc = Document(docx_path)

# Lấy tất cả đoạn văn không rỗng
paras = [p.text.strip() for p in doc.paragraphs if p.text.strip() != ""]

# Tách thành từng dòng nếu có newline
lines = []
for p in paras:
    parts = p.split('\n')
    for part in parts:
        t = part.strip()
        if t:
            lines.append(t)

# Parse sang cấu trúc câu hỏi
questions = []
current = None
import re
for line in lines:
    m = re.match(r'^(Câu\s*([0-9]{1,3}))\b(.*)', line, flags=re.I)
    if m:
        if current:
            questions.append(current)
        num = m.group(2)
        rest = line.replace(m.group(1), '').strip(' :.-–—')
        current = {"num": num, "text": rest, "options": []}
        continue
    # option dạng [<$>] text
    m_opt1 = re.match(r'^\[<\$\>\]\s*(.*)', line)
    if m_opt1 and current:
        letter = chr(ord('a') + len(current["options"]))
        current["options"].append({"letter": letter, "text": m_opt1.group(1)})
        continue
    # option dạng "A. text" hoặc "A) text"
    m_opt2 = re.match(r'^([A-Da-d])[.\)]\s*(.*)', line)
    if m_opt2 and current:
        letter = m_opt2.group(1).lower()
        current["options"].append({"letter": letter, "text": m_opt2.group(2)})
        continue
    # tiếp nối dòng của option trước
    if current and current["options"]:
        current["options"][-1]["text"] += " " + line
        continue

if current:
    questions.append(current)

# Key đáp án (đã do bạn cung cấp)
answer_key = {
# ... (chèn full JSON key ở đây; copy từ phần trước)
"1": "C", "2": "A", "3": "B", "4": "A", "5": "B", "6": "A", "7": "A", "8": "B", "9": "C", "10": "A",
    "11": "B", "12": "B", "13": "A", "14": "D", "15": "A", "16": "A", "17": "A", "18": "B", "19": "C", "20": "A",
    "21": "B", "22": "B", "23": "A", "24": "B", "25": "A", "26": "C", "27": "C", "28": "C", "29": "A", "30": "A",
    "31": "B", "32": "B", "33": "A", "34": "A", "35": "C", "36": "D", "37": "C", "38": "C", "39": "D", "40": "D",
    "41": "B", "42": "B", "43": "C", "44": "A", "45": "C", "46": "D", "47": "A", "48": "B", "49": "C", "50": "C",
    "51": "D", "52": "B", "53": "C", "54": "B", "55": "C", "56": "D", "57": "A", "58": "B", "59": "C", "60": "D",
    "61": "A", "62": "B", "63": "A", "64": "D", "65": "D", "66": "D", "67": "B", "68": "B", "69": "A", "70": "C",
    "71": "A", "72": "B", "73": "C", "74": "D", "75": "D", "76": "B", "77": "C", "78": "A", "79": "B", "80": "A",
    "81": "C", "82": "C", "83": "B", "84": "B", "85": "B", "86": "B", "87": "B", "88": "A", "89": "B", "90": "C",
    "91": "B", "92": "C", "93": "B", "94": "D", "95": "C", "96": "A", "97": "C", "98": "A", "99": "B", "100": "C",
    "101": "A", "102": "B", "103": "A", "104": "B", "105": "B", "106": "B", "107": "D", "108": "A", "109": "A", "110": "C",
    "111": "D", "112": "B", "113": "A", "114": "B", "115": "C", "116": "B", "117": "D", "118": "C", "119": "B", "120": "D",
    "121": "B", "122": "D", "123": "B", "124": "C", "125": "D", "126": "D", "127": "B", "128": "A", "129": "A", "130": "A",
    "131": "D", "132": "B", "133": "C", "134": "B", "135": "D", "136": "C", "137": "B", "138": "C", "139": "C", "140": "D",
    "141": "B", "142": "A", "143": "A", "144": "B", "145": "C", "146": "D", "147": "D", "148": "B", "149": "B", "150": "B",
    "151": "D", "152": "D", "153": "D", "154": "D", "155": "A", "156": "C", "157": "A", "158": "C", "159": "B", "160": "D",
    "161": "D", "162": "C", "163": "A", "164": "B", "165": "C", "166": "C", "167": "B", "168": "C", "169": "A", "170": "D",
    "171": "D", "172": "A", "173": "D", "174": "C", "175": "B", "176": "A", "177": "D", "178": "B", "179": "A", "180": "D",
    "181": "A", "182": "A", "183": "C", "184": "A", "185": "D", "186": "C", "187": "B", "188": "D", "189": "B", "190": "D",
    "191": "A", "192": "D", "193": "A", "194": "D", "195": "D", "196": "D", "197": "A", "198": "D", "199": "B", "200": "D",
    "201": "D", "202": "D", "203": "A", "204": "D", "205": "C", "206": "D", "207": "B", "208": "D", "209": "D", "210": "D",
    "211": "D", "212": "B", "213": "D", "214": "D", "215": "A", "216": "C", "217": "D", "218": "D", "219": "D", "220": "A",
    "221": "A", "222": "A", "223": "B", "224": "A", "225": "B", "226": "A", "227": "B", "228": "A", "229": "A", "230": "C",
    "231": "A", "232": "C", "233": "B", "235": "A", "236": "A", "237": "A", "238": "D", "239": "A", "240": "B",
    "241": "D", "242": "C", "243": "A", "244": "A", "245": "C", "246": "D", "247": "B", "248": "D", "249": "B", "250": "A"
}

# Sinh file HTML
html_parts = []
html_parts.append("""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"/>
<title>Quiz 250 câu — Đã tích hợp sẵn</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;background:#f3f6fb;padding:18px;color:#111}
.question{background:#fff;padding:12px;border-radius:8px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,0.06)}
.q-title{font-weight:600;margin-bottom:8px}
.opts{display:flex;flex-direction:column;gap:6px}
.opt{display:flex;gap:10px;align-items:flex-start;padding:8px;border-radius:8px;cursor:pointer;border:1px solid transparent}
.opt.correct{background:#e8fff0;border-color:#6ed28a}
.opt.wrong{background:#fff0f0;border-color:#f08a8a}
button{padding:8px 12px;border-radius:8px;border:1px solid #ccc;background:#1976d2;color:#fff;cursor:pointer}
#result{display:none;background:#fff;padding:12px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.1);margin-top:16px}
</style>
</head><body>
<h2>Quiz 250 câu — Tải từ file của bạn</h2>
<div style="margin-bottom:12px">
<button id="submitBtn">Nộp bài</button>
<button id="resetBtn" style="margin-left:8px">Làm lại</button>
<span style="margin-left:12px" id="stats"></span>
</div>
<div id="questions">""")

for q in questions:
    qnum = q["num"]
    text = html.escape(q["text"])
    html_parts.append(f'<div class="question" data-q="{qnum}"><div class="q-title">Câu {qnum}. {text}</div><div class="opts">')
    if q["options"]:
        for opt in q["options"]:
            letter = opt["letter"]
            otext = html.escape(opt["text"])
            html_parts.append(f'<label class="opt" data-letter="{letter}"><input type="radio" name="q_{qnum}" value="{letter}"> <strong>{letter.upper()}.</strong> {otext}</label>')
    else:
        for i, letter in enumerate(['a','b','c','d']):
            html_parts.append(f'<label class="opt" data-letter="{letter}"><input type="radio" name="q_{qnum}" value="{letter}"> <strong>{letter.upper()}.</strong> (Không có nội dung)</label>')
    html_parts.append("</div></div>")

html_parts.append("""</div>
<div id="result"></div>

<script>
const answerKey = %s;

function updateStats(){
  const total = document.querySelectorAll('.question').length;
  document.getElementById('stats').textContent = 'Tổng: ' + total + ' câu';
}
updateStats();

function grade(){
  const qDivs = document.querySelectorAll('.question');
  let correct=0, total=qDivs.length, wrong=[];
  qDivs.forEach(div=>{
    const qn = div.dataset.q;
    const chosen = div.querySelector('input:checked');
    const ans = answerKey[qn];
    div.querySelectorAll('.opt').forEach(o=>o.classList.remove('correct','wrong'));
    if (chosen){
      if (chosen.value === ans){
        chosen.parentElement.classList.add('correct');
        correct++;
      } else {
        chosen.parentElement.classList.add('wrong');
        const corr = div.querySelector('.opt[data-letter="'+ans+'"]');
        if (corr) corr.classList.add('correct');
        wrong.push(qn);
      }
    } else {
      const corr = div.querySelector('.opt[data-letter="'+ans+'"]');
      if (corr) corr.classList.add('correct');
      wrong.push(qn);
    }
  });
  const score = Math.round((correct/total*10)*100)/100;
  const rb = document.getElementById('result');
  rb.style.display = 'block';
  rb.innerHTML = '<h3>Kết quả</h3><p><b>Điểm:</b> '+score+' / 10</p><p><b>Đúng:</b> '+correct+'/'+total+'</p><p><b>Sai:</b> '+(total-correct)+'</p>' + (wrong.length?('<p><b>Câu sai:</b> '+wrong.join(', ')+'</p>'):'');
  rb.scrollIntoView({behavior:"smooth"});
}

document.getElementById('submitBtn').addEventListener('click',grade);
document.getElementById('resetBtn').addEventListener('click',()=>{
  document.querySelectorAll('input[type=radio]').forEach(i=>i.checked=false);
  document.querySelectorAll('.opt').forEach(o=>o.classList.remove('correct','wrong'));
  document.getElementById('result').style.display='none';
  window.scrollTo({top:0,behavior:'smooth'});
});
</script>
</body></html>""" % (repr(answer_key)))

html_content = "\n".join(html_parts)
with open("quiz_250_preloaded.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Đã tạo file quiz_250_preloaded.html")
