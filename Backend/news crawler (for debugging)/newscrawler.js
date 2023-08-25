const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://entertain.naver.com/home';
const headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
};

axios.get(url, { headers })
  .then(response => {
    const html = response.data;

    console.log(html);  


    const $ = cheerio.load(html);

    
    const titleLinks = $('a.title')
    .filter((i, link) => $(link).attr('href').startsWith('/read'))
    .map((i, link) => `https://entertain.naver.com${$(link).attr('href')}`)
    .get();
    
    titleLinks.forEach(newsLink => {
        console.log(newsLink);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
