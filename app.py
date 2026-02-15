from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze-task', methods=['POST'])
def smart_analyzer():
    # استلام البيانات القادمة من Make.com
    data = request.json
    message = data.get('text', '').strip()
    sender = data.get('sender', 'Unknown')

    # عقل "جوجل": منطق التصنيف التلقائي
    if any(word in message.lower() for word in ['سعر', 'بكم', 'قيمة']):
        category = "استفسار مالي"
        action = "إرسال قائمة الأسعار"
    elif any(word in message.lower() for word in ['مشكلة', 'عطل', 'بطيء']):
        category = "دعم فني"
        action = "فتح تذكرة صيانة"
    else:
        category = "طلب عام"
        action = "تحويل للمبيعات"

    # النتيجة التي ستعود إلى Make.com ليرسلها لـ Google Sheets
    return jsonify({
        "customer": sender,
        "original_message": message,
        "ai_category": category,
        "suggested_action": action
    })

if __name__ == '__main__':
    app.run(port=5000)
  
