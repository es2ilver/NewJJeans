const url = 'http://localhost:3000/predict';
const input = "https://entertain.naver.com//read?oid=112&aid=0003649533&cid=1073788"

// 요청 보내는 파일 

fetch(url, {
  method: 'POST',
  headers: { // HTTP 요청의 헤더
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: `text=${encodeURIComponent(input)}`
})
.then(response => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then(data => {
  const result = data;
  console.log(result); // result 변수 출력
})
.catch(error => {
  console.error('Fetch error:', error);
});


