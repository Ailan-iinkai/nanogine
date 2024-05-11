document.addEventListener("DOMContentLoaded", function() {
    // モーダル表示のタイマーを設定
    setTimeout(function() {
        var modalContainer = document.getElementById('modal-container');
        modalContainer.classList.add('visible'); // モーダル表示
    }, 10000);

    // ニュースボタンにクリックイベントを追加
    var newsBtn = document.getElementById('news-btn');
    newsBtn.addEventListener('click', function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/picup', true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                window.location.href = '/picup'; // リクエストが成功したら"/picup"にリダイレクト
            } else {
                console.error('リクエスト中にエラーが発生しました。');
            }
        };
        xhr.send();

        // ニュースボタンが押されたらモーダルを閉じる
        var modalContainer = document.getElementById('modal-container');
        modalContainer.classList.remove('visible'); // モーダル非表示
    });

    // モーダル以外の領域をクリックした際にモーダルを閉じる
    var modalContainer = document.getElementById('modal-container');
    modalContainer.addEventListener('click', function(event) {
        if (event.target === modalContainer) {
            modalContainer.classList.remove('visible'); // モーダル非表示
        }
    });
});
