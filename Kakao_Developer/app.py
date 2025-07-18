from flask import Flask, render_template_string

app = Flask(__name__)

# 앱 정보 (예시)
app_info = {
    "name": "LGESMI Vision Alert",
    "app_id": "1234567890",
    "description": "LGESMI Vision Alert는 AI 기반 비전 알림 서비스입니다.",
    "service_url": "https://yourdomain.dev/vision-alert-test",
    "contact_email": "kimjihee@lgensol.com"
}

# 간단한 HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{{ app_info.name }} - 서비스 정보</title>
</head>
<body>
    <h1>{{ app_info.name }}</h1>
    <p><strong>앱 ID:</strong> {{ app_info.app_id }}</p>
    <p><strong>설명:</strong> {{ app_info.description }}</p>
    <p><strong>서비스 링크:</strong> <a href="{{ app_info.service_url }}" target="_blank">{{ app_info.service_url }}</a></p>
    <p><strong>문의 이메일:</strong> <a href="mailto:{{ app_info.contact_email }}">{{ app_info.contact_email }}</a></p>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, app_info=app_info)

if __name__ == "__main__":
    app.run(debug=True)
