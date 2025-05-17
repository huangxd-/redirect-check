from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/redirect-check', methods=['GET'])
def redirect_check():
    # 获取 query 参数中的 url
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "缺少 'url' 参数"}), 400

    headers = {
        "User-Agent": "AptvPlayer/1.4.6",
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10, allow_redirects=False)
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("Location")
            return jsonify({
                "status": response.status_code,
                "location": location
            }), 200
        else:
            return jsonify({
                "status": response.status_code,
                "message": "没有重定向",
                "content_snippet": response.text[:300]
            }), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时"}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "连接错误"}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"请求异常: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
