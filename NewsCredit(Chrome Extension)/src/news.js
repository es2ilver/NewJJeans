const serverUrl = "http://127.0.0.1:5000";
const clickbait = function (node) {
  const text = [...node.getElementsByClassName('title_area')];

  text.forEach(function (el) {
    var links = el.getElementsByTagName('a');
    var link = "";
    for (var i = 0; i < links.length; i++) {
      link = (links[i].getAttribute("href"));
    }
    var encodedLink = encodeURIComponent(link);
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
      if (request.readyState === 4) {
        if (request.status === 200) {
          var htmlResponse = request.responseText; // API 응답 데이터
          var responseData = JSON.parse(request.responseText); // 파이썬에서 응답한 clickbait 값을 사용

          // HTML 데이터를 DOM으로 변환
          var parser = new DOMParser();
          var doc = parser.parseFromString(htmlResponse, 'text/html');
    
          //var clickbait = 0;
          var clickbaitClass = responseData.clickbaitClass;      
          var clickbait = responseData.prob;

          var clickbait_banner = el.appendChild(document.createElement("div"));
          if (clickbait >= 80 && clickbait <= 100) {
            clickbait_banner.style.textDecoration = "underline";
            clickbait_banner.style.color = "rgb(0, 128, 0)";
            clickbait_banner.style.textAlign = "right";
            clickbait_banner.textContent = clickbait + "%" + "(고)품질";
        } else if (clickbait >= 30) {
            clickbait_banner.style.textDecoration = "underline";
            clickbait_banner.style.color = "rgb(0, 0, 128)";
            clickbait_banner.style.textAlign = "right";
            clickbait_banner.textContent = clickbait + "%" + "(중)품질";
        } else {
            clickbait_banner.style.textDecoration = "underline";
            clickbait_banner.style.color = "rgb(128, 0, 0)";
            clickbait_banner.style.textAlign = "right";
            clickbait_banner.textContent = clickbait + "%" + "(저)품질";
        }
        console.log(clickbait_banner);
        console.log(el);
        
        }
      }
    };
   

    // AJAX 요청 보낼 때 도메인을 동일하게 맞춰줍니다.
    request.open("GET", serverUrl + "/predict?link=https://entertain.naver.com" + encodedLink, true);
    request.send();
  });
};

const observer = new MutationObserver(function (mutations) {
  mutations.forEach(function (mutation) {
    mutation.addedNodes.forEach(function (node) {
      if (node.nodeType === 1) { // ELEMENT_NODE
        clickbait(node);
      }
    });
  });
});

const config = {
  attributes: false,
  childList: true,
  characterData: false,
  subtree: true
};

observer.observe(document.body, config);

clickbait(document.body);
