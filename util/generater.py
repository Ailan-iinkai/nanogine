from datetime import datetime, timedelta
import os
import yaml
start_head = """
<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="UTF-8">
    <title>Nested List Example</title>
"""
style_part = """

    <style>
        /* 初期状態で非表示にする */
        ul ul {
            display: none;
        }
        .toggle {
            background-color: #f5f5f5; /* デフォルトの背景色を淡いグレーに変更 */
            color: #333; /* テキスト色 */
            border: 1px solid #f5f5f5; /* ボーダーを背景色と同じにして目立たなくする */
            padding: 8px 16px; /* パディングを調整 */
            cursor: pointer;
            transition: background-color 0.3s, border-color 0.3s; /* 背景色とボーダーの変化をアニメーション化 */
            border-radius: 5px; /* 角の丸みを追加 */
        }
        .toggle.active {
            background-color: #e9ecef; /* オンの状態の背景色 */
        }
        .toggle:hover {
            background-color: #e9ecef; /* ホバー時の背景色 */
        }
        #submit-btn {
            display: none; /* 最初は非表示 */
            margin-top: 10px;
            padding: 8px 16px; /* パディングを調整 */
            cursor: pointer;
            background-color: #007bff; /* 送信ボタンの背景色 */
            color: #fff; /* テキスト色 */
            border: none;
            transition: background-color 0.3s, border-color 0.3s; /* 背景色とボーダーの変化をアニメーション化 */
            border-radius: 5px; /* 角の丸みを追加 */
        }
        #submit-btn:hover {
            background-color: #0056b3; /* ホバー時の背景色 */
        }
    </style>
"""


end_head_start_body ="""
</head>
<body>
<h1>タグ選択<h1>
<h3>6個以上選択してね<h3>
"""

js_part = """

    <!-- 送信ボタン -->
    <button id="submit-btn">送信</button>

    <script>
    
    document.addEventListener("DOMContentLoaded", function() {
    var toggles = document.querySelectorAll('.toggle');
    toggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            var nestedList = this.nextElementSibling;
            if (nestedList) {
                if (nestedList.style.display === 'none' || nestedList.style.display === '') {
                    nestedList.style.display = 'block';
                } else {
                    nestedList.style.display = 'none';
                }
                this.classList.toggle('active'); // クリックされたボタンに'active'クラスをトグル
                checkSubmitButton(); // トグルが変更されたら送信ボタンの表示をチェック
            }
        });
    });

    // 送信ボタン
   var submitBtn = document.getElementById('submit-btn');
submitBtn.addEventListener('click', function() {
    var activeToggles = document.querySelectorAll('.toggle.active');
    var data = [];
    activeToggles.forEach(function(toggle) {
        data.push(toggle.textContent.trim());
    });

    // JSONデータを取得
    var jsonData = JSON.stringify(data);

    // リクエスト設定
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:5000/receive_tags';
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.alert('タグを保存したよ!!!😄');
            window.location.href = '/'; 
        } else {
            window.alert('データの送信中にエラーが発生しました。😨');
        }
    };

    // リクエスト送信
    xhr.send(jsonData);
});



    // トグルが10個を超えたら送信ボタンを表示
    function checkSubmitButton() {
        var activeToggles = document.querySelectorAll('.toggle.active');
        if (activeToggles.length > 5) {
            submitBtn.style.display = 'block';
        } else {
            submitBtn.style.display = 'none';
        }
    }

    // 最下層のボタンにもクリックイベントを設定
    var bottomToggles = document.querySelectorAll('.toggle:not(:has(ul))');
    bottomToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            this.classList.toggle('active');
            checkSubmitButton(); // トグルが変更されたら送信ボタンの表示をチェック
        });
    });
});

    
    
    

"""
end_body = """
    </script>
    <a href="/">home</a>
    </body>
</html>
"""

def gernerate_htmllist(data):
    html = ""
    for key, values in data.items():
        html += f"<li><button class='toggle'>{key}</button>"
        if isinstance(values, list):
            html += "<ul>"
            for value in values:
                html += f"<li><button class='toggle'>{value}</button></li>"
            html += "</ul>"
        elif isinstance(values, dict):
            html += "<ul>"
            html += gernerate_htmllist(values)
            html += "</ul>"
        html += "</li>"
    return html


def generate_html_from_yaml(yaml_data):
    print(yaml_data)
    html = f"""{start_head}{style_part}{end_head_start_body}<ul id="nested-list"> {gernerate_htmllist(yaml_data)} </ul>{js_part}{end_body}"""
    html 
    return html


def valid_cache() -> bool:
    cool_time = 3600
    cached = False
    if os.path.exists("../cache/next_time.inn"):
        with open(f'../cache/next_time.inn', 'r') as file:
            timestamp = file.read()
            stamped_time = datetime.fromtimestamp(int(timestamp))
        if datetime.now() > stamped_time:
            print('[info] Cahe Expired')
        else:
            print('[info] Cahe Valid')
            cached = True
    else:
        print('[info] Not Found ../cache/next_time.inn')
    with open(f'../cache/next_time.inn', 'w') as file:
        next_time = int((datetime.now() + timedelta(seconds=cool_time)).timestamp())
        file.write(str(next_time))
    return cached
        