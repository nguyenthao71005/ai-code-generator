from flask import Flask, render_template, request
import os
import re
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

MODEL_NAME = "gemini-2.5-flash"
OUTPUT_DIR = "generated_codes"

api_key = "AIzaSyAL1RRJAE6_XyEvg-9iqDG2IZR7lXpaatM"
client = genai.Client(api_key=api_key) if api_key else None


def split_exercises(text):
    pattern = r"(Bài\s*(\d+)\s*:\s*.*?)(?=(?:\n\s*Bài\s*\d+\s*:)|\Z)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL)

    exercises = []
    for full_text, number in matches:
        exercises.append({
            "number": number,
            "content": full_text.strip()
        })

    return exercises


def clean_code_response(code):
    code = code.strip()

    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    elif code.startswith("```"):
        code = code[len("```"):].strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    return code


def generate_code_with_gemini(exercise_text):
    if not client:
        raise ValueError("Chưa tìm thấy GEMINI_API_KEY trong file .env")

    prompt = f"""
Bạn là trợ lý lập trình Python.

Hãy đọc đề bài sau và viết đúng 1 chương trình Python hoàn chỉnh.

Yêu cầu:
- Code chạy được
- Đơn giản, dễ hiểu
- Dùng input() và print() nếu phù hợp
- Nếu đề yêu cầu thư viện math thì hãy import đúng
- Không giải thích
- Không thêm markdown
- Chỉ trả về code Python thuần

Đề bài:
{exercise_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    code = response.text if response.text else ""
    return clean_code_response(code)


def save_code_file(number, code):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"Bai{number}.py"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return filepath


def ensure_git_repo():
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def git_has_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True
    )
    return bool(result.stdout.strip())


def git_push_all():
    subprocess.run(["git", "add", "."], check=True)

    if not git_has_changes():
        return "Không có thay đổi mới để commit."

    commit_message = f"Auto generate python exercises - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

    return "Đã commit và push code lên GitHub thành công."


@app.route("/", methods=["GET", "POST"])
def index():
    result_message = ""
    generated_files = []
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("exercise_text", "").strip()
        action = request.form.get("action", "generate")

        if not input_text:
            result_message = "Bạn chưa nhập đề bài."
            return render_template(
                "index.html",
                result_message=result_message,
                generated_files=generated_files,
                input_text=input_text
            )

        exercises = split_exercises(input_text)

        if not exercises:
            result_message = "Không tìm thấy đề bài theo định dạng 'Bài X: ...'"
            return render_template(
                "index.html",
                result_message=result_message,
                generated_files=generated_files,
                input_text=input_text
            )

        for ex in exercises:
            number = ex["number"]
            content = ex["content"]

            try:
                code = generate_code_with_gemini(content)
                filepath = save_code_file(number, code)
                generated_files.append({
                    "number": number,
                    "filepath": filepath,
                    "code": code
                })
            except Exception as e:
                generated_files.append({
                    "number": number,
                    "filepath": "Lỗi",
                    "code": f"Lỗi khi tạo code cho Bài {number}: {str(e)}"
                })

        if action == "generate_and_push":
            try:
                if not ensure_git_repo():
                    result_message = (
                        "Đã tạo file xong, nhưng thư mục này chưa phải Git repo. "
                        "Hãy chạy git init và kết nối remote GitHub trước."
                    )
                else:
                    git_message = git_push_all()
                    result_message = f"Tạo file xong. {git_message}"
            except Exception as e:
                result_message = f"Đã tạo file, nhưng push GitHub lỗi: {str(e)}"
        else:
            result_message = "Đã tạo file Python thành công."

    return render_template(
        "index.html",
        result_message=result_message,
        generated_files=generated_files,
        input_text=input_text
    )


if __name__ == "__main__":
    app.run(debug=True)