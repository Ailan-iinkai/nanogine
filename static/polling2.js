function pollResult() {
    // エンドポイントのURL
    var endpoint = '/picup/result';

    // ポーリング間隔（ミリ秒）
    var interval = 3000;

    // ポーリングを実行する関数
    function poll() {
        // XMLHttpRequestオブジェクトを作成
        var xhr = new XMLHttpRequest();

        // リクエストを開始
        xhr.open('GET', endpoint, true);

        // リクエストが完了したときの処理
        xhr.onload = function () {
            if (xhr.status === 204) {
                // ポーリングを継続
                setTimeout(poll, interval);
            } else if (xhr.status === 500) {
                const targetImages = document.querySelectorAll('img#target');
                targetImages.forEach(image => {
                    image.src = 'static/shockcat.gif';
                });
                // 画像の読み込みが完了した後にアラートを表示
                var img = new Image();
                img.onload = function() {
                    alert('ポーリングが中断されました：' + xhr.responseText);
                    window.location.href = '/';
                };
                img.src = 'static/shockcat.gif';
            } else if (xhr.status === 200) {
                // ポーリング成功
                alert('ニュースの取得が終わりました。');
                window.location.href = '/';
            } else {
                const targetImages = document.querySelectorAll('img#target');
                targetImages.forEach(image => {
                    image.src = 'static/shockcat.gif';
                });
                // 画像の読み込みが完了した後にアラートを表示
                var img = new Image();
                img.onload = function() {
                    alert('エラーが発生しました：' + xhr.status);
                    window.location.href = '/';
                };
                img.src = 'static/shockcat.gif';
            }
        };

        // リクエストを送信
        xhr.send();
    }

    // 最初のポーリングを開始
    poll();
}

// ページの読み込みが完了したらポーリングを開始
document.addEventListener("DOMContentLoaded", function () {
    pollResult();
});
