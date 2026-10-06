#typescript #код #информатика
````typescript
let words: string[] = ["Да", "Нет", "Возможно"];

let words_len: number = words.length;

let answer_index: number = Math.floor(Math.random() * words_len);  // * вместо +

  

prompt("Задавайте вопрос!");

console.log(words, words_len, answer_index);

alert(words[answer_index]);
````

Мы изучили базовый синтекс typescirpt, на данный момент мне кажется typescript кажется более удобный чем python.
Так-же мы сделали что-то вроде шара предсказаний