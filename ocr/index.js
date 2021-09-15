//index.js file
const Tesseract = require('tesseract.js');
Tesseract.recognize(
    // this first argument is for the location of an image it can be a //url like below or you can set a local path in your computer
    '/Applications/MAMP/htdocs/11straps-main/ocr/supporting-a-column/ch3/5.png',
    // this second argument is for the laguage 
    'eng', { logger: m => console.log(m) }
).then(({ data: { text } }) => {
    console.log(text);
})