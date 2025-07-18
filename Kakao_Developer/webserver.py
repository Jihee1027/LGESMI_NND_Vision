from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>LGESMI Vision Alert - 서비스 소개</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }
        h1 { color: #0047ab; }
        .section { margin-bottom: 30px; }
        .highlight { color: #d9534f; font-weight: bold; }
        ul { line-height: 1.6; }
    </style>
</head>
<body>
    <h1>LG Energy Solution, Michigan<br/>Notching and Dryer Vision Alert System</h1>

    <div class="section">
        <h2>서비스 개요</h2>
        <p>
            LG Energy Solution Michigan 공장의 Notching 및 Dryer 각 호기별 <span class="highlight">NG (불량) 결함률</span>과 관련된 데이터를 실시간으로 모니터링합니다.
            <br/>
            실시간 분석을 통해 결함률이 설정 임계치를 초과할 경우, 즉시 담당자에게 <strong>카카오톡 알림톡</strong>을 발송하여 빠른 대응을 돕습니다.
        </p>
    </div>

    <div class="section">
        <h2>주요 기능</h2>
        <ul>
            <li>각 호기별 NG defect rate 실시간 수집 및 시각화</li>
            <li>임계치 초과 시 자동으로 카카오톡 알림톡 발송</li>
            <li>관리자 및 현장 담당자별 맞춤 알림 설정 지원</li>
            <li>사용자 친화적인 웹 대시보드 제공</li>
            <li>카카오 로그인 연동으로 안전한 사용자 인증</li>
        </ul>
    </div>

    <div class="section">
        <h2>시스템 기대 효과</h2>
        <ul>
            <li>불량률 조기 감지 및 신속 대응으로 품질 향상</li>
            <li>생산 라인 중단 최소화 및 효율성 증대</li>
            <li>현장 커뮤니케이션 간소화 및 신뢰성 강화</li>
            <li>데이터 기반 의사결정 지원</li>
        </ul>
    </div>

    <div class="section">
        <h2>연락처</h2>
        <p>서비스 관련 문의: <a href="mailto:support@yourdomain.dev">support@yourdomain.dev</a></p>
    </div>
</body>
</html>
"""

@app.route("/vision-alert-test")
def vision_alert():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
