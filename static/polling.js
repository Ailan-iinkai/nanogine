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
                // ポーリングを中断し、エラーメッセージを表示
                alert('ポーリングが中断されました：' + xhr.responseText);
                window.location.href = '/';
            } else if (xhr.status === 200) {
                // ポーリング成功
                alert('ニュースの取得が終わりました。');
                window.location.href = '/';
            } else {
                // その他のステータスコードの場合、エラーメッセージを表示
                alert('エラーが発生しました：' + xhr.status);
                window.location.href = '/';
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
